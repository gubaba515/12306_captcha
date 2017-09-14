# /usr/bin/env python
# coding=utf8

import hashlib
import random
import requests
import json
import argparse


def translate(appKey, secretKey, fromLang, toLang, q):
    m1 = hashlib.md5()
    salt = random.randint(1, 65536)
    sign = '%s%s%d%s' % (appKey, q, salt, secretKey)
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()

    myurl = "http://openai.youdao.com/api?" \
            "appKey={appKey}&" \
            "q={q}&" \
            "from={fromLang}&" \
            "to={toLang}&" \
            "salt={salt}&" \
            "sign={sign}" \
        .format(
        **{  # input your content
            'appKey': appKey,
            'q': q,
            'fromLang': fromLang,
            'toLang': toLang,
            'salt': salt,
            'sign': sign
        }
    )

    try:
        t = requests.get(myurl)
        if t.status_code == 200:
            t_json = json.loads(t.text)
            translated_text = t_json['translation'][0]   # get information
            return translated_text
        else:
            print(t.text)
            return None
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--appKey', required=True, help='the AppID of youdao openai')
    parse.add_argument('--secretKey', required=True, help='the screctKey of youdao openai')
    parse.add_argument('--fromLang', default='EN', help="the language of source text")
    parse.add_argument('--toLang', default='zh-CHS', help='the language of target text')
    opt = parse.parse_args()

    s = requests.session()
    s.keep_alive = False

    to_translate_words = 'luna'
    translated_words = translate(opt.appKey, opt.secretKey, opt.fromLang, opt.toLang, to_translate_words)
    if translated_words is not None:
        print(translated_words)
