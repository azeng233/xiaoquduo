# -*- coding: utf-8 -*-
import logging
import datetime
import json
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header

# Made by ZengChen
# https://zengchen233.cn/
logger = logging.getLogger()
url = r"https://mps.zocedu.com/corona/submitHealthCheck/submit"
url_info = r"https://mps.zocedu.com/corona/submitHealthCheck/getCurrentInfo"
defaultjson = {
    "data": {
        "checkPlace": "",
        "contactMethod": "",
        "teacher": "",
        "temperature": "36",
        "isCohabitFever": "否",
        "isLeavePalce": "否",
        "beenPlace": "",
        "isContactNcov": "否",
        "livingPlace": "",
        "livingPlaceDetail": "",
        "name1": "",
        "relation1": "",
        "phone1": "",
        "name2": "",
        "relation2": "",
        "phone2": "",
        "remark": "",
        "extraInfo": "[]",
        "healthStatus": "z",
        "emergencyContactMethod": "[]",
        "checkPlacePoint": "124,37",
        "checkPlaceDetail": "",
        "checkPlaceCountry": "",
        "checkPlaceProvince": "",
        "checkPlaceCity": "",
        "checkPlaceArea": "",
    },
    "other": {
        "openid": ""
    }
}
openid = ""
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
}
data = {}
jsonfile = "config.json"


# 获取JSESSIONID
def getSessionID():
    url = "https://mps.zocedu.com/corona/submitHealthCheck"
    res = requests.get(url, {
        "openId": openid,
        "latitude": "",
        "longitude": ""
    })
    sessionid = res.cookies.get("JSESSIONID")
    return sessionid


# 加载Json配置文件
def loadJson():
    global data, openid
    f = open(jsonfile, "r")
    obj = json.load(f)
    f.close()
    data = obj["data"]
    openid = obj["other"]["openid"]


# 打卡函数
def checkIn():
    cookies = {
        "JSESSIONID": getSessionID()
    }
    res = requests.post(url, data=data, headers=headers, cookies=cookies)
    if res.text == "":
        logger.info("校趣多打卡成功！当前时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        send_email()
    else:
        logger.error("校趣多打卡失败！请检查配置文件是否填写正确！")


# 创建配置文件
def createConfigFile():
    global defaultjson
    f = open(jsonfile, "w")
    json.dump(defaultjson, f, ensure_ascii=False, indent=2)
    f.close()


def send_email():
    # 参数
    global server
    sender = ""  # 发送邮件的地址
    pwd = ""  # smtp密码
    server_host = ""  # smtp主机地址
    receiver = ''  # 接收者邮箱

    # 邮件内容
    subject = '健康打卡已经完成！'
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    sentence = '当前时间为：' + time + '，当天健康打卡已经完成！'
    message = MIMEText(sentence, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender

    # 发送
    try:
        server = smtplib.SMTP_SSL(server_host)
        server.connect(server_host, 465)
        server.login(sender, pwd)
        server.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    server.close()


def handler(event, context):
    if not os.path.exists(jsonfile):
        createConfigFile()
        logger.error("未检测到配置文件，请填写config.json后运行本打卡脚本!")
        exit(0)
    else:
        loadJson()
        checkIn()