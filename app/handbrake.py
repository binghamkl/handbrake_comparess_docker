import time
from datetime import datetime as dt
import datetime as date_util
import os
import subprocess
import shutil

source_dir = "/source"
work_dir = "/work"


def encode_file(src_dir: str, file: str, preset="Fast 1080p30"):
    """
    Encodes the file at source directory with the preset given.
    :param src_dir:
    :param file:
    :param preset:
    :return:
    """
    args = []
    try:
        # preset = "Hardware/H.265 VCN 1080p"
        newfile = file[:-3] + ".mp4"
        outfile = os.path.join(work_dir, newfile)
        convert_file = os.path.join(src_dir, file)
        write_to_log(f"Start {convert_file:}")
        args = ["-v", "-i", convert_file, "-o", outfile, "--preset", preset] # , "-e", "qsv_h264"]
        # subprocess.Popen(["HandBrakeCLI"] + args)
        try:
            subprocess.check_call(["HandBrakeCLI"] + args)
            # success remove the original file
            copy_to = os.path.join(src_dir, newfile)
            shutil.move(outfile, copy_to)
            if os.path.exists(copy_to):
                os.remove(os.path.join(src_dir, file))
            else:
                write_to_error_log("Error moving file {0}".format(copy_to))
                print("Error moving file {0}".format(copy_to))

        except subprocess.CalledProcessError as ex1:
            write_to_error_log(str(ex1))
            print(str(ex1))
            return False
    except Exception as ex:
        write_to_error_log(str(args) + chr(13) + str(ex))
        print("Error ")
        print(args, flush=True)
        print(str(ex), flush=True)
        print(file, flush=True)
        return False
    write_to_log(f"{convert_file:}->{copy_to:}")
    return True


def valid_file(file: str):
    """
    Returns True if file ends in .ts, otherwise returns False
    :param file:
    :return:
    """
    if file.endswith(".ts"):
        return True
    return False


def walk_directories(from_dir: str):
    """
    walks directories from the source directory.
    Checks any files found in the directory and subdirectories.
    If it's a valid file then it calls handbrake encode.
    :param from_dir:
    :return:
    """

    summary = [0, 0, 0]

    for sdir, directories, files in os.walk(from_dir):
        for file in files:
            if valid_file(file):
                summary[0] += 1
                result = encode_file(sdir, file)
                if result:
                    summary[1] += 1
                else:
                    summary[2] += 1

    return summary


def write_to_log(info: str):
    """
        Writes information to the log in the root.

    :return:
    """
    try:

        file = open(os.path.join(source_dir, "plexhandbrake.log"), "a")
        date_str = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
        print("{0:22}{1}".format(date_str, info), file=file)
        file.close()
    except Exception as ex:
        write_to_error_log(str(ex))


def write_to_error_log(error: str):
    """
        writes out the error log.
    :param error:
    :return:
    """
    try:
        file = open(os.path.join(source_dir, "plexhandbrake_error.log"), "a")
        date_str = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
        print("{0:22}{1}".format(date_str, error), file=file)
        file.close()
    except Exception as ex:
        print("error writing to error log")
        print(str(ex), flush=True)


def write_summary(results: list):
    """
    Writes out the results to a summary file.
    :param results:
    :return:
    """
    try:
        log_file = os.path.join(source_dir, "plexhandbrake_summary.log")
        existed = os.path.exists(log_file)
        file = open(log_file, "a")
        if not existed:
            print("{0:22}{1:10}{2:10}{3:10}".format("DateTime",
                                                    "Files", "Success",
                                                    "Errors"),
                  file=file)

        date_str = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
        print("{0:22}{1:10}{2:10}{3:10}".format(date_str,
                                                results[0], results[1],
                                                results[2]),
              file=file)
        file.close()

    except Exception as ex:
        write_to_error_log(str(ex))


def seconds_until_midnight():
    """
    Returns the # of seconds until midnight.
    :return:
    """
    now = dt.now().astimezone()
    next_day = now + date_util.timedelta(days=1)
    midnight = dt(next_day.year, next_day.month, next_day.day,
                  0, 0, 0).astimezone()
    return (midnight - now).total_seconds()


if __name__ == "__main__":
    while True:
        write_summary(walk_directories(source_dir))
        time.sleep(seconds_until_midnight())
