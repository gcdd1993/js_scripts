#!/usr/bin/env python
# -*- coding: utf-8 -*-
# v2p中青工具

import datetime
import random
import sys

import requests


def print_ts(s):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def read(key):
    """
    从elecV2p获取值
    :param key: 值名称
    :return: 值
    """
    try:
        r = requests.get(f"{v2p}/store?key={key}").json()
        # print(r)
        return r
    except:
        return {"value": ''}


def write(key, value):
    """
    修改值
    :param key: 值名称
    :param value: 值
    """
    body = {
        "type": "save",
        "data": {
            "key": key,
            "value": value
        }
    }
    # print(json.dumps(body))
    r = requests.put(f"{v2p}/store", json=body).json()
    # print(r)


def fetch_one_key(key):
    global msg
    value = read(key)
    msg += f"获取 {key} 数据 {value['value']}\n"


def fetch_key(key, split_key):
    """
    获取值并打印
    """
    global msg
    res = read(key)
    value = res["value"].split(split_key)
    if res["value"] == "" or len(value) <= 0:
        msg += f"没有获取到 {key} 数据，赶紧抓取，以免影响收益\n"
    else:
        msg += f"获取 {len(value)} 条 {key} 数据\n"
        # 打乱顺序提交
        random.shuffle(value)
        res["value"] = split_key.join(value)
        write(key, res)


def fetch_key_limit(key, split_key, limit):
    """
    获取值并限制值个数
    """
    global msg
    res = read(key)
    value = res["value"].split(split_key)
    if res["value"] == "" or len(value) <= 0:
        msg += f"没有获取到 {key} 数据，赶紧抓取，以免影响收益\n"
    else:
        msg += f"获取 {len(value)} 条 {key} 数据\n"
        if len(value) > limit:
            msg += f"只取最后一条 {key} 数据\n"
            res["value"] = split_key.join(item for item in value[(len(value) - limit):limit])
            write(key, res)


def query_data():
    # 中青
    # zqwzbody zq_timebody zqqdbody zqlookStartbody zqboxbody zq_cookie zq_withdraw zqllzbody zqsszbody
    fetch_key_limit("zq_cookie", "@", 1)
    fetch_key_limit("zq_timebody", "@", 1)
    fetch_key_limit("zqqdbody", "&", 1)
    fetch_key("zq_withdraw", "@")
    fetch_key("zqllzbody", "&")
    fetch_key("zqlookStartbody", "&")
    fetch_key("zqsszbody", "&")
    fetch_key("zqwzbody", "&")
    fetch_key("zqboxbody", "&")
    fetch_one_key("zqbody_index")

    # 晶彩 wzbody lookStartbody qdbody jc_timebody jc_cookie jcboxbody jc_withdraw
    fetch_key_limit("jc_timebody", "&", 1)
    fetch_key_limit("jc_cookie", "@", 1)
    fetch_key_limit("qdbody", "&", 1)
    fetch_key("jc_withdraw", "@")
    fetch_key("wzbody", "&")
    fetch_key("lookStartbody", "&")
    fetch_key("jcboxbody", "&")
    fetch_one_key("jcbody_index")


if __name__ == '__main__':
    # v2ps = ["http://172.16.1.22:8100", "http://172.16.1.23:8100", "http://172.16.1.24:8100"]
    msg = ""
    v2ps = ["http://localhost:8100"]
    for v2p in v2ps:
        query_data()
        print_ts(f"提示 -- {v2p}\n")
        print_ts(msg)
        msg = ""
