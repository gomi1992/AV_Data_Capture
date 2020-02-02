import json
import re
from configparser import ConfigParser

import requests
import AV_Data_Capture

cookie = ""


def get_115_dir_cid():
    url = "https://aps.115.com/natsort/files.php"
    querystring = {"aid": "1", "cid": "0", "o": "file_name", "asc": "1", "offset": "0", "show_dir": "1", "limit": "24",
                   "code": "", "scid": "", "snap": "0", "natsort": "1", "record_open_time": "1", "source": "",
                   "format": "json", "fc_mix": "0", "type": "", "star": "", "is_q": "", "is_share": ""}
    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "5dc22854-05f2-45dc-8de1-e36497b82577,91aa059f-dd4b-46f8-bd4e-65688c767bc1",
        'Host': "aps.115.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': cookie,
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    data = data['data']
    for d in data:
        if (d['n'] == "115r"):
            return d['cid']
    return None


def get_115_file_list(cid):
    url = "https://aps.115.com/natsort/files.php"

    querystring = {"aid": "1", "cid": cid, "o": "file_name", "asc": "1", "offset": "0",
                   "show_dir": "1", "limit": "1000", "code": "", "scid": "", "snap": "0", "natsort": "1",
                   "record_open_time": "1", "source": "", "format": "json", "fc_mix": "", "type": "", "star": "",
                   "is_q": "", "is_share": "", "suffix": "", "custom_order": ""}

    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "239cf3bf-ae63-4abd-ae45-2e633883616b,d31bbf24-6dee-4fbe-bce4-2e85706d0d05",
        'Host': "aps.115.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': cookie,
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    data = data['data']
    return data


def rename_115_file(fid, fname):
    url = "https://webapi.115.com/files/edit"

    querystring = {"fid": fid,
                   "file_name": fname}

    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "239cf3bf-ae63-4abd-ae45-2e633883616b,d31bbf24-6dee-4fbe-bce4-2e85706d0d05",
        'Host': "webapi.115.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': cookie,
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, headers=headers, data=querystring)

    data = json.loads(response.text)
    return data["state"]


if __name__ == '__main__':
    config_file = 'config.ini'
    Config = ConfigParser()
    Config.read(config_file, encoding='UTF-8')
    cookie = Config['115']['cookie']
    cid_115r = get_115_dir_cid()
    # print(cid_115r)
    files = get_115_file_list(cid_115r)
    print(len(files))
    for index, f in enumerate(files):
        filepath = f['n']
        houzhui = str(
            re.search('[.](AVI|RMVB|WMV|MOV|MP4|MKV|FLV|TS|avi|rmvb|wmv|mov|mp4|mkv|flv|ts)$', filepath).group())
        c_word = ""
        if '-c.' in filepath or '-C.' in filepath or '中文' in filepath or '字幕' in filepath:
            cn_sub = '1'
            c_word = '-C'  # 中文字幕影片后缀
        try:
            name = AV_Data_Capture.getNumber(filepath)
        except:
            print(filepath)
            break
        new_name = name + c_word + houzhui
        tmp = filepath.replace(name, "\033[0;31m%s\033[0m" % name)
        print(index + 1, "/", len(files), tmp, new_name)
        if filepath == new_name:
            continue

        # if not rename_115_file(f['fid'], new_name):
        #     print("error")
