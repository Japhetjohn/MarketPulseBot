import telebot
from dotenv import load_dotenv
import os
import requests
from flask import Flask
from threading import Thread
import time
import schedule  # For scheduling tasks
from vybe_api import get_transfers
from telebot.types import ReplyKeyboardMarkup, KeyboardButton  # For reply keyboard
from datetime import datetime, timezone  # For date formatting and timezone for UTC

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
VYBE_API_KEY = os.getenv("VYBE_API_KEY")

def check_env_vars():
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not VYBE_API_KEY:
        missing.append("VYBE_API_KEY")
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}. Please check your .env file.")

# Initialize bot and Flask app
check_env_vars()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Store user alerts
user_alerts = {}

@app.route('/')
def home():
    return "CryptoPulse Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080, debug=False)

# Helper function to make API requests
def make_vybe_request(endpoint, params=None, method="GET"):
    url = f"https://api.vybenetwork.xyz{endpoint}"
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=params)
        else:
            response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": "We couldn't find the requested data. Please check your input and try again."}
    except requests.exceptions.RequestException:
        return {"error": "There was a problem connecting to the server. Please try again later."}

# Create a reply keyboard for commands
def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/pulse"), KeyboardButton("/whale"))
    keyboard.add(KeyboardButton("/holdings"), KeyboardButton("/transfers"))
    keyboard.add(KeyboardButton("/volume"), KeyboardButton("/history"))
    keyboard.add(KeyboardButton("/alert"), KeyboardButton("/help"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = (
        "🚀 *CryptoPulse Bot*\n\n"
        "*Available Commands:*\n"
        "• /pulse <address> - Quick wallet analysis\n"
        "• /whale <address> - Whale activity tracking\n"
        "• /holdings <address> - Portfolio overview\n"
        "• /transfers <address> - Recent transactions\n"
        "• /volume <token> - Token volume stats\n"
        "• /history <token> - Price trends\n"
        "• /alert <token> <condition> - Custom alerts\n\n"
        "🔍 Powered by [AlphaVybe](https://alphavybe.com)"
    )
    bot.reply_to(message, welcome_message, parse_mode="Markdown", disable_web_page_preview=True)
    bot.reply_to(message, welcome_message, reply_markup=create_keyboard())

@bot.message_handler(commands=['pulse'])
def send_wallet_analysis(message):
    try:
        wallet_address = message.text.split()[1]
        data = make_vybe_request(f"/account/token-balance/{wallet_address}")
        if "error" in data:
            bot.reply_to(message, data["error"])
        elif not data or len(data.get('data', [])) == 0:
            bot.reply_to(message, f"No data found for wallet: {wallet_address}")
        else:
            total_value = data.get('totalTokenValueUsd', '0')
            token_count = data.get('totalTokenCount', '0')
            bot.reply_to(
                message,
                f"📊 Wallet Analysis:\n"
                f"- Total Value: ${total_value}\n"
                f"- Total Tokens: {token_count}"
            )
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /pulse <wallet_address>")
    except Exception:
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['whale'])
def send_whale_analysis(message):
    try:
        wallet_address = message.text.split()[1].strip()
        print(f"Wallet Address for /whale: {wallet_address}")  # Debugging log
        params = {"ownerAddress": wallet_address}
        data = make_vybe_request("/account/known-accounts", params=params)
        print(f"API Response for /whale: {data}")  # Debugging log

        if "error" in data:
            bot.reply_to(message, f"Error: {data['error']}. Please check the wallet address and try again.")
        elif not data or len(data.get('accounts', [])) == 0:
            bot.reply_to(message, f"No whale activity found for wallet: {wallet_address}. It might not be tracked as a whale.")
        else:
            accounts = data.get('accounts', [])
            whale_info = "\n\n".join([
                f"🐋 **Whale Account**:\n"
                f"- **Name**: {account.get('name', 'N/A')}\n"
                f"- **Owner Address**: {account.get('ownerAddress', 'N/A')}\n"
                f"- **Labels**: {', '.join(account.get('labels', []))}\n"
                f"- **Date Added**: {account.get('dateAdded', 'N/A')}"
                for account in accounts
            ])
            bot.reply_to(message, f"🐋 **Whale Activity for Wallet `{wallet_address}`**:\n\n{whale_info}")
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /whale <wallet_address>")
    except Exception as e:
        print(f"Error in /whale command: {e}")  # Debugging log
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['holdings'])
def send_holdings(message):
    try:
        wallet_address = message.text.split()[1]
        data = make_vybe_request(f"/account/token-balance/{wallet_address}")
        if "error" in data:
            bot.reply_to(message, data["error"])
        elif not data or len(data.get('data', [])) == 0:
            bot.reply_to(message, f"No holdings found for wallet: {wallet_address}")
        else:
            holdings = "\n".join([
                f"- {token['name']} ({token['symbol']}): {token['amount']} tokens"
                for token in data.get('data', [])
            ])
            bot.reply_to(message, f"💰 Token Holdings:\n{holdings}")
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /holdings <wallet_address>")
    except Exception:
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['transfers'])
def send_transfers(message):
    try:
        wallet_address = message.text.split()[1].strip()
        # Correctly call the transfers endpoint with the wallet address
        data = make_vybe_request(f"/token/transfers", {"walletAddress": wallet_address})
        
        if "error" in data:
            bot.reply_to(message, f"🚫 Error: {data['error']}")
            return
            
        transfers = data.get("transfers", [])
        if not transfers:
            bot.reply_to(message, "No recent transfers found for this wallet.")
            return
            
        response = "🔄 *Recent Transfers*\n\n"
        for tx in transfers[:5]:  # Show only top 5 transfers
            amount = float(tx.get("amount", 0))
            value_usd = float(tx.get("valueUsd", 0))
            response += (
                f"💸 *Transfer*\n"
                f"Amount: {amount:,.2f} tokens\n"
                f"Value: ${value_usd:,.2f}\n"
                f"From: `{tx['senderAddress'][:8]}...`\n"
                f"To: `{tx['receiverAddress'][:8]}...`\n\n"
            )
        response += "\n🔍 View more details on [AlphaVybe](https://alphavybe.com/address/" + wallet_address + ")"
        
        bot.reply_to(message, response, parse_mode="Markdown", disable_web_page_preview=True)
        print(f"API Response for /transfers: {data}")  # Debugging log

    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /transfers <wallet_address>")
    except Exception as e:
        print(f"Error in /transfers command: {e}")  # Debugging log
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['volume'])
def send_token_volume(message):
    try:
        token = message.text.split()[1].strip()
        print(f"Token for /volume: {token}")  # Debugging log
        current_time = int(time.time())
        one_week_ago = current_time - (7 * 24 * 60 * 60)

        params = {
            "startTime": one_week_ago,
            "endTime": current_time,
            "interval": "1d",
            "limit": 7
        }
        data = make_vybe_request(f"/token/{token}/transfer-volume", params=params)
        print(f"API Response for /volume: {data}")  # Debugging log
        
        if "error" in data:
            bot.reply_to(message, f"Error: {data['error']}. Please check the token and try again.")
        elif not data or len(data.get('data', [])) == 0:
            bot.reply_to(message, f"No volume data found for token: {token}. It might not be supported.")
        else:
            volume_date = datetime.fromtimestamp(data["time"], tz=timezone.utc).strftime('%Y-%m-%d')
            volume_usd = float(data["volume"])
            response = (
                f"📊 Token Volume for `{token}`:\n\n"
                f"- Date: {volume_date}\n"
                f"  Volume: ${volume_usd:,.2f}\n\n"
                f"🔍 View more details on [AlphaVybe](https://alphavybe.com/token/{token})"
            )
            bot.reply_to(message, response, parse_mode="Markdown", disable_web_page_preview=True)
    except IndexError:
        bot.reply_to(message, "Please provide a token. Example: /volume <token>")
    except Exception as e:
        print(f"Error in /volume command: {e}")  # Debugging log
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['history'])
def send_token_history(message):
    try:
        token = message.text.split()[1].strip()
        current_time = int(time.time())
        one_month_ago = current_time - (30 * 24 * 60 * 60)

        params = {
            "mintAddress": token,
            "resolution": "1d",
            "timeStart": one_month_ago,
            "timeEnd": current_time,
            "limit": 10
        }
        data = make_vybe_request(f"/price/{token}/token-ohlcv", params=params)
        print(f"API Response for /history: {data}")  # Debugging log

        if "error" in data:
            bot.reply_to(message, f"Error: {data['error']}. Please check the token and try again.")
        elif not data or len(data.get('data', [])) == 0:
            bot.reply_to(message, f"No historical price data found for token: {token}. Please ensure the token is valid and has recorded transactions.")
        else:
            history = "\n".join([
                f"- Date: {datetime.fromtimestamp(entry.get('time', 0), tz=timezone.utc).strftime('%Y-%m-%d')} | Open: {entry['open']} | Close: {entry['close']} | High: {entry['high']} | Low: {entry['low']}"
                for entry in data.get('data', [])
            ])
            bot.reply_to(message, f"📈 Token Price History:\n{history}")
    except IndexError:
        bot.reply_to(message, "Please provide a token. Example: /history <token>")
    except Exception as e:
        print(f"Error in /history command: {e}")  # Debugging log
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Please provide a token and condition. Example: /alert USDC >1000")
            return
        token = parts[1].upper()
        condition = " ".join(parts[2:])
        chat_id = message.chat.id
        if chat_id not in user_alerts:
            user_alerts[chat_id] = []
        user_alerts[chat_id].append({"token": token, "condition": condition})
        bot.reply_to(message, f"✅ Alert set for {token} when {condition}.")
    except Exception:
        bot.reply_to(message, "Something went wrong. Please try again later.")

def check_alerts():
    for chat_id, alerts in user_alerts.items():
        for alert in alerts:
            token = alert["token"]
            condition = alert["condition"]
            data = make_vybe_request(f"/token/{token}/transfer-volume")
            if "error" in data or not data:
                continue
            for entry in data.get("data", []):
                volume = float(entry.get("volume", 0))
                if eval(f"{volume} {condition}"):
                    bot.send_message(chat_id, f"🚨 Alert Triggered for {token}:\nCondition: {condition}\nVolume: {volume}")
                    alerts.remove(alert)

# Schedule the alert checker to run every minute
schedule.every(1).minutes.do(check_alerts)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the bot and Flask server
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    print("Bot is starting...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(15)