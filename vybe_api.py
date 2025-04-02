import requests
from dotenv import load_dotenv
import os

load_dotenv()
VYBE_API_KEY = os.getenv("VYBE_API_KEY") or "placeholder_key"  # Replace when you get it

def get_token_pulse(token):
    url = f"https://api.vybe.network/token/{token}"  # Placeholder—update from docs
    headers = {"Authorization": f"Bearer {VYBE_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        volume = data.get("volume", "N/A")  # Adjust per API docs
        return f"{token}: Volume {volume}. More at AlphaVybe: https://alphavybe.com"
    except Exception as e:
        return f"Error fetching {token}: {str(e)}"

def get_token_history(token):
    url = f"https://api.vybe.network/token/{token}/history"  # Placeholder
    headers = {"Authorization": f"Bearer {VYBE_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        peak = data.get("peak_volume", "N/A")  # Adjust per API
        return f"{token} peak volume yesterday: {peak}"
    except Exception as e:
        return f"Error fetching {token} history: {str(e)}"
