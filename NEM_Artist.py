import NEM_Browser
import NEM_Download


def Artist_DownloadAll(id):
    """
    下载音乐家所有歌曲
    :param id:
    """
    req = NEM_Browser.Browser_Request("artistSongs", {
        "id": id,
        "limit": 50
    })

    detail = req["songs"]
    id_table = []
    offset = 0
    for song in detail:
        id_table.append(song["id"])
    while req["more"]:
        offset += 1
        req = NEM_Browser.Browser_Request("artistSongs", {
            "id": id,
            "limit": 50,
            "offset": offset * 50
        })
        for song in req["songs"]:
            if song["id"] not in id_table:
                detail.append(song)
                id_table.append(song["id"])

    art_detail = NEM_Browser.Browser_Request("artistDetail", {"id": id})

    album_detail = {}
    for song in detail:
        if song["al"]["id"] not in album_detail.keys():
            alb_de = NEM_Browser.Browser_Request("albumDetail", {"id": song["al"]["id"]})
            song["al"] = alb_de["album"]
            album_detail[song["al"]["id"]] = alb_de["album"]
        else:
            song["al"] = album_detail[song["al"]["id"]]

    NEM_Download.Download_fromTrackDetails(detail, {
        "type": "playList",
        "playlist": art_detail["data"]["artist"]["name"]
    })
    pass