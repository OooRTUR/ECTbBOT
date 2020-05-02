import config
import time

import telebot
from  telebot import  apihelper

bot = telebot.TeleBot(config.TOKEN)

apihelper.proxy = {'https':'socks5://95.110.194.245:15808'}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['say'])
def send_say(message):
	bot.reply_to(message, "Say hello to my little friend!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()

while True:
	try:
		bot.polling(none_stop=True, interval=0, timeout=20)
		bot.send_message()
	except Exception as e:
		print(e.args)
		time.sleep(2)


