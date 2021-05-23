import os


def Utils_Format_autoTranscode(source, output):
    return os.system("ffmpeg -i '%s' '%s'" % (source, output))
