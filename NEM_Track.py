import NEM_Browser


def Track_getSongUrl(tracks):
    return NEM_Browser.Browser_Request("trackGetURL", {"id": tracks})


def Track_getSongDetails(tracks):
    return NEM_Browser.Browser_Request("trackGetDetail", {"ids": tracks})
