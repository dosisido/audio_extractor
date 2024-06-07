from utils.dev import is_dev_env

import moviepy.editor as mp
import speech_recognition as sr

from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime
import shutil

import whisper
import warnings

from datetime import datetime

import os


import dotenv
dotenv.load_dotenv()
MODEL_TYPE = os.getenv("MODEL_TYPE")
TMP_FOLDER = os.getenv("TRANSCRIBER_FOLDER")
assert TMP_FOLDER.endswith("cache"), "TMP_FOLDER must end with 'cache'"


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
    
    def transcribe(self) -> str:
        assert MODEL_TYPE in ("tiny", "base", "small", "medium", "large"), "Invalid model type"     
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        model = whisper.load_model(MODEL_TYPE)

        if not os.path.isdir(TMP_FOLDER):
            os.mkdir(TMP_FOLDER)
        wav_file = os.path.join(TMP_FOLDER, "temp{:-%Y%m%d%H%M%S}.wav".format(datetime.now()))
        self.export_audio(wav_file)

        if is_dev_env(): print("Extracting audio...")
        result = model.transcribe(wav_file) # language="it-IT"

        # shutil.rmtree(TMP_FOLDER)
        os.remove(wav_file)
        self._video.close()
        # print(result.keys()) # ['text', 'segments', 'language']
        return result["text"]




def transcribe_audio(wav_file, txt_file):
    # Transcribe audio file to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source, duration=4)
    try:
        text = recognizer.recognize_google(audio)
        with open(txt_file, "w") as file:
            file.write(text)
        print(f"Transcription saved to {txt_file}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")



def extract_text(path, txt_file):
    """
    splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    then delete the chunks and only return the text
    """
    def mp3_wav(path):
        # source file
        source = path

        # create a directory to store the converted audio file
        folder_name = "dummy"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        temp_file = os.path.join(folder_name, "temp{:-%Y%m%d%H%M%S}.wav".format(datetime.now()))

        # convert wav to mp3
        sound = AudioSegment.from_mp3(source)
        sound.export(temp_file, format="wav")

        return temp_file

    file_name = mp3_wav(path)
    # open the audio file using pydub
    sound = AudioSegment.from_wav(file_name)

    # split audio sound where silence is 700 miliseconds or more and get chunks
    print("Chunking...")
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )

    # create a directory to store the audio chunks
    folder_name = "dummy"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = []
    recognizer = sr.Recognizer()


    # process each chunk
    print(f"Processing {len(chunks)} chunks")
    for i, audio_chunk in enumerate(chunks, start=1):
        print(f"{(i+1)/len(chunks)*100:3.2f}% complete", end="\r")
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            # try converting it to text
            try:
                text = recognizer.recognize_google(audio_listened)
            except sr.UnknownValueError:
                continue
            else:
                text = f"{text.capitalize()}."
                whole_text += text

    # deleting the temp folder
    shutil.rmtree("dummy")

    # return the text for all chunks detected

    with open(txt_file, "w") as file:
        file.write(" ".join(whole_text))

    return whole_text
