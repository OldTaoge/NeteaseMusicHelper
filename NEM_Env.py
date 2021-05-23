import os

import NEM_Data


def ENV_getProtected():
    """
    NEM_PHONE
    NEM_EMAIL
    NEM_PASS_MD5
    :return:
    """
    global_data = NEM_Data.Data_getData()
    env_list = ["NEM_PHONE", "NEM_EMAIL", "NEM_PASS_MD5", "NEM_NMTID", "NEM_MUSIC_U", "NEM_USER_ID", "NEM_API_PREFIX"]
    save_path = {
        "NEM_PHONE": ["user", "loginInfo", "phone"],
        "NEM_EMAIL": ["user", "loginInfo", "email"],
        "NEM_PASS_MD5": ["user", "loginInfo", "md5_pass"],
        "NEM_NMTID": ["user", "loginCookies", "NMTID"],
        "NEM_MUSIC_U": ["user", "loginCookies", "MUSIC_U"],
        "NEM_USER_ID": ["user", "id"],
        "NEM_API_PREFIX": ["api", "prefix"]
    }
    for env_n in env_list:
        if env_n in os.environ:
            cur_p = global_data
            for cur_pn in save_path[env_n][:-1]:
                cur_p = cur_p[cur_pn]
            cur_p[save_path[env_n][-1]] = os.environ[env_n]
    NEM_Data.Data_saveData()
