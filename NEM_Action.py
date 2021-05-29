import time

import NEM_Data
import NEM_Playlist
import NEM_Download


def Action_radar_to_pl():
    global_data = NEM_Data.Data_getData()
    radar_pl = NEM_Playlist.Playlist_getPlaylistDetail(3136952023)
    tracks_list = radar_pl["playlist"]["tracks"]
    track_id_str = _Action_TrackListToStr(tracks_list)
    if track_id_str in global_data["data"]["radarIdHash"]:
        return -1
    global_data["data"]["radarIdHash"].append(track_id_str)
    npl = NEM_Playlist.Playlist_getPlaylistCreate(time.strftime(global_data["config"]["dailyNameTemplate"]["radar"],
                                                                time.localtime()))
    NEM_Playlist.Playlist_getPlaylistAdd(npl["playlist"]["id"], track_id_str)
    return npl["playlist"]["id"]


def Action_downloadPlaylist(playlist_id, is_radar=False, is_favourite=False, is_recommend=False):
    playlist_detail = NEM_Playlist.Playlist_getPlaylistDetail(playlist_id)
    if is_radar:
        dl_type = "radar"
    elif is_favourite:
        dl_type = "favouriteMusic"
    elif is_recommend:
        dl_type = "recommend"
    else:
        dl_type = "playlist"
    NEM_Download.Download_fromTrackDetails(playlist_detail["playlist"]["tracks"], {
        "type": dl_type,
        "playlist": playlist_detail["playlist"]["name"]
    })


def Action_downloadFavourite():
    Action_downloadPlaylist(NEM_Playlist.Playlist_getUserFavourite()["id"], is_favourite=True)


def Action_recommendToPlaylist():
    global_data = NEM_Data.Data_getData()
    track_id_str = _Action_TrackListToStr(NEM_Playlist.Playlist_getRecommendSongs())
    npl = NEM_Playlist.Playlist_getPlaylistCreate(time.strftime(global_data["config"]["dailyNameTemplate"]["recommend"],
                                                                time.localtime()))
    NEM_Playlist.Playlist_getPlaylistAdd(npl["playlist"]["id"], track_id_str)
    return npl["playlist"]["id"]


def _Action_TrackListToStr(track_list):
    track_id_str = str(track_list[0]["id"])
    for track in track_list[1:]:
        track_id_str += "," + str(track["id"])
    return track_id_str
