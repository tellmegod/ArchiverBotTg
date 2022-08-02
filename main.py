import telebot
import json
from urllib.request import urlopen

bot = telebot.TeleBot('API_KEY')
user_register_dict = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Let's find an old website! Type a website URL: ")
    user_register_dict[message.chat.id] = {}
    bot.register_next_step_handler(message, typeurl)

def typeurl(message):
    user_register_dict[message.chat.id]['site'] = message.text
    bot.reply_to(message, "Type a year, month, and day, like 20150613: ")
    bot.register_next_step_handler(message, msg)

def msg(message):
    user_register_dict[message.chat.id]['era'] = message.text
    url = "http://archive.org/wayback/available?url=%s&timestamp=%s" % (user_register_dict[message.chat.id]['site'], user_register_dict[message.chat.id]['era'])
    dt = json.loads(urlopen(url).read().decode("utf-8"))

    try:
        old_site = dt["archived_snapshots"]["closest"]["url"]
        bot.send_message(message.chat.id, "Found this copy: ")
        bot.send_message(message.chat.id, old_site)
    except:
        bot.send_message(message.chat.id, "Sorry, no luck finding" + user_register_dict[message.chat.id]['site'])

bot.polling(none_stop=True)
