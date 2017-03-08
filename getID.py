# -*- coding: utf-8 -*-  
import re
import requests  
import webbrowser
import base64  
import re  
import urllib
import urllib.parse
import rsa  
import json  
import binascii  
from bs4 import BeautifulSoup
  
class Userlogin:  
    def userlogin(self,username,password):  
        session = requests.Session()  
        url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=1364875106625'  
        url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'  
  
        #get servertime,nonce, pubkey,rsakv  
        resp = session.get(url_prelogin)  
        json_data  = re.findall(r'(?<=\().*(?=\))', resp.text)[0]
        data       = json.loads(json_data)  


        servertime = data['servertime']  
        nonce      = data['nonce']  
        pubkey     = data['pubkey']  
        rsakv      = data['rsakv']  
  
        # calculate su  
        print(urllib.parse.quote(username))
        su  = base64.b64encode(username.encode(encoding="utf-8"))  
  
        #calculate sp  
        rsaPublickey= int(pubkey,16)  
        key = rsa.PublicKey(rsaPublickey,65537)  
        message = str(servertime) +'\t' + str(nonce) + '\n' + str(password)  
        sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"),key))  
        postdata = {  
                            'entry': 'weibo',  
                            'gateway': '1',  
                            'from': '',  
                            'savestate': '7',  
                            'userticket': '1',  
                            'ssosimplelogin': '1',  
                            'vsnf': '1',  
                            'vsnval': '',  
                            'su': su,  
                            'service': 'miniblog',  
                            'servertime': servertime,  
                            'nonce': nonce,  
                            'pwencode': 'rsa2',  
                            'sp': sp,  
                            'encoding': 'UTF-8',  
                            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
                            'returntype': 'META',  
                            'rsakv' : rsakv,  
                            }  
        resp = session.post(url_login,data=postdata)  
        print ("logged")
        login_url = re.findall(r'http://weibo.*&retcode=0',resp.text)  
        #  
        print(login_url)
        respo = session.get(login_url[0])  
        return session
        #uid = re.findall('"uniqueid":"(\d+)",',respo.text)[0]  
        #url = "http://weibo.com/u/"+uid  

def getContent(session, uid):
    url = "http://service.account.weibo.com/show?rid=" + uid
    respo = session.get(url)  
    return respo.content

username = 'lisong1013@gmail.com'
password = ''
login = Userlogin()
session = login.userlogin(username,password) 
res = []

line_num = 0
fi = open('res.txt', 'r')
for line in fi:
#    line_num += 1
#    if line_num > 1000:
#        break
    content = getContent(session, line)
    str_content = content.decode('utf-8')
    pattern = re.compile(r"href=.http:././weibo.com./\w+./(\w+)")
    for m in re.findall(pattern, str_content):
        print (m)
        res.append(m)

f = open("weiboID1.txt", 'w')
f.write("\n".join(res))
f.close()
