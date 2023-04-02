import requests
from bs4 import BeautifulSoup
from urllib import parse
from icecream import ic

import requests,time,random,hashlib,json

def translate(i):
    lts = str(int(time.time()*1000))
    salt = lts + str(random.randint(0,9))
    sign_str = 'fanyideskweb' + i + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
    m = hashlib.md5()
    m.update(sign_str.encode())
    sign = m.hexdigest()
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        "Referer": "https://fanyi.youdao.com/",
        "Cookie": 'OUTFOX_SEARCH_USER_ID=-1124603977@10.108.162.139; JSESSIONID=aaamH0NjhkDAeav9d28-x; OUTFOX_SEARCH_USER_ID_NCOO=1827884489.6445506; fanyi-ad-id=305426; fanyi-ad-closed=1; ___rl__test__cookies=1649216072438',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    }

    data = {
        "i": i,
        "from": "en",
        "to": "zh",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "lts": lts,
        "bv": "a0d7903aeead729d96af5ac89c04d48e",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }

    res = requests.post(url,headers=headers,data=data)
    response = json.loads(res.text)

    value = response['translateResult'][0][0]['tgt']
    return value

def searchweb(name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'}
    url = 'https://cn.bing.com/search?q={}'.format("what is "+name)
    res = requests.get(url,headers=headers)
    r = res.text
    soup=BeautifulSoup(r,'html.parser')
    jpgo=[]
    jpgo+=soup.find_all("div",class_="b_focusTextMedium")
    jpgo+=soup.find_all("div",class_="b_focusTextLarge")
    if len(jpgo)==0:
        return None
    return translate(jpgo[0].string)

# print(searchweb("fiddler"))

# print(parse.quote("什么是+python"))
# print("自从20世纪90年代初Python语言诞生至今" in soup.prettify())
# print(soup.findAll(name="div"))
# ic("rwrl_pri" in res.text)