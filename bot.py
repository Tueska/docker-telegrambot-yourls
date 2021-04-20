import telebot
import requests
import json
import os
import urllib.parse
import logging
from functools import wraps

API_TOKEN = os.environ['TELEGRAM_API']
SEC_SIG = os.environ['YOURLS_SECRET']
DOMAIN = os.environ['YOURLS_DOMAIN']
try:
    ADMIN_LIST = os.environ['ADMIN_LIST']
    restricted_mode = True
except:
    ADMIN_LIST = []
    restricted_mode = False


bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def restricted(func):
    @wraps(func)
    def wrapped(update, *args, **kwargs):
        user_id = update.from_user.id
        if (restricted_mode) and (str(user_id) not in ADMIN_LIST):
            print("Unauthorized access denied for {} - {}.".format(user_id, update.from_user.username))
            bot.send_message(update.chat.id, "Error: _Unauthorized access, try contacting the Botadmin_", parse_mode='Markdown')
            return
        return func(update, *args, **kwargs)
    return wrapped


@bot.message_handler(commands=['short'])
@restricted
def short(m):
    chat = m.text[9:]
    if chat == "":
        bot.send_message(m.chat.id, "/short <link>")
    else:
        arguments = len(m.text.split())
        link = urllib.parse.quote_plus(m.text.split()[1])
        if arguments > 2:
            keyword = urllib.parse.quote_plus(m.text.split()[2])
        else:
            keyword = ''
        if not link.startswith("http"):
            link = urllib.parse.quote_plus("http://"+link)
        url = 'https://' + DOMAIN + '/yourls-api.php?signature=' + SEC_SIG + '&action=shorturl&url=' + link + '&format=json&keyword=' + keyword
        print("User {} issued QUERY: link={} keyword={}".format(m.from_user.username, link, keyword))
        try:
            r = requests.get(url)
            res = r.json()
            if res["status"] == "success" or res["shorturl"] is not None :
                bot.send_message(m.chat.id, "*Short Link: *" + str(res["shorturl"]), parse_mode='Markdown')
                print("RESPONSE: " + str(res))     
            else:
                bot.send_message(m.chat.id, "Error: _" + str(res["message"]) + "_", parse_mode='Markdown')
        except KeyError:
            bot.send_message(m.chat.id, "Error: _" + str(res["message"]) + "_", parse_mode='Markdown')
        except json.JSONDecodeError:
            bot.send_message(m.chat.id, "Error: _YOURLS SERVER NOT REACHABLE; TRY AGAIN LATER_", parse_mode='Markdown')


@bot.message_handler(commands=['info'])
def info(m):
    chat = m.text[5:]
    if chat == "":
        bot.send_message(m.chat.id, "/info <key/link>")
    else:
        link = urllib.parse.quote_plus(m.text.split()[1])
        url = 'https://' + DOMAIN + '/yourls-api.php?signature=' + SEC_SIG + '&action=url-stats&shorturl=' + link + '&format=json'
        print("User: {} issued QUERY: link={}".format(m.from_user.username, link))
        try:
            r = requests.get(url)
            res = r.json()
            if res["message"] == "success":
                bot.send_message(m.chat.id, "*Short: *" + str(res["link"]["shorturl"]) + 
                "\n*URL:\t\t*" + str(res["link"]["url"]) + 
                "\n*Created:\t\t*" + str(res["link"]["timestamp"]) +
                "\n*Clicks:\t\t*" + str(res["link"]["clicks"]), parse_mode='Markdown')
                print("RESPONSE: " + str(res))
            else:
                bot.send_message(m.chat.id, "Error: _" + str(res["message"]) + "_", parse_mode='Markdown')
        except KeyError:
            bot.send_message(m.chat.id, "Error: _" + str(res["message"]) + "_", parse_mode='Markdown')
        except json.JSONDecodeError:
            bot.send_message(m.chat.id, "Error: _YOURLS SERVER NOT REACHABLE; TRY AGAIN LATER_", parse_mode='Markdown')

bot.polling(none_stop=True, timeout=999999)
