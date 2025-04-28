import telebot
from dotenv import load_dotenv
import os
import requests
from flask import Flask
from threading import Thread
import time
import schedule
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timezone
import re

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

# Token symbol to mint address mapping
TOKEN_MAPPING = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "WETH": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
    "SRM": "SRMuApVNdxXekkYD7kqFN73JQGCZCFBZfzD61ZdWyR"
}

@app.route('/')
def home():
    return "CryptoPulse Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080, debug=False)

# Helper function to validate Solana address
def is_valid_solana_address(address):
    # Solana addresses are 43-44 characters, base58 (alphanumeric excluding 0, O, I, l)
    pattern = r'^[1-9A-HJ-NP-Za-km-z]{43,44}$'
    return bool(re.match(pattern, address))

# Helper function to resolve token input (symbol or address)
def resolve_token(token):
    token = token.upper()
    if token in TOKEN_MAPPING:
        return TOKEN_MAPPING[token]
    if is_valid_solana_address(token):
        return token
    return None

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
        data = response.json()
        print(f"API Response for {endpoint}: {data}")  # Debug log
        return data
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            error_msg = error_data.get('message', f"HTTP Error: {e.response.status_code}")
        except ValueError:
            error_msg = f"HTTP Error: {e.response.status_code}"
        print(f"API Error for {endpoint}: {error_msg}")  # Debug log
        return {"error": error_msg}
    except requests.exceptions.RequestException as e:
        print(f"Network Error for {endpoint}: {e}")  # Debug log
        return {"error": "Network error. Please try again later."}

# Create an inline keyboard for navigation
def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Pulse", callback_data="cmd_pulse"),
        InlineKeyboardButton("Whale", callback_data="cmd_whale")
    )
    keyboard.row(
        InlineKeyboardButton("Holdings", callback_data="cmd_holdings"),
        InlineKeyboardButton("Transfers", callback_data="cmd_transfers")
    )
    keyboard.row(
        InlineKeyboardButton("Volume", callback_data="cmd_volume"),
        InlineKeyboardButton("History", callback_data="cmd_history")
    )
    keyboard.row(
        InlineKeyboardButton("Alert", callback_data="cmd_alert")
    )
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
        "🔍 Powered by [Vybe Network](https://alpha.vybenetwork.com)"
    )
    bot.reply_to(message, welcome_message, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=create_inline_keyboard())

@bot.message_handler(commands=['pulse'])
def send_wallet_analysis(message):
    try:
        wallet_address = message.text.split()[1].strip()
        if not is_valid_solana_address(wallet_address):
            bot.reply_to(message, "Invalid Solana address. Please provide a valid address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Fetching wallet data...")
        data = make_vybe_request(f"/account/token-balance/{wallet_address}")
        if "error" in data:
            bot.edit_message_text(data["error"], chat_id=message.chat.id, message_id=sent_msg.message_id)
        elif not data or len(data.get('data', [])) == 0:
            bot.edit_message_text(f"No data found for wallet: {wallet_address}", chat_id=message.chat.id, message_id=sent_msg.message_id)
        else:
            total_value = data.get('totalTokenValueUsd', '0')
            token_count = data.get('totalTokenCount', '0')
            top_tokens = "\n".join([f"- {token['name']} ({token['symbol']}): {token['amount']} tokens" for token in data.get('data', [])[:3]])
            bot.edit_message_text(
                f"📊 *Wallet Analysis*:\n"
                f"- Total Value: ${float(total_value):,.2f}\n"
                f"- Total Tokens: {token_count}\n"
                f"- Top Tokens:\n{top_tokens}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/{wallet_address})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /pulse <wallet_address>")
    except Exception as e:
        print(f"Error in /pulse: {e}")
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['whale'])
def send_whale_analysis(message):
    try:
        wallet_address = message.text.split()[1].strip()
        if not is_valid_solana_address(wallet_address):
            bot.reply_to(message, "Invalid Solana address. Please provide a valid address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Checking whale activity...")
        params = {"ownerAddress": wallet_address}
        data = make_vybe_request("/account/known-accounts", params=params)
        if "error" in data:
            bot.edit_message_text(f"Error: {data['error']}. This wallet may not be a known whale.", chat_id=message.chat.id, message_id=sent_msg.message_id)
        elif not data or len(data.get('accounts', [])) == 0:
            bot.edit_message_text(
                f"No whale activity found for wallet: {wallet_address}. Try a known whale address.\n\n"
                f"🔍 Explore tokens at [Vybe Network](https://alpha.vybenetwork.com)",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        else:
            accounts = data.get('accounts', [])
            whale_info = "\n\n".join([
                f"🐋 *Whale Account*:\n"
                f"- Name: {account.get('name', 'N/A')}\n"
                f"- Owner Address: {account.get('ownerAddress', 'N/A')}\n"
                f"- Labels: {', '.join(account.get('labels', [])) or 'None'}\n"
                f"- Date Added: {account.get('dateAdded', 'N/A')}"
                for account in accounts
            ])
            bot.edit_message_text(
                f"🐋 *Whale Activity for `{wallet_address}`*:\n\n{whale_info}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/{wallet_address})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /whale <wallet_address>")
    except Exception as e:
        print(f"Error in /whale: {e}")
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['holdings'])
def send_holdings(message):
    try:
        wallet_address = message.text.split()[1].strip()
        if not is_valid_solana_address(wallet_address):
            bot.reply_to(message, "Invalid Solana address. Please provide a valid address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Fetching holdings...")
        data = make_vybe_request(f"/account/token-balance/{wallet_address}")
        if "error" in data:
            bot.edit_message_text(data["error"], chat_id=message.chat.id, message_id=sent_msg.message_id)
        elif not data or len(data.get('data', [])) == 0:
            bot.edit_message_text(f"No holdings found for wallet: {wallet_address}", chat_id=message.chat.id, message_id=sent_msg.message_id)
        else:
            holdings = "\n".join([
                f"- {token['name']} ({token['symbol']}): {float(token['amount']):,.2f} tokens"
                for token in data.get('data', [])
            ])
            bot.edit_message_text(
                f"💰 *Token Holdings*:\n{holdings}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/{wallet_address})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /holdings <wallet_address>")
    except Exception as e:
        print(f"Error in /holdings: {e}")
        bot.reply_to(message, "Something went wrong. Please try again later.")

@bot.message_handler(commands=['transfers'])
def send_transfers(message):
    try:
        wallet_address = message.text.split()[1].strip()
        if not is_valid_solana_address(wallet_address):
            bot.reply_to(message, "Invalid Solana address. Please provide a valid address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Fetching transfers...")
        params = {"walletAddress": wallet_address, "limit": 5}
        data = make_vybe_request("/token/transfers", params=params)
        if "error" in data:
            bot.edit_message_text(f"Error: {data['error']}", chat_id=message.chat.id, message_id=sent_msg.message_id)
        elif not data or len(data.get('transfers', [])) == 0:
            bot.edit_message_text(f"No recent transfers found for wallet: {wallet_address}", chat_id=message.chat.id, message_id=sent_msg.message_id)
        else:
            transfers = "\n\n".join([
                f"💸 *Transfer*:\n"
                f"- Token: {transfer.get('mintAddress', 'Unknown')}\n"
                f"- Amount: {float(transfer.get('amount', 0)):.2f} tokens\n"
                f"- Value: ${float(transfer.get('valueUsd', 0)):.2f}\n"
                f"- From: `{transfer.get('senderAddress', 'Unknown')[:8]}...`\n"
                f"- To: `{transfer.get('receiverAddress', 'Unknown')[:8]}...`\n"
                f"- Date: {datetime.fromtimestamp(transfer.get('blockTime', 0), tz=timezone.utc).strftime('%b %d, %Y %I:%M %p')}"
                for transfer in data.get('transfers', [])
            ])
            bot.edit_message_text(
                f"🔄 *Recent Transfers for `{wallet_address}`*:\n\n{transfers}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/{wallet_address})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a wallet address. Example: /transfers <wallet_address>")
    except Exception as e:
        print(f"Error in /transfers: {e}")
        bot.edit_message_text("Something went wrong. Please try again later.", chat_id=message.chat.id, message_id=sent_msg.message_id)

@bot.message_handler(commands=['volume'])
def send_token_volume(message):
    try:
        token_input = message.text.split()[1].strip()
        token = resolve_token(token_input)
        if not token:
            bot.reply_to(message, "Invalid token. Use a token symbol (e.g., SOL, USDC) or a valid Solana mint address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Fetching volume...")
        current_time = int(time.time())
        one_week_ago = current_time - (7 * 24 * 60 * 60)
        params = {"startTime": one_week_ago, "endTime": current_time}
        data = make_vybe_request(f"/token/{token}/transfer-volume", params=params)
        if "error" in data:
            bot.edit_message_text(
                f"Error: {data['error']}. Ensure the token is supported by Vybe Network.",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id
            )
        elif not data or 'data' not in data or len(data['data']) == 0:
            bot.edit_message_text(
                f"No volume data found for token: {token_input}. Try a different token like SOL.",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id
            )
        else:
            total_volume = sum(float(entry.get("volume", 0)) for entry in data["data"])
            bot.edit_message_text(
                f"📊 *Token Volume for `{token_input}`*:\n\n"
                f"Total Volume (7 days): ${total_volume:,.2f}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/{token})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a token. Example: /volume SOL or /volume So11111111111111111111111111111111111111112")
    except Exception as e:
        print(f"Error in /volume: {e}")
        bot.edit_message_text("Something went wrong. Please try again later.", chat_id=message.chat.id, message_id=sent_msg.message_id)

@bot.message_handler(commands=['history'])
def send_token_history(message):
    try:
        token_input = message.text.split()[1].strip()
        token = resolve_token(token_input)
        if not token:
            bot.reply_to(message, "Invalid token. Use a token symbol (e.g., SOL, USDC) or a valid Solana mint address (43-44 characters).")
            return
        sent_msg = bot.reply_to(message, "Fetching price history...")
        current_time = int(time.time())
        one_week_ago = current_time - (7 * 24 * 60 * 60)
        params = {"resolution": "1d", "timeStart": one_week_ago, "timeEnd": current_time, "limit": 5}
        data = make_vybe_request(f"/price/{token}/token-ohlcv", params=params)
        if "error" in data:
            bot.edit_message_text(f"Error: {data['error']}. Ensure the token is supported by Vybe Network.", chat_id=message.chat.id, message_id=sent_msg.message_id)
        elif not data or len(data.get('data', [])) == 0:
            bot.edit_message_text(f"No price history found for token: {token_input}. Try a different token like SOL.", chat_id=message.chat.id, message_id=sent_msg.message_id)
        else:
            history = "\n".join([
                f"- {datetime.fromtimestamp(entry.get('time', 0), tz=timezone.utc).strftime('%Y-%m-%d')}: "
                f"Open: ${float(entry['open']):.2f}, Close: ${float(entry['close']):.2f}"
                for entry in data.get('data', [])[:5]
            ])
            bot.edit_message_text(
                f"📈 *Price History for `{token_input}`*:\n\n{history}\n\n"
                f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/{token})",
                chat_id=message.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    except IndexError:
        bot.reply_to(message, "Please provide a token. Example: /history SOL or /history So11111111111111111111111111111111111111112")
    except Exception as e:
        print(f"Error in /history: {e}")
        bot.edit_message_text("Something went wrong. Please try again later.", chat_id=message.chat.id, message_id=sent_msg.message_id)

@bot.message_handler(commands=['alert'])
def set_alert(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Please provide a token and condition. Example: /alert USDC >1000")
            return
        token_input = parts[1].strip()
        token = resolve_token(token_input)
        if not token:
            bot.reply_to(message, "Invalid token. Use a token symbol (e.g., SOL, USDC) or a valid Solana mint address (43-44 characters).")
            return
        condition = " ".join(parts[2:])
        if not any(op in condition for op in [">", "<", "=="]):
            bot.reply_to(message, "Condition must include >, <, or ==. Example: /alert USDC >1000")
            return
        chat_id = message.chat.id
        if chat_id not in user_alerts:
            user_alerts[chat_id] = []
        user_alerts[chat_id].append({"token": token, "condition": condition, "token_input": token_input})
        bot.reply_to(message, f"✅ Alert set for {token_input} when {condition}.", reply_markup=create_inline_keyboard())
    except Exception as e:
        print(f"Error in /alert: {e}")
        bot.reply_to(message, "Something went wrong. Please try again later.")

def check_alerts():
    for chat_id, alerts in user_alerts.items():
        for alert in alerts[:]:  # Copy to avoid modification issues
            token = alert["token"]
            token_input = alert["token_input"]
            condition = alert["condition"]
            current_time = int(time.time())
            one_day_ago = current_time - (24 * 60 * 60)
            params = {"startTime": one_day_ago, "endTime": current_time, "interval": "1h"}
            data = make_vybe_request(f"/token/{token}/transfer-volume", params=params)
            if "error" in data or not data or 'data' not in data:
                continue
            for entry in data.get("data", []):
                volume = float(entry.get("volume", 0))
                op, value = condition.split()
                value = float(value)
                if (op == ">" and volume > value) or (op == "<" and volume < value) or (op == "==" and abs(volume - value) < 0.01):
                    bot.send_message(
                        chat_id,
                        f"🚨 *Alert Triggered for {token_input}*:\n"
                        f"Condition: Volume {op} ${value:,.2f}\n"
                        f"Current Volume: ${volume:,.2f}\n\n"
                        f"🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/{token})",
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    alerts.remove(alert)
                    break

schedule.every(1).minutes.do(check_alerts)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Inline keyboard callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cmd = call.data.split("_")[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"Please provide an address or token for /{cmd}. Example: /{cmd} <address>")

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