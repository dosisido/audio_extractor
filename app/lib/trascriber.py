from lib.dev import is_dev_env
import whisper
from typing import Dict
from lib.config import MODEL_TYPE
 
import subprocess 
import os
import signal


def transcribe(file_path, model = MODEL_TYPE) -> Dict[str, str]:
    '''
    @return: ['text', 'segments', 'language']
    '''

    # warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
    model = whisper.load_model(model, device="cuda")

    if is_dev_env():
        print("Trascribing file")
        process = subprocess.Popen(["python", "timer.py"])
    result = model.transcribe(file_path)
    if process:
        os.kill(process.pid, signal.SIGINT)

    # print(result.keys()) # ['text', 'segments', 'language']
    return result
