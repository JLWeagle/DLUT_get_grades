#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import smtplib
import json
from email.message import EmailMessage
from bs4 import BeautifulSoup

'''
    请修改conf.json配置文件内容，
    以使获取成绩等功能正常工作。
'''

with open('confs.json') as f:
    confs = json.load(f)


class Query:

    '''
        用于初始化登录信息，
        并获取成绩结果。
    '''

    def __init__(self, username, password):
        self.usr = username
        self.psw = password
        self.posturl = confs["url"]["post_url"]
        self.postData = {'zjh': self.usr, 'mm': self.psw}

    def login(self):
        r = s.post(url=self.posturl, data=self.postData)
        flag = False if("重新" in r.text) else True
        # print(r.text)

        if flag:
            print('登陆成功')

        else:
            print('登陆失败，请检查您的学号与密码')

        return flag

    def get_term_score(self):
        # 获取本学期成绩
        self.score = s.get(
            confs["url"]["term_score"]).text

    def get_all_score(self):
        # 获取全部成绩
        self.score = s.get(
            confs["url"]["all_score"]).text

    def save_html(self):
        # 将中文成绩单保存至本地
        self.score = s.get(
            confs["url"]["save_html"]).text
        html_file = open("score.html", "w")
        html_file.write(self.score)
        html_file.close()


def query_score():
    # 登录并完成所选功能
    usr = confs["login_info"]["username"]
    psw = confs["login_info"]["password"]
    test = Query(usr, psw)

    if test.login() == True:
        print('请选择模式:')
        print('1 - 本学期所有成绩')
        print('2 - 培养方案成绩')
        print('3 - 保存成绩单到本地')
        print('4 - 成绩更新时发送成绩至邮箱')

        if confs["login_info"]["defaultmode"]:
            choice = confs["login_info"]["defaultmode"]
        else:
            choice = input()

        if choice == '1' or choice == '4':
            test.get_term_score()

        elif choice == '2':
            test.get_all_score()

        elif choice == '3':
            test.save_html()
            print('成功保存至本地目录！')
            return

        else:
            print('请输入有效输入')
            query_score()

        soup = BeautifulSoup(test.score, 'lxml')
        # print(soup.prettify())

        all_texts = []
        for item in soup.find_all('td', {'align': 'center'}):
            text = item.text
            trans = text.maketrans("\n\t\r", "   ")
            text = text.translate(trans).strip()
            all_texts.append(text)
        # print(all_texts)

        if choice == '4':
            while True:
                test = Query(usr, psw)
                test.get_term_score()
                soup = BeautifulSoup(test.score, 'lxml')
                now_texts = []

                for item in soup.find_all('td', {'align': 'center'}):
                    text = item.text
                    trans = text.maketrans("\n\t\r", "   ")
                    text = text.translate(trans).strip()
                    now_texts.append(text)

                if now_texts == all_texts:
                    print('当前无成绩更新')
                    time.sleep(300)
                    continue

                else:
                    message = ''
                    for index in range(0, len(now_texts), 7):
                        message += '%s:%s\n' % (now_texts[index+2],
                                                now_texts[index+6])

                    send_mail(to_email=[confs["receive_email"]["username"]],
                              subject='成绩详情', message=message)
                    all_texts = now_texts

        else:
            print("--------------------成绩详情--------------------")
            for index in range(0, len(all_texts), 7):
                print('%s:%s' % (all_texts[index+2], all_texts[index+6]))
            print("------------------------------------------------")

    else:
        return


def send_mail(to_email, subject, message,
              server=confs["send_email"]["server"],
              from_email=confs["send_email"]["username"]):
    # 用于发送邮件
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)
    server = smtplib.SMTP(server)
    # server.set_debuglevel(1)
    server.login(from_email, confs["send_email"]["password"])
    server.send_message(msg)
    server.quit()
    print('发送成功！')


if __name__ == '__main__':
    s = requests.Session()
    query_score()
    input('按回车键退出')
