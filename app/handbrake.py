import time
import datetime
import os
import subprocess
import shutil

def ConvertFile(src_dir : str, file : str, preset = "Fast 1080p30"):
    try:
        # preset = "H.265 QSV 1080p"
        newfile = file[:-3] + ".mp4"
        outfile = os.path.join(work_dir, newfile)
        args = ["-i", os.path.join(src_dir, file),  "-o", outfile, "--preset", preset]
        # subprocess.Popen(["HandBrakeCLI"] + args)
        try:
            subprocess.check_call(["HandBrakeCLI"] + args)
            # success remove the original file
            copy_to = os.path.join(src_dir, newfile)
            shutil.move(outfile, copy_to)

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

def walk_directories(source_dir : str):
    for dir, directories, files in os.walk(source_dir):
        for file in files:
            if valid_file(file):
                ConvertFile(dir, file)


source_dir = "/source"
work_dir = "/work"

while True:
    walk_directories(source_dir)
    time.sleep(60 * 60)

