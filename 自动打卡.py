# -*- coding: utf-8 -*-
import logging
import datetime
import json
import os
import pytz
import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header

logger = logging.getLogger()

# 邮箱参数
sender = ''  # 发送邮箱
pwd = ''  # 邮箱smtp密码
server_host = ''  # smtp地址
receiver = ''  # 接收者

# post地址
url = r"https://mps.zocedu.com/corona/submitHealthCheck/submit"
url_info = r"https://mps.zocedu.com/corona/submitHealthCheck/getCurrentInfo"

# 生成json文件
defaultjson = {
    "data": {
        "checkPlace": "",
        "contactMethod": "",
        "teacher": "",
        "temperature": "36.2",
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
        logger.info("校趣多打卡成功！当前时间：" + datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"))
        send_email()
    else:
        logger.error("校趣多打卡失败！请检查配置文件是否填写正确！")
        send_error_email()


# 创建配置文件
def createConfigFile():
    global defaultjson
    f = open(jsonfile, "w")
    json.dump(defaultjson, f, ensure_ascii=False, indent=2)
    f.close()


def send_email():
    global server
    # 邮件内容
    subject = '健康打卡已经完成！'
    time = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M")
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
    finally:
        server.close()


def send_error_email():
    global server
    # 邮件内容
    subject = '好像出错啦！'
    time = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M")
    sentence = '当前时间为：' + time + '，当天未完成健康打卡，请手动打卡，错误信息见控制台。'
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
    finally:
        server.close()


def handler(event, context):
    if not os.path.exists(jsonfile):
        createConfigFile()
        logger.error("未检测到配置文件，请填写config.json后运行本打卡脚本!")
        exit(0)
    else:
        loadJson()
        checkIn()