import threading
import time
import re
from vybe_api import get_token_pulse, get_token_holdings, get_recent_transfers

alerts = {}
whale_cache = {}

def check_alerts(bot):
    while True:
        for chat_id, alert in list(alerts.items()):
            token = alert["token"]
            condition = alert["condition"]
            data = get_token_pulse(token)
            try:
                volume_str = data.split("Volume $")[1].split(".")[0]
                volume = float(volume_str.replace(',', ''))
                threshold = float(condition.split(">")[1])
                if volume > threshold:
                    bot.send_message(chat_id, f"Alert triggered: {data}")
                    del alerts[chat_id]
            except (IndexError, ValueError) as e:
                bot.send_message(chat_id, f"Error with alert for {token}: {str(e)}")
                del alerts[chat_id]
        time.sleep(60)

def handle_whale_command(bot, update, args):
    address = args[0] if args else None
    if not address:
        bot.send_message(update.message.chat_id, "Please provide a wallet address.")
        return

    try:
        balance_data = get_token_balance(address)
        total_usd_value = sum(token["usdValue"] for token in balance_data["tokens"])

        whale_status = "detected" if total_usd_value > 100000 else "not detected"
        message = f"Whale status for {address}: {whale_status}"

        transfers = get_token_transfers(address)
        for transfer in transfers["transfers"]:
            if transfer["usdValue"] > 50000:
                message += f"\nLarge transfer detected: {transfer['amount']} {transfer['mintAddress']} (${transfer['usdValue']})"

        bot.send_message(update.message.chat_id, message)


    except Exception as e:
        bot.send_message(update.message.chat_id, f"Error processing whale command: {e}")


def handle_command(bot, update):
    text = update.message.text.lower()
    if text.startswith("/pulse"):
        args = text[6:].strip().split()
        if args:
            handle_whale_command(bot, update, args)
        else:
             bot.send_message(update.message.chat_id,"Usage: /pulse <wallet_address>")
    elif text.startswith("/whale"):
        args = text[6:].strip().split()
        handle_whale_command(bot, update, args)
    elif text.startswith("/setalert"):
        try:
            parts = text[9:].strip().split()
            token = parts[0].upper()
            condition = parts[1]  #e.g., ">1000"
            alerts[update.message.chat_id] = {"token": token, "condition": condition}
            bot.send_message(update.message.chat_id, f"Alert set for {token}: {condition}")
        except (IndexError, ValueError):
            bot.send_message(update.message.chat_id, "Invalid alert format. Use: /setalert <token> <condition> (e.g., /setalert SOL >1000)")
    elif text.startswith("/clear"):
            if update.message.chat_id in alerts:
                del alerts[update.message.chat_id]
                bot.send_message(update.message.chat_id, "Alert cleared")
            else:
                bot.send_message(update.message.chat_id, "No active alert for this chat")

    else:
        bot.send_message(update.message.chat_id, "Invalid command. Use /setalert, /pulse, /whale or /clear")


def start_alert_thread(bot):
    thread = threading.Thread(target=check_alerts, args=(bot,))
    thread.daemon = True
    thread.start()

#Example usage (replace with your bot instance)
#bot.message_handler(func=lambda message: message.text.startswith('/'))(handle_command)