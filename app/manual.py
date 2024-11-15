
from lib.trascriber import transcribe
from lib.dialog_file_path import get_files_path
import os
import time
from lib.config import MODEL_TYPE
from lib.utils import format_time_from_seconds
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



files = get_files_path()

for file in files:
    print("Elaborating: ", file)
    t0 = time.time()
    text = transcribe(file, MODEL_TYPE)["text"]
    file_path = os.path.dirname(file)
    file_name = os.path.basename(file).split(".")[0]
    with open(f"{file_path}/{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Time elapsed: ", format_time_from_seconds(time.time() - t0))


