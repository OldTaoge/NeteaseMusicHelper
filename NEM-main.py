import NEM_Action
import NEM_Autorun
import NEM_Browser
import NEM_Data
import NEM_Env

if __name__ == "__main__":
    NEM_Data.Data_NemData("file", "data.json")
    NEM_Env.ENV_getProtected()
    NEM_Browser.Browser_CheckLogin()
    # NEM_Browser.Browser_Request("userPlayList", )
    # print(NEM_Data.Data_getData())
    # print(NEM_Playlist.Playlist_getUserPlaylist())
    # print(NEM_Playlist.Playlist_getPlaylistDetail(3136952023))
    # print(NEM_Playlist.Playlist_getPlaylistCreate("test"))
    # print()
    # Utils_MetaTools.Utils_Meta_setMusicInfo("9c0e_16dd_8cde_16b6909c93cb93aad35d756a61f5e347.mp3", {
    #     "TALB": "China-w",
    #     "TIT2": "China-w",
    #     "TPE1": "Arealy仁辰/南有乔木",
    #     "APIC": "109951163104126448.jpg"
    # })
    # NEM_Action.Action_downloadPlaylist(6768969597, True)
    # NEM_Action.Action_downloadFavourite()
    # id = NEM_Action.Action_radar_to_pl()
    # NEM_Action.Action_downloadPlaylist(id, is_radar=True)
    # id = NEM_Action.Action_RecommendToPlaylist()
    # NEM_Action.Action_downloadPlaylist(id, is_recommend=True)
    print("Init successfully")
    NEM_Autorun.Autorun()
