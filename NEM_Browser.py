import time
import traceback

import requests
import os

import NEM_Data


def Browser_Request(end_point, data, update_cookies=False):
    global_data = NEM_Data.Data_getData()
    cookies = global_data["user"]["loginCookies"]
    if len(cookies) != 0:
        for times in range(0, 5):
            try:
                request_o = requests.post(
                    global_data["api"]["prefix"] + global_data["api"]["paths"][end_point],
                    cookies=cookies,
                    data=data,
                    params={"timestamp": time.time()})
                if len(request_o.cookies) > 0 and update_cookies:
                    global_data["user"]["loginCookies"].update(request_o.cookies.items())
                    NEM_Data.Data_saveData()
                return request_o.json()
            except Exception:
                traceback.print_exc()
                print(end_point)
                print(request_o.content)



def Browser_Download(url, path):
    for times in range(0, 5):
        try:
            req = requests.get(url)
            with open(path, 'wb') as fd:
                for chunk in req.iter_content(4096):
                    fd.write(chunk)
            return
        except Exception:
            traceback.print_exc()
    print("Succeed to do download :" + os.path.split(url)[1])


def Browser_CheckLogin():
    if Browser_Request("signin", None)["code"] == 301 or Browser_Request("yunbeiSign", None)["code"] == 301:
        Browser_DoLogin()


def Browser_DoLogin():
    # TODO: Login By QRCode
    global_data = NEM_Data.Data_getData()
    if global_data["user"]["loginInfo"]["md5_pass"] is not None:
        if global_data["user"]["loginInfo"]["phone"] is not None:
            lo_res = Browser_Request("loginPhone", {
                "phone": global_data["user"]["loginInfo"]["phone"],
                "md5_password": global_data["user"]["loginInfo"]["md5_pass"]
            }, update_cookies=True)
        elif global_data["user"]["loginInfo"]["email"] is not None:
            lo_res = Browser_Request("loginEmail", {
                "email": global_data["user"]["loginInfo"]["phone"],
                "md5_password": global_data["user"]["loginInfo"]["md5_pass"]
            }, update_cookies=True)
        else:
            raise Exception("Login method not found")
        if lo_res["code"] != 200:
            raise Exception(lo_res["message"])
        else:
            global_data["user"]["id"] = lo_res["account"]["id"]
            NEM_Data.Data_saveData()
    else:
        raise Exception("password not fount")
