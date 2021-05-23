import time

import NEM_Playlist
import NEM_Download


def Action_radar_to_pl():
    radar_pl = NEM_Playlist.Playlist_getPlaylistDetail(3136952023)
    tracks_list = radar_pl["playlist"]["tracks"]
    track_id_str = str(tracks_list[0]["id"])
    for track in tracks_list[1:]:
        track_id_str += "," + str(track["id"])
    npl = NEM_Playlist.Playlist_getPlaylistCreate(time.strftime("%y.%m.%d", time.localtime()))
    NEM_Playlist.Playlist_getPlaylistAdd(npl["playlist"]["id"], track_id_str)
    return npl["playlist"]["id"]


def Action_downloadPlaylist(playlist_id, is_radar=False, is_favourite=False):
    playlist_detail = NEM_Playlist.Playlist_getPlaylistDetail(playlist_id)
    if is_radar:
        dl_type = "radar"
    elif is_favourite:
        dl_type = "favouriteMusic"
    else:
        dl_type = "playlist"
    NEM_Download.Download_fromTrackDetails(playlist_detail["playlist"]["tracks"], {
        "type": dl_type,
        "playlist": playlist_detail["playlist"]["name"]
    })


def Action_downloadFavourite():
    Action_downloadPlaylist(NEM_Playlist.Playlist_getUserFavourite()["id"], is_favourite=True)
