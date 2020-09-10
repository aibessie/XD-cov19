#此代码仅为模板，不用于填写
#使用该代码前请阅读Readme.md
#标￥为需要填写信息的地方
import requests
import json
import smtplib
import datetime
import time
from email.mime.text import MIMEText


def send_email(message):  # 发送一封邮件
    msg_from = '243078372@qq.com'  ￥ 发送方邮箱 
    passwd = 'udkgzqbullwlbihj' ￥ 发送方邮箱密码，QQ邮箱，新浪邮箱请填写授权码
    msg_to = msg_from  # 接收方，即自己给自己发
    a=int(time.strftime("%H",time.localtime()))
    if a >= 20:# 注意GitHub上是格林威治时间
        subject = '晨检'  # 主题
    elif a >=2 and a <=6:
        subject = '午检'  # 主题
    else:
        subject = '晚检'  # 主题
    msg = MIMEText(message)  # HTML纯文本格式发送邮件
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    s = smtplib.SMTP_SSL("smtp.qq.com",465 )  # ￥ 邮件服务器（引号内）及端口号（逗号后），在网上查找
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())


conn = requests.Session()
result_login = conn.post(
    url='https://xxcapp.xidian.edu.cn/uc/wap/login/check',
    data={'username': '17040520010', 'password': 'Daisc19990816'}#￥ username后填写学号，password后填写统一登录密码
)

if result_login.status_code != 200:
    print('登录错误，错误代码：', result_login.status_code)
    send_email(BJT +'\n'+'登录错误，错误代码：'+result_login.status_code)
    exit()
else:
    print('登录成功。')

data={
    "ymtys":"0",#一码通颜色
    "sfzx": "1",#是否在校
    "tw": "1",#体温范围：36.5°C~36.9°C
    "area": b'\xE9\x99\x95\xE8\xA5\xBF\xE7\x9C\x81\x20\xE8\xA5\xBF\xE5\xAE\x89\xE5\xB8\x82\x20\xE9\x95\xBF\xE5\xAE\x89\xE5\x8C\xBA',#陕西省 西安市 长安区
    "city": b'\xE8\xA5\xBF\xE5\xAE\x89\xE5\xB8\x82',#西安市
    "province": b'\xE9\x99\x95\xE8\xA5\xBF\xE7\x9C\x81',#陕西省
    "address": b'\xE8\xA5\xBF\xE6\xB2\xA3\xE8\xB7\xAF\xE5\x85\xB4\xE9\x9A\x86\xE6\xAE\xB5\x32\x36\x36\xE5\x8F\xB7\xE8\xA5\xBF\xE5\xAE\x89\xE7\x94\xB5\xE5\xAD\x90\xE7\xA7\x91\xE6\x8A\x80\xE5\xA4\xA7\xE5\xAD\xA6\xE9\x95\xBF\xE5\xAE\x89\xE6\xA0\xA1\xE5\x8C\xBA',#西沣路兴隆段266号西安电子科技大学长安校区
    "sfcyglq": "0",#是否处于隔离期
    "sfyzz": "0",#是否出现乏力、干咳、呼吸困难等症状
    "qtqk": "",#其他情况
    "askforleave": "0"
}

result_main = conn.post(
    url="https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save",
    data=data#填写数据
)

if result_main.status_code != 200:
    print("数据发送错误，错误代码：", result_main.status_code)
    send_email(BJT +'\n'+'数据发送错误，错误代码：'+result_login.status_code)
    exit()

respond_json=json.loads(result_main.text)

BJT=str(datetime.datetime.now() + datetime.timedelta(hours=+8))[:-7]

send_email(BJT +'\n'+respond_json['m'])
