import time
import datetime
import os
import subprocess

def ConvertFile(src_dir : str, file : str, preset = "Fast 1080p30"):
    try:
        # preset = "H.265 QSV 1080p"
        newfile = file[:-3] + ".mp4"
        args = ["-i", os.path.join(src_dir, file),  "-o", os.path.join(src_dir, newfile), "--preset", preset]
        # subprocess.Popen(["HandBrakeCLI"] + args)
        try:
            subprocess.check_call(["HandBrakeCLI"] + args)
            # success remove the original file
            os.remove(os.path.join(src_dir, file))
        except subprocess.CalledProcessError as ex1:
            print(str(ex1))
        print ("complete", flush=True)
    except Exception as ex:
        print("Error ")
        print(args, flush=True)
        print(str(ex), flush=True)
        print(file, flush=True)

def valid_file(file : str):
    if file.endswith(".ts"):
        return True
    return False

source_dir = "/source"
for dir, directories, files in os.walk(source_dir):
    for file in files:
        if valid_file(file):
            ConvertFile(dir, file)

while True:
    time.sleep(10)
    print(datetime.datetime.now(), flush=True)

