import time
from lib.utils import format_time_from_seconds
import sys


start = time.time()
while True:
    print(f" {format_time_from_seconds(time.time()-start)}", end='\r')
    time.sleep(1)