import json
import uuid

import requests
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
def crawl():
    proxies_num = 20
    for j in range(100):
        # get specific number proxies
        r = requests.get('http://127.0.0.1:8000/?count=%d'%proxies_num)
        ip_ports = json.loads(r.text)
        for i in range(len(ip_ports)):
            ip,port = ip_ports[i][0],ip_ports[i][1]
            try:
                proxies = {
                    'http': 'http://%s:%s' % (ip, port),
                    'https': 'http://%s:%s' % (ip, port)
                }
                res = requests.get("https://kyfw.12306.cn/passport/captcha/captcha-image",verify=False,timeout=5,proxies = proxies)
                if res.status_code != 200:
                    continue
                with open('./captcha/%s.jpg'%uuid.uuid4(),'wb') as to_write:
                    to_write.write(res.content)
            except Exception as e:
                requests.get('http://0.0.0.0:8000/delete?ip=%s' % ip)
                continue

from multiprocessing import Pool

pool = Pool(3)

for i in range(10):
    pool.apply_async(crawl,args=())

pool.close()
pool.join()
print('complete')