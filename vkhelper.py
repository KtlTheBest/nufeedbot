import requests
import config
import re

def login_to_vk(username, password):
	session = requests.Session()

	first_page = session.get(config.VK_MAIN_PAGE).text
	
	ip_h = re.compile(r'ip_h=(.+?)&').search(first_page).group(1)
	lg_h = re.compile(r'lg_h=(.+?)&').search(first_page).group(1)

	data_to_send = config.VK_POST_DATA.format(ip_h, lg_h, username, password)

	session.post(config.VK_POST_PAGE, data=data_to_send)
	return session

def login_to_vk2(username, password):
	session = requests.Session()

	first_page = session.get(config.VK_MAIN_PAGE).text
	
	submit_to = re.compile(r'method="post" action="(.+?)"').search(first_page).group(1)

	data_to_send = config.VK_POST_DATA2.format(username, password)

	session.post(submit_to, data=data_to_send)
	print(session.get(config.VK_FEED_PAGE).text)
	return session
