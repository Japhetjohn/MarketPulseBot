import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
VYBE_API_KEY = os.getenv("VYBE_API_KEY")

BASE_URL = "https://api.vybenetwork.xyz"

# Map token symbols to mint addresses
TOKEN_MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
}

def get_token_pulse(token):
    mint_address = TOKEN_MINTS.get(token.upper(), token)
    url = f"{BASE_URL}/token/{mint_address}"
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("Pulse Response:", data)
        volume = data.get("usdValueVolume24h", "N/A")
        return f"{token}: Volume {volume}. More at AlphaVybe: https://alphavybe.com"
    except requests.RequestException as e:
        print("Pulse Error:", str(e))
        return f"{token}: Volume 150 (dummy data). More at AlphaVybe: https://alphavybe.com"

def get_token_history(token):
    mint_address = TOKEN_MINTS.get(token.upper(), token)
    url = f"{BASE_URL}/token/{mint_address}"
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("History Response:", data)
        price_1d = data.get("price1d", "N/A")
        price_7d = data.get("price7d", "N/A")
        return f"{token} price 1 day ago: {price_1d}, 7 days ago: {price_7d}"
    except requests.RequestException as e:
        print("History Error:", str(e))
        return f"{token} price 1 day ago: 200, 7 days ago: 190 (dummy data)"
