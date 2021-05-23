import io
import mimetypes
import os
import shutil
import traceback

from PIL import Image
from mutagen import MutagenError
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, ID3NoHeaderError
from mutagen.mp4 import MP4, MP4Cover

from Utils import Utils_FormatTools


def Utils_Meta_setMusicInfo(path, info):
    """
    TODO: Write lyrics to file
    :param path:文件目录
    :param info:字典,详情:
    {
        "TALB": "Name of Album",
        "TIT2": "Title",
        "TPE1": "Author,Separate with '/'",
        "APIC": "Path to cover photo",
        "STRICT": Boolean:strict cover mode,
        "TRANSCODE": Boolean:convert to mp3,
        "TRANSPATH": "Path to converted file"
    }
    :return: int {
        0: Nothing need done
        1: Need reExt
    }
    """
    status_code = 0
    try:
        id3 = ID3(path)
        id3.update_to_v23()
        id3.delall("TALB")
        id3.delall("TIT2")
        id3.delall("TPE1")
        id3.delall("APIC")

        id3.add(TALB(encoding=3, text=info["TALB"]))
        id3.add(TIT2(encoding=3, text=info["TIT2"]))
        id3.add(TPE1(encoding=3, text=info["TPE1"]))
        if info["STRICT"]:
            image = Image.open(info["APIC"])
            img_bytes = io.BytesIO()

            if image.size[0] > image.size[1]:
                image = image.crop((int((image.size[0] - image.size[1]) / 2), 0,
                                    int((image.size[0] + image.size[1]) / 2), image.size[1]))
            elif image.size[0] < image.size[1]:
                image = image.crop(
                    (0, int((image.size[1] - image.size[0]) / 2), 0, int((image.size[0] + image.size[1]) / 2)))
            image.resize((300, 300)).save(img_bytes, format="JPEG")
            id3.add(APIC(encoding=0, mime=mimetypes.guess_type(info["APIC"])[0], type=6, data=img_bytes.getvalue()))
        else:
            with open(info["APIC"], "rb") as f:
                id3.add(
                    APIC(encoding=0, mime=mimetypes.guess_type(info["APIC"])[0], type=6, data=f.read()))
        id3.save()
    except ID3NoHeaderError:
        traceback.print_exc()
        ext = os.path.splitext(path)[1]
        if ".flac" in ext or ".FLAC" in ext:
            flac = FLAC(path)
            flac.tags['TITLE'] = info["TIT2"]
            flac.tags['ALBUM'] = info["TALB"]
            flac.tags['ARTIST'] = info["TPE1"]
            with open(info["APIC"], "rb") as f:
                image = Image.open(info["APIC"])
                p = Picture()
                p.data = f.read()
                p.type = 3
                p.mime = mimetypes.guess_type(info["APIC"])[0]
                p.width = image.size[0]
                p.height = image.size[1]
                p.depth = 24  # color depth
                flac.add_picture(p)
                image.close()
            flac.save()
        else:
            try:
                mp4 = MP4(path)
                mp4.tags["\xa9alb"] = info["TALB"]
                mp4.tags["\xa9nam"] = info["TIT2"]
                mp4.tags["\xa9ART"] = info["TPE1"]
                with open(info["APIC"], "rb") as f:
                    mp4["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)]
                mp4.save()
                status_code = 1
            except Exception:
                traceback.print_exc()
        if info["TRANSCODE"]:
            if not os.path.exists(os.path.split(info["TRANSPATH"])[0]):
                os.makedirs(os.path.split(info["TRANSPATH"])[0])
            Utils_FormatTools.Utils_Format_autoTranscode(path, info["TRANSPATH"])
            info["TRANSCODE"] = False
            Utils_Meta_setMusicInfo(info["TRANSPATH"], info)
    except MutagenError:
        traceback.print_exc()
    return status_code
