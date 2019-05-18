import config
import logging
from bs4 import BeautifulSoup
from dbhandler import DBHandler
from time import sleep

from vkhelper import login_to_vk

logging.basicConfig(format="[*] %(asctime)s - %(name)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
	database = DBHandler()
	database.add_id(update.message.chat_id)
	logger.info("Connected to bot: %d" % update.message.chat_id)
	bot.send_message(chat_id=update.message.chat_id, text="Hello")
	bot.send_message(chat_id=update.message.chat_id, text=database.get_latest_post()[0])

def stop(bot, update):
	database = DBHandler()
	database.delete_item(update.message.chat_id)
	logger.info("Disconnected from bot: %d" % update.message.chat_id)
	bot.send_message(chat_id=update.message.chat_id, text="Bye")
	bot.send_message(chat_id=update.message.chat_id, text="Stopped")

def get_latest_posts(session, database):
	page_text = session.get(config.VATRIUME_URL).text
	logger.info("Got VATRIUME page")
	soup = BeautifulSoup(page_text, 'html.parser')
	
	logger.info("Setup Beautiful Soup")

	res = database.get_latest_post()
	if len(res) == 0:
		last_post = ""
	else:
		last_post = res[0]

	logger.info("Fetch latest post")
	latest_posts = []

	for post in soup.find_all('div', attrs={'class': 'wall_item'}):
		post_author = post.find('div', attrs={'class': 'wi_author'}).text
		post_text = post.find('div', attrs={'class':'wi_body'}).text
		new_post = (post_text, post_author)

		logger.info("Author - %s" % post_author)

		latest_posts.append(new_post)
		logger.info("Appended new post")
		
		if new_post[0] == last_post:
			break

	database.update_latest_post(last_post, latest_posts[0][0])
	logger.info("Updated latest post")

	latest_posts.reverse()

	return latest_posts

def get_updates(database):
	session = login_to_vk(config.USERNAME, config.PASSWORD)
	return get_latest_posts(session, database)

def send_posts_to(bot, user, latest_posts):
	for post in latest_posts:
		text_to_send = config.FORMAT_POST % (post[1], post[0])
		logger.info("DEBUG: %s" % text_to_send)
		bot.send_message(chat_id=user, text=text_to_send)

def run(bot):
	database = DBHandler()
	while True:
		for user in database.get_items():
			latest_posts = get_updates(database)
			send_posts_to(bot, user, latest_posts)

		sleep(1 * config.HOURS)
