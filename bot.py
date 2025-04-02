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
    welcome_message = (
        "🚀 Welcome to MarketPulse Bot! 🚀\n"
        "I provide real-time crypto analytics using Vybe APIs.\n\n"
        "Here’s what I can do:\n"
        "📊 /pulse <token> - Get live token data (e.g., /pulse SOL)\n"
        "🔔 /alert <token> <condition> - Set custom alerts (e.g., /alert SOL volume>50)\n"
        "📜 /history <token> - See historical trends (e.g., /history SOL)\n"
        "❓ /help - Show this message\n\n"
        "Start by trying /pulse SOL to see live data!"
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = (
        "📋 MarketPulse Bot Commands:\n"
        "📊 /pulse <token> - Live token data (e.g., /pulse SOL)\n"
        "🔔 /alert <token> <condition> - Set alerts (e.g., /alert SOL volume>50)\n"
        "📜 /history <token> - Historical trends (e.g., /history SOL)\n"
        "❓ /help - Show this message"
    )
    bot.reply_to(message, help_message)

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
