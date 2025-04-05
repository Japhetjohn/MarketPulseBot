import telebot
from dotenv import load_dotenv
import os
from vybe_api import get_token_pulse, get_token_history
from alerts import start_alert_thread, alerts
from flask import Flask
from threading import Thread

# Load the .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Set up Flask app
app = Flask('')

@app.route('/')
def home():
    return "MarketPulse Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Welcome message with all commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "🚀 Welcome to MarketPulse Bot! 🚀\n"
        "I give you crypto data using Vybe APIs.\n\n\n"
        "Here’s what I can do:\n\n\n"
        "📊 /pulse <token> - See live volume (e.g., /pulse SOL)\n\n"
        "🔔 /alert <token> <condition> - Set volume alerts (e.g., /alert SOL volume>50)\n\n"
        "📜 /history <token> - See past prices (e.g., /history SOL)\n\n"
        "❓ /help - Show this message\n\n"
        "Try /pulse SOL to start!"
    )
    bot.reply_to(message, welcome_message)

# Help message
@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = (
        "📋 MarketPulse Bot Commands:\n\n\n"
        "📊 /pulse <token> - Live volume (e.g., /pulse SOL)\n\n"
        "🔔 /alert <token> <condition> - Set volume alerts (e.g., /alert SOL volume>50)\n\n"
        "📜 /history <token> - Past prices (e.g., /history SOL)\n\n"
        "❓ /help - Show this message"
    )
    bot.reply_to(message, help_message)

# /pulse command to get live data
@bot.message_handler(commands=['pulse'])
def send_pulse(message):
    try:
        token = message.text.split()[1]  # Get the token (e.g., SOL)
        reply = get_token_pulse(token)
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "Please use: /pulse <token> (e.g., /pulse SOL)")

# /alert command to set alerts
@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        parts = message.text.split(maxsplit=2)
        token, condition = parts[1], parts[2]  # e.g., SOL volume>50
        alerts[message.chat.id] = {"token": token, "condition": condition}
        bot.reply_to(message, f"Alert set for {token}: {condition}")
    except:
        bot.reply_to(message, "Please use: /alert <token> <condition> (e.g., /alert SOL volume>50)")

# /history command to get past data
@bot.message_handler(commands=['history'])
def send_history(message):
    try:
        token = message.text.split()[1]
        reply = get_token_history(token)
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "Please use: /history <token> (e.g., /history SOL)")

# Start the bot and Flask server
if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the alert thread
    start_alert_thread(bot)
    
    # Start the bot polling
    bot.polling()
