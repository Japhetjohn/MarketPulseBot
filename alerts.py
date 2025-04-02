import threading
import time
from vybe_api import get_token_pulse

alerts = {}  # {chat_id: {"token": "SOL", "condition": "volume>50"}}

def check_alerts(bot):
    while True:
        for chat_id, alert in list(alerts.items()):
            token = alert["token"]
            condition = alert["condition"]
            data = get_token_pulse(token)
            try:
                volume = float(data.split()[2])  # Parse volume from reply
                threshold = float(condition.split(">")[1])
                if volume > threshold:
                    bot.send_message(chat_id, f"Alert triggered: {data}")
                    del alerts[chat_id]
            except (IndexError, ValueError):
                pass  # Skip if parsing fails
        time.sleep(60)  # Check every minute

def start_alert_thread(bot):
    thread = threading.Thread(target=check_alerts, args=(bot,))
    thread.daemon = True
    thread.start()  # Ensure this line is indented correctly
