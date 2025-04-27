import os
import requests
from dotenv import load_dotenv

load_dotenv()
VYBE_API_KEY = os.getenv("VYBE_API_KEY")
BASE_URL = "https://api.vybenetwork.xyz/v1"

def make_request(endpoint, params=None):
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return {"error": "Unable to fetch data. Please try again later."}

def get_wallet_analysis(address):
    data = make_request(f"/account/{address}/overview")
    if "error" in data:
        return f"Error analyzing wallet: {data['error']}"
    try:
        holdings = data.get("holdings", [])
        transfers = data.get("transfers", [])
        momentum = data.get("momentumScore", 0)

        holdings_str = "\n".join([f"• {token['amount']} {token['symbol']} (${token['usdValue']:,.2f})" for token in holdings[:5]]) if holdings else "No holdings found"
        transfers_str = "\n".join([f"• {('Sent' if tx['direction'] == 'out' else 'Received')} {tx['amount']} {tx['symbol']} (${tx['usdValue']:,.2f})" for tx in transfers[:3]]) if transfers else "No recent transfers"

        response = (
            f"🔍 *WALLET ANALYSIS REPORT*\n"
            f"Address: `{address[:4]}...{address[-4:]}`\n\n"
            f"📈 *Performance Metrics*\n"
            f"• Momentum Score: {momentum}/100\n\n"
            f"💼 *Portfolio Overview*\n"
            f"{holdings_str}\n\n"
            f"📊 *Recent Transactions*\n"
            f"{transfers_str}\n\n"
            f"🔗 *Detailed Analytics*\n"
            f"View comprehensive insights at:\n"
            f"https://alphavybe.com/address/{address}\n\n"
            f"_Powered by AlphaVybe_"
        )
        return response
    except Exception as e:
        return f"Error formatting wallet analysis: {str(e)}"


def get_whale_info(address):
    data = make_request(f"/account/{address}/whale-status")
    if "error" in data:
        return f"Error analyzing whale activity: {data['error']}"
    try:
        total_value = data.get("totalValue", 0)
        is_whale = data.get("isWhale", False)
        whale_moves = data.get("highImpactMoves", [])
        response = (
            f"🐋 Whale Analysis for {address[:4]}...{address[-4:]}\n\n"
            f"Portfolio Value: ${total_value:,.2f}\n"
            f"Whale Status: {'🔵 Active Whale' if is_whale else '⚪ Not a whale'}\n\n"
        )
        if whale_moves:
            response += "Recent High-Impact Moves:\n" + "\n".join([f"• Moved {tx['amount']} {tx['symbol']} (${float(tx['usdValue']):,.2f})" for tx in whale_moves])
        else:
            response += "No recent high-impact moves detected."
        return response
    except Exception as e:
        return f"Error formatting whale analysis: {str(e)}"


def get_token_holdings(address):
    data = make_request(f"/account/{address}/token-balance")
    if "error" in data:
        return data["error"]
    return "\n".join([f"• {token['amount']} {token['symbol']} (${token['usdValue']:,.2f})" for token in data[:5]]) if data else "No holdings found"


def get_transfers(address):
    data = make_request(f"/account/{address}/transfers", {"limit": 3})
    if "error" in data:
        return {"error": data["error"]}
    transfers = data.get("transfers", [])
    if not transfers:
        return {"transfers": []}
    return {"transfers": transfers}


def get_token_volume(token):
    data = make_request(f"/token/{token}/transfer-volume", {
        "interval": "1d",
        "limit": 1
    })
    if "error" in data:
        return {"error": data["error"]}
    if not data or "data" not in data:
        return {"error": "No volume data available"}
    
    latest_volume = data["data"][0] if data["data"] else {}
    return {
        "volume": latest_volume.get("volumeUsd", 0),
        "time": latest_volume.get("timeBucketStart", 0)
    }


def get_token_history(token):
    data = make_request(f"/token/{token}/price-history", {"interval": "1d", "limit": 7})
    if "error" in data:
        return data["error"]
    try:
        price_1d = data[0].get("price", "N/A")
        price_7d = data[-1].get("price", "N/A") if len(data) >=7 else "N/A"
        return f"{token} price 1 day ago: {price_1d}, 7 days ago: {price_7d}"
    except (IndexError, TypeError) as e:
        return f"Error formatting token history: {str(e)}"

# Removed functions as they are replaced by the improved API calls