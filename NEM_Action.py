import time

import NEM_Playlist
import NEM_Download


def Action_radar_to_pl():
    radar_pl = NEM_Playlist.Playlist_getPlaylistDetail(3136952023)
    tracks_list = radar_pl["playlist"]["tracks"]
    track_id_str = _Action_TrackListToStr(tracks_list)
    npl = NEM_Playlist.Playlist_getPlaylistCreate(time.strftime("T%y.%m.%d", time.localtime()))
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


def Action_eecommendToPlaylist():
    track_id_str = _Action_TrackListToStr(NEM_Playlist.Playlist_getRecommendSongs())
    npl = NEM_Playlist.Playlist_getPlaylistCreate(time.strftime("R%y.%m.%d", time.localtime()))
    NEM_Playlist.Playlist_getPlaylistAdd(npl["playlist"]["id"], track_id_str)
    return npl["playlist"]["id"]


def _Action_TrackListToStr(track_list):
    track_id_str = str(track_list[0]["id"])
    for track in track_list[1:]:
        track_id_str += "," + str(track["id"])
    return track_id_str
