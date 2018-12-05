import requests
import time
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

class Query:
	def __init__(self, username, password):
		self.usr = username
		self.psw = password
		self.posturl = 'http://zhjw.dlut.edu.cn/loginAction.do' 
		self.postData = {'zjh':self.usr, 'mm':self.psw}
	
	def login(self):
		r = s.post(url=self.posturl, data=self.postData)
		flag = False if("重新" in r.text) else True
		#print(r.text)

		if flag:
			print('登陆成功')
		else:
			print('登陆失败，请检查您的学号与密码')

		return flag 
		
	def get_term_score(self):
		self.score = s.get('http://zhjw.dlut.edu.cn/bxqcjcxAction.do').text

	def get_all_score(self):
		self.score = s.get('http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=6989').text

	def save_html(self):
		self.score = s.get('http://zhjw.dlut.edu.cn/reportFiles/student/cj_zwcjd_all.jsp').text
		html_file = open("score.html","w")
		html_file.write(self.score)
		html_file.close()

def query_score():
	print('请输入您的学号：')
	usr = input()
	print('请输入您的密码：')
	psw = input()
	test = Query(usr, psw)

	if test.login() == True:
		print('请选择模式:')
		print('1 - 本学期所有成绩')
		print('2 - 培养方案成绩')
		print('3 - 保存成绩单到本地')
		print('4 - 成绩更新时发送成绩至邮箱')

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
		#print(soup.prettify())

		all_texts = []
		for item in soup.find_all('td',{'align':'center'}):
			text = item.text
			trans = text.maketrans("\n\t\r", "   ")
			text = text.translate(trans).strip()
			all_texts.append(text)
		#print(all_texts)

		if choice == '4':
			while True:
				test = Query(usr, psw)
				test.get_term_score()
				soup = BeautifulSoup(test.score, 'lxml')
				now_texts = []

				for item in soup.find_all('td',{'align':'center'}):
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
					for index in range(0, len(all_texts), 7):
						message += '%s:%s\n' % (all_texts[index+2], all_texts[index+6])
						
					send_mail(to_email=[''],
							 subject='成绩详情', message=message)
					all_texts = now_texts

		else:
			print("--------------------成绩详情--------------------")
			for index in range(0, len(all_texts), 7):
				print('%s:%s' % (all_texts[index+2], all_texts[index+6]))
			print("------------------------------------------------")	

	else:
		query_score()

def send_mail(to_email, subject, message, server='smtp.xx.com', from_email=''):
	msg = EmailMessage()
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = ', '.join(to_email)
	msg.set_content(message)
	server = smtplib.SMTP(server)
	#server.set_debuglevel(1)

	# 发送邮箱的帐号与密码
	server.login(from_email, '')
	server.send_message(msg)
	server.quit()
	print('发送成功！')

if __name__ == '__main__':
	s = requests.Session()
	query_score()
	input('按回车键退出')