from utils.dev import is_dev_env

import moviepy.editor as mp
import speech_recognition as sr

from datetime import datetime

import whisper
import warnings

from datetime import datetime

import os

from typing import Dict, List


from utils.config import MODEL_TYPE, TRANSCRIBER_FOLDER as TMP_FOLDER


class ElaborateMp4():
    _path: str
    _video: mp.VideoFileClip
    _max_duration: int | None = None 
    _chunk_size: int | None = None
    
    def __init__(self, video_path: str):
        assert video_path.endswith(".mp4"), "File must be an mp4 file"
        self._path = video_path
        self._video = mp.VideoFileClip(video_path)
    
    def export_audio(self, path: str):
        video = self._video.copy()
        if self._max_duration:
            video = self._video.subclip(0, self._max_duration)
        video.audio.write_audiofile(path)
        return self

    @property
    def max_duration(self):
        return self._max_duration
    
    @max_duration.setter
    def max_duration(self, duration: int):
        self._max_duration = duration
    
    def waw_extractor(self)-> str:
        if not os.path.isdir(TMP_FOLDER):
            os.mkdir(TMP_FOLDER)
        wav_file = os.path.join(TMP_FOLDER, "temp{:-%Y%m%d%H%M%S}.wav".format(datetime.now()))
        self.export_audio(wav_file)
        self._video.close()
        return wav_file

    def transcribe(self) -> str:

        wav_file = self.waw_extractor()
        result = transcribe(wav_file, MODEL_TYPE)
        # shutil.rmtree(TMP_FOLDER)
        os.remove(wav_file)

        return result["text"]


def transcribe(file_path, model = MODEL_TYPE) -> Dict[str, str]:
    '''
    @return: ['text', 'segments', 'language']
    '''

    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
    model = whisper.load_model(model)

    if is_dev_env(): print("Extracting audio...")
    result = model.transcribe(file_path) # language="it-IT"

    # print(result.keys()) # ['text', 'segments', 'language']
    return result
