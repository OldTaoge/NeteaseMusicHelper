import os.path
import re
import shutil
import traceback

import NEM_Browser
import NEM_Data
import NEM_Track

from Utils import Utils_MetaTools

7
def Download_fromTrackDetails(details, template_info):
    """

    :param details: Domain@NEM
    :param template_info: {
            "type": "nameTemplate, see @data.json",
            "playlist": "name of playlist"
    }
    :return:
    """
    ids_strs = []
    ids = ""
    ids_str_num = 0
    soup_info = {}
    for detail in details:
        id = detail["id"]
        ids += str(id) + ","
        ids_str_num += 1
        if ids_str_num >= 512:
            ids_strs.append(ids[0:-1])
            ids_str_num = 0
            ids = ""
        artist_name = ""
        for artist in detail["ar"]:
            if len(artist["tns"]) > 0:
                artist_name += artist["name"] + " (" + artist["tns"][0] + ")/"
            else:
                artist_name += artist["name"] + "/"
        artist_name = artist_name[:-1]
        if "tns" in detail.keys() and len(detail["tns"]) > 0:
            track_name = detail["tns"][0] + " (" + detail["name"] + ")"
        else:
            track_name = detail["name"]
        soup_info[id] = {
            "name": track_name,
            "artist": artist_name,
            "album_name": detail["al"]["name"],
            "album_cover_url": detail["al"]["picUrl"]
        }
    ids_strs.append(ids[0:-1])
    track_url_list = []
    for ids in ids_strs:
        track_url_list.extend(NEM_Track.Track_getSongUrl(ids)["data"])
    for track_url_o in track_url_list:
        current_id = track_url_o["id"]
        if track_url_o["url"] is None or len(os.path.splitext(track_url_o["url"])[1]) <= 1:
            # Retry
            retry_o = NEM_Track.Track_getSongUrl(current_id)["data"][0]
            if retry_o["url"] is None:
                print("Can not get URL of %d %s" % (current_id, soup_info.pop(current_id)))
                continue
            else:
                soup_info[current_id]["url"] = retry_o["url"]
        else:
            soup_info[current_id]["url"] = track_url_o["url"]
        soup_info[current_id] = _download_render(soup_info[current_id], template_info)
    _download_fromSoupInfos(soup_info)


def _download_fromSoupInfos(infos):
    global_data = NEM_Data.Data_getData()
    download_path = global_data["config"]["download"]["path"]
    tmp_path = os.path.join(download_path, global_data["config"]["download"]["tempPath"])
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    for id, info in infos.items():
        file_path = os.path.join(download_path, info["download_path"])
        if not os.path.exists(file_path):
            if not os.path.exists(os.path.split(file_path)[0]):
                os.makedirs(os.path.split(file_path)[0])

            file_tmp_path = os.path.join(tmp_path, os.path.split(file_path)[1])
            cover_path = file_tmp_path + os.path.splitext(info['album_cover_url'])[-1]
            NEM_Browser.Browser_Download(info["url"], file_tmp_path)
            NEM_Browser.Browser_Download(info['album_cover_url'], cover_path)
            Utils_MetaTools.Utils_Meta_setMusicInfo(file_tmp_path, {
                "TALB": info['album_name'],
                "TIT2": info['name'],
                "TPE1": info['artist'],
                "APIC": cover_path,
                "STRICT": global_data["config"]["output"]["strictCover"],
                "TRANSCODE": global_data["config"]["output"]["transcodeToMP3"],
                "TRANSPATH": os.path.join(download_path, global_data["config"]["nameTemplate"]["convertedPath"]
                                          .replace("%seg", os.path.sep)
                                          .replace("%sourcePath", os.path.splitext(file_path)[0] + ".mp3"))
            })
            try:
                shutil.move(file_tmp_path, file_path)
                os.remove(cover_path)
            except Exception:
                traceback.print_exc()
    os.rmdir(tmp_path)


def _download_render(soup_info, template_info):
    """
    :param soup_info:  {
            "name": "The name of track",
            "artist": "Author,Separate with ','"
            "album_name": "Name of Album",
            "album_cover_url": "URL of cover photo",
            "url": "URL of track"
    :param template_info: {
            "type": "nameTemplate, see @data.json",
            "playlist": "name of playlist"
    }
    :return: @param soup_info but add "download_path"
    """
    global_data = NEM_Data.Data_getData()
    soup_info["download_path"] = global_data["config"]["nameTemplate"][template_info["type"]] \
        .replace("%seg", os.path.sep) \
        .replace("%trackName", _download_validateFileName(soup_info["name"])) \
        .replace("%playlistName", template_info["playlist"]) \
        .replace("%artistName", soup_info["artist"].replace("/", ",")) \
        .replace("%suffix", os.path.splitext(soup_info["url"])[-1])
    return soup_info


def _download_validateFileName(name):
    return re.sub(r'[/\\:*?"<>|]', "_", name)
