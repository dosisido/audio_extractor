
from utils.trascriber import transcribe
from utils.dialog_file_path import get_files_path
import os
import time

def format_time(seconds):
    m = seconds // 60
    s = seconds % 60
    h = m // 60
    m = m % 60
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"


files = get_files_path()

for file in files:
    print("Elaborating: ", file)
    t0 = time.time()
    text = transcribe(file, "tiny")["text"]
    file_path = os.path.dirname(file)
    file_name = os.path.basename(file).split(".")[0]
    with open(f"{file_path}/{file_name}.txt", "w") as f:
        f.write(text)
    print("Time elapsed: ", format_time(time.time() - t0))


