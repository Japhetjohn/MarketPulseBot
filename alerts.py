import threading
import time
from vybe_api import get_token_pulse

alerts = {}

def check_alerts(bot):
    while True:
        for chat_id, alert in list(alerts.items()):
            token = alert["token"]
            condition = alert["condition"]
            data = get_token_pulse(token)
            try:
                volume_part = data.split()[2]
                if "(dummy" in data:
                    volume_part = volume_part.rstrip("(dummy")
                if volume_part == "N/A":
                    raise ValueError("Volume data not available")
                # Remove any trailing punctuation (e.g., "1628519594238.5205.")
                volume_part = volume_part.rstrip(".")
                volume = float(volume_part)
                threshold = float(condition.split(">")[1])
                if volume > threshold:
                    bot.send_message(chat_id, f"Alert triggered: {data}")
                    del alerts[chat_id]
            except (IndexError, ValueError) as e:
                bot.send_message(chat_id, f"Error with alert for {token}: {str(e)}")
                del alerts[chat_id]
        time.sleep(60)

def start_alert_thread(bot):
    thread = threading.Thread(target=check_alerts, args=(bot,))
    thread.daemon = True
    thread.start()
