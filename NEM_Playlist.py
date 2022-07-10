import NEM_Browser
import NEM_Data
import NEM_Track


def Playlist_getUserPlaylist():
    global_data = NEM_Data.Data_getData()
    user_id = global_data["user"]["id"]
    return NEM_Browser.Browser_Request("userPlayList", {"uid": user_id})


def Playlist_getUserFavourite():
    return Playlist_getUserPlaylist()["playlist"][0]


def Playlist_getPlaylistDetail(playlist_id):
    playlist_o = NEM_Browser.Browser_Request("playlistDetail", {"id": playlist_id})
    ids_str = ""
    tracks = playlist_o["playlist"]["trackIds"]
    playlist_o["playlist"]["tracks"] = []
    len_per_req = 512
    if len(tracks) >= len_per_req:
        parts = int(len(tracks) / len_per_req)
        for i in range(parts):
            for tracker_id_o in tracks[len_per_req*i:len_per_req+len_per_req*i]:
                ids_str += str(tracker_id_o["id"]) + ","
            ids_str = ids_str[0:-1]
            playlist_o["playlist"]["tracks"] += NEM_Track.Track_getSongDetails(ids_str)["songs"]
            ids_str = ""
    else:
        for tracker_id_o in playlist_o["playlist"]["trackIds"]:
            ids_str += str(tracker_id_o["id"]) + ","
        ids_str = ids_str[0:-1]
        playlist_o["playlist"]["tracks"] = NEM_Track.Track_getSongDetails(ids_str)["songs"]
    return playlist_o


def Playlist_getPlaylistCreate(playlist_name):
    return NEM_Browser.Browser_Request("playlistCreate", {"name": playlist_name})


def Playlist_getPlaylistAdd(playlist_id, tracks):
    return NEM_Browser.Browser_Request("playlistAdd", {"op": "add",
                                                       "pid": playlist_id,
                                                       "tracks": tracks})


def Playlist_getRecommendSongs():
    return NEM_Browser.Browser_Request("recommendSong", None)["data"]["dailySongs"]
