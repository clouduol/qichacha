#! /usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup

# convert cookies to dict
# copy valid cookies form browser to data/cookies first
def get_cookie():
    cookies={}
    with open('data/cookies','r') as f:
        for line in f.read().split(';'):
            name,value=line.strip().split('=',1)  #1代表只分割一次
            cookies[name]=value 
    return cookies

if __name__=="__main__":
    host="www.qichacha.com"
    headers = {'Accept-Encoding': 'gzip, deflate', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Connection': 'keep-alive', 'Host': 'www.qichacha.com', 'Accept-Language': 'zh-CN,zh;q=0.9', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    cookies = get_cookie()
    # convert cookies dict to RequestsCookieJar object
    cookiejar=requests.utils.cookiejar_from_dict(cookies)

    s=requests.session()
    s.headers.update(headers)
    s.cookies=cookiejar

    # search firm name
    r=s.get('http://www.qichacha.com/search?key=北京极地加科技有限公司')
    # print(r.text)

    re_firm=r'a href="(/firm.*)" target="_blank" class="ma_h1"'
    partial_urls=re.findall(re_firm, r.text)
    if len(partial_urls) == 0:
        print("no firm matched")
        exit
    firm_url="http://"+host+partial_urls[0]
    print(firm_url)

    # get firm info page
    infos = {"time":"", "phone":"", "email":"", "address":"", "industry":""}
    r=s.get(firm_url)
    # print(r.text)
    soup=BeautifulSoup(r.text,"lxml")
    # first block
    span_phone=soup.find('span', text="电话：")
    infos["phone"]=span_phone.find_next_sibling().find_next().string.strip("\n ")
    span_email=soup.find('span', text="邮箱：")
    infos["email"]=span_email.find_next_sibling().find_next().string.strip("\n ")
    span_address=soup.find('span', text="地址：")
    infos["address"]=span_address.find_next_sibling().find_next().string.strip("\n ")
#    div=soup.find('div', class_='content')
#    spans=div.find_all('span', recursive=True)
#    for span in spans:
#        if span.string == "电话：":
#            infos["phone"]=span.find_next_sibling().find_next().string.strip("\n ")
#        if span.string == "邮箱：":
#            infos["email"]=span.find_next_sibling().find_next().string.strip("\n ")
#        if span.string == "地址：":
#            infos["address"]=span.find_next_sibling().find_next().string.strip("\n ")

    # second block
    td_time=soup.find('td', text=re.compile(r"成立日期"))
    infos["time"]=td_time.find_next_sibling().string.strip("\n ")
    td_address=soup.find('td', text=re.compile(r"所属行业"))
    infos["industry"]=td_address.find_next_sibling().string.strip("\n ")

    print(infos)

