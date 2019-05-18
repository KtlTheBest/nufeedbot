import threading
import logging

from telegram.ext import Updater, CommandHandler

import nufeedbot
import config

logging.basicConfig(format="[*] %(asctime)s - %(name)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
	logger.info("Started bot...")
	updater = Updater(config.TOKEN)
	logger.info("Initiated updater with TOKEN")

	thread = threading.Thread(target=nufeedbot.run, args=(updater.bot, ))
	logger.info("Setup the nufeedbot.run() thread")
	thread.start()
	logger.info("Start nufeedbot.run() thread")

	dp = updater.dispatcher
	logger.info("Created dispatcher handler")
	dp.add_handler(CommandHandler('start', nufeedbot.start))
	logger.info("Added 'start' command handler")
	dp.add_handler(CommandHandler('stop',  nufeedbot.stop ))
	logger.info("Added 'stop' command handler")
	updater.start_polling()
	logger.info("Started polling")


if __name__ == "__main__":
	main()
