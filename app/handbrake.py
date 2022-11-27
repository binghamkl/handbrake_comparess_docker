import time
import datetime
import os


def ConvertFile(file, preset = "Fast 1080p30"):
    try:
        newfile = file[:-3] + ".mp4"
        os.execl("HandBrakeCLI", "-i", "\"" + os.path.join(source_dir, file) + "\"", "-o", '"' + os.path.join(source_dir, newfile) + '"', "--preset", preset)
        print ("complete", flush=True)
    except:
        print("Error ")
        print(file, flush=True)


source_dir = "/source"
files = os.listdir(source_dir)
for file in files:
    if file.endswith(".ts"):
        ConvertFile(file)

while True:
    time.sleep(10)
    print(datetime.datetime.now(), flush=True)

