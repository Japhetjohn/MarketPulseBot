import telebot
from dotenv import load_dotenv
import os
from vybe_api import get_token_pulse, get_token_history
from alerts import start_alert_thread, alerts

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to MarketPulse Bot! Use /pulse <token> for insights.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Commands:\n/pulse <token> - Live data\n/alert <token> <condition> - Set alert\n/history <token> - Past trends")

@bot.message_handler(commands=['pulse'])
def send_pulse(message):
    try:
        token = message.text.split()[1]
        reply = get_token_pulse(token)
        bot.reply_to(message, reply)
    except IndexError:
        bot.reply_to(message, "Usage: /pulse <token>")

@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        parts = message.text.split(maxsplit=2)
        token, condition = parts[1], parts[2]
        alerts[message.chat.id] = {"token": token, "condition": condition}
        bot.reply_to(message, f"Alert set for {token}: {condition}")
    except IndexError:
        bot.reply_to(message, "Usage: /alert <token> <condition>")

@bot.message_handler(commands=['history'])
def send_history(message):
    try:
        token = message.text.split()[1]
        reply = get_token_history(token)
        bot.reply_to(message, reply)
    except IndexError:
        bot.reply_to(message, "Usage: /history <token>")

if __name__ == "__main__":
    start_alert_thread(bot)
    bot.polling()
