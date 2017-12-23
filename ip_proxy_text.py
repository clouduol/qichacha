#! /usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import socket
import socks


def init_proxy():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket=socks.socksocket

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
    # set proxy
    init_proxy()
    print("after proxy")
    r=requests.get("http://icanhazip.com")
    print(r.text)

    host="www.qichacha.com"
    headers = {'X-Forwarded-For':'104.236.170.168','Accept-Encoding': 'gzip, deflate', 'Referer':'http://www.qichacha.com','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Connection': 'keep-alive', 'Host': 'www.qichacha.com', 'Accept-Language': 'zh-CN,zh;q=0.9', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    cookies = get_cookie()
    # convert cookies dict to RequestsCookieJar object
    cookiejar=requests.utils.cookiejar_from_dict(cookies)

    s=requests.session()
    s.headers.update(headers)
    s.cookies=cookiejar

    infos = {"time":"", "phone":"", "email":"", "address":"", "industry":""}
    # search firm name
    r=s.get('http://www.qichacha.com/search?key=北京极地加科技有限公司')
    #print(r.text)

    soup=BeautifulSoup(r.text, "lxml")
    table=soup.find('table', class_="m_srchList")
    td=table.find('tbody').find('tr').find('td').find_next_sibling()
    partial_url=td.find('a')["href"]
    current_p=td.find('p')
    span_time=current_p.find('span').find_next_sibling()
    infos["time"]=span_time.string.split("：")[1].strip("\n ")
    #current_p=current_p.find_next_sibling()
    #infos["phone"]=current_p.string.split("：")[1].strip("\n ")
    #infos["email"]=current_p.find('span').string("：")[1].strip("\n ")
    #current_p=current_p.find_next_sibling()

    #re_firm=r'a href="(/firm.*?)" target="_blank" class="ma_h1"'
    #partial_urls=re.findall(re_firm, r.text)
    #if len(partial_urls) == 0:
    #    print("no firm matched")
    #    exit()
    #firm_url="http://"+host+partial_urls[0]
    if partial_url == None:
        print("no firm matched")
        exit()
    firm_url="http://"+host+partial_url
    print(firm_url)

    # get firm info page
    r=s.get(firm_url)
    # print(r.text)
    soup=BeautifulSoup(r.text,"lxml")
    # first block
#    div=soup.find('div', class_='content')
#    spans=div.find_all('span', recursive=True)
#    for span in spans:
#        if span.string == "电话：":
#            infos["phone"]=span.find_next_sibling().find_next().string.strip("\n ")
#        if span.string == "邮箱：":
#            infos["email"]=span.find_next_sibling().find_next().string.strip("\n ")
#        if span.string == "地址：":
#            infos["address"]=span.find_next_sibling().find_next().string.strip("\n ")
    span_phone=soup.find('span', text="电话：")
    strtmp=span_phone.find_next_sibling().find_next().string
    if strtmp != None:
        strtmp = strtmp.strip("\n ")
    infos["phone"]=strtmp
    span_email=soup.find('span', text="邮箱：")
    strtmp=span_email.find_next_sibling().find_next().string
    if strtmp != None:
        strtmp = strtmp.strip("\n ")
    infos["email"]=strtmp
    span_address=soup.find('span', text="地址：")
    strtmp=span_address.find_next_sibling().find_next().string
    if strtmp != None:
        strtmp = strtmp.strip("\n ")
    infos["address"]=strtmp
    # second block
    td_time=soup.find('td', text=re.compile(r"成立日期"))
    if td_time != None:
        strtmp=td_time.find_next_sibling().string
        if strtmp != None:
            strtmp = strtmp.strip("\n ")
        infos["time"]=strtmp
    td_address=soup.find('td', text=re.compile(r"所属行业"))
    if td_address != None:
        strtmp=td_address.find_next_sibling().string
        if strtmp != None:
            strtmp = strtmp.strip("\n ")
        infos["industry"]=strtmp

    print(infos)

