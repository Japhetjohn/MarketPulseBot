
import telebot
from dotenv import load_dotenv
import os
from vybe_api import (get_token_pulse, get_token_history, get_wallet_pulse, 
                     get_token_holdings, get_recent_transfers, get_whale_analysis)
from alerts import start_alert_thread, alerts
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and Flask app
bot = telebot.TeleBot(BOT_TOKEN, case_sensitive=False)  # Disable case sensitivity
app = Flask(__name__)

@app.route('/')
def home():
    return "CryptoPulse Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080, debug=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "🚀 Welcome to CryptoPulse Bot! 🚀\n\n"
        "Available Commands:\n"
        "• /pulse <wallet_address> - Get wallet analysis\n"
        "• /whale <address> - Whale activity analysis\n"
        "• /wallet <address> - Full wallet analysis\n"
        "• /holdings <address> - Token holdings\n"
        "• /transfers <address> - Recent transfers\n"
        "• /alert <token> <condition> - Set volume alerts\n"
        "• /history <token> - Past prices\n"
        "• /volume <token> - Token volume info\n"
        "• /help - Show this message\n\n"
        "Example: /pulse 5eXhL2f2..."
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = (
        "📋 CryptoPulse Bot Commands:\n\n"
        "🔍 Wallet Analysis:\n"
        "• /pulse <address> - Quick wallet analysis\n"
        "• /whale <address> - Track whale activity\n"
        "• /wallet <address> - Detailed wallet info\n"
        "• /holdings <address> - Token holdings\n"
        "• /transfers <address> - Recent transfers\n\n"
        "📊 Token Data:\n"
        "• /volume <token> - Token volume (e.g., /volume SOL)\n"
        "• /history <token> - Price history\n"
        "• /alert <token> <condition> - Set alerts (e.g., /alert SOL volume>50)\n\n"
        "❓ /help - Show this message"
    )
    bot.reply_to(message, help_message)

@bot.message_handler(commands=['pulse', 'wallet'])
def send_wallet_analysis(message):
    try:
        wallet_address = message.text.split()[1]
        if len(wallet_address) != 44:
            bot.reply_to(message, "❌ Invalid Solana wallet address format.")
            return
        reply = get_wallet_pulse(wallet_address)
        bot.reply_to(message, reply)
    except IndexError:
        bot.reply_to(message, "Please use: /pulse <wallet_address>")

@bot.message_handler(commands=['whale'])
def send_whale_analysis(message):
    try:
        wallet_address = message.text.split()[1]
        if len(wallet_address) != 44:
            bot.reply_to(message, "❌ Invalid Solana wallet address format.")
            return
        reply = get_whale_analysis(wallet_address)
        bot.reply_to(message, reply)
    except IndexError:
        bot.reply_to(message, "Please use: /whale <wallet_address>")

@bot.message_handler(commands=['volume'])
def send_token_volume(message):
    try:
        token = message.text.split()[1].upper()
        reply = get_token_pulse(token)
        bot.reply_to(message, reply)
    except IndexError:
        bot.reply_to(message, "Please use: /volume <token>")

@bot.message_handler(commands=['holdings'])
def send_holdings(message):
    try:
        wallet_address = message.text.split()[1]
        if len(wallet_address) != 44:
            bot.reply_to(message, "❌ Invalid Solana wallet address format.")
            return
        holdings = get_token_holdings(wallet_address)
        bot.reply_to(message, f"💰 Holdings for {wallet_address[:4]}...{wallet_address[-4:]}:\n\n{holdings}")
    except IndexError:
        bot.reply_to(message, "Please use: /holdings <wallet_address>")

@bot.message_handler(commands=['transfers'])
def send_transfers(message):
    try:
        wallet_address = message.text.split()[1]
        if len(wallet_address) != 44:
            bot.reply_to(message, "❌ Invalid Solana wallet address format.")
            return
        transfers = get_recent_transfers(wallet_address)
        bot.reply_to(message, f"🔄 Recent transfers for {wallet_address[:4]}...{wallet_address[-4:]}:\n\n{transfers}")
    except IndexError:
        bot.reply_to(message, "Please use: /transfers <wallet_address>")

@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        parts = message.text.split(maxsplit=2)
        token, condition = parts[1].upper(), parts[2]
        alerts[message.chat.id] = {"token": token, "condition": condition}
        bot.reply_to(message, f"🔔 Alert set for {token}: {condition}")
    except:
        bot.reply_to(message, "Please use: /alert <token> <condition> (e.g., /alert SOL volume>50)")

@bot.message_handler(commands=['history'])
def send_history(message):
    try:
        token = message.text.split()[1].upper()
        reply = get_token_history(token)
        bot.reply_to(message, f"📈 {reply}")
    except:
        bot.reply_to(message, "Please use: /history <token> (e.g., /history SOL)")

# Start the bot and Flask server
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    start_alert_thread(bot)
    
    print(f"Bot @{bot.get_me().username} is starting...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(15)
