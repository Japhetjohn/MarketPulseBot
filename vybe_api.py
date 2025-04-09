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

def get_wallet_pulse(address):
    """Get comprehensive wallet analysis"""
    try:
        holdings = get_token_holdings(address)
        transfers = get_recent_transfers(address)
        momentum = calculate_momentum_score(transfers)
        
        response = (
            f"📊 Wallet Pulse Report for {address[:4]}...{address[-4:]}\n\n"
            f"🏆 Momentum Score: {momentum}/100\n\n"
            f"💰 Key Holdings:\n{holdings}\n\n"
            f"🔄 Recent Activity:\n{transfers}\n\n"
            f"View more at: https://alphavybe.com/address/{address}"
        )
        return response
    except Exception as e:
        return f"Error analyzing wallet: {str(e)}"

def get_token_holdings(address):
    """Get token balances for a wallet"""
    url = f"{BASE_URL}/account/token-balance/{address}"
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if not data:
            return "No holdings found"
        holdings = []
        for token in data[:5]:  # Show top 5 holdings
            holdings.append(f"• {token['amount']} {token['symbol']} (${token['usdValue']:,.2f})")
        return "\n".join(holdings)
    except:
        return "Unable to fetch holdings"

def get_recent_transfers(address):
    """Get recent transfer history"""
    url = f"{BASE_URL}/token/transfers"
    params = {
        "sourceOwner": address,
        "destOwner": address,
        "limit": 3
    }
    headers = {"X-API-Key": VYBE_API_KEY}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        if not data:
            return "No recent transfers"
        transfers = []
        for tx in data:
            direction = "Sent" if tx["sourceOwner"] == address else "Received"
            transfers.append(f"• {direction} {tx['amount']} {tx['symbol']} (${tx['usdValue']:,.2f})")
        return "\n".join(transfers)
    except:
        return "Unable to fetch transfers"

def calculate_momentum_score(transfers):
    """Calculate wallet momentum score based on volume, frequency, and recency"""
    try:
        # Volume Factor
        total_usd_volume = sum(float(tx['usdValue']) for tx in transfers)
        dynamic_cap = max(100, min(50000, total_usd_volume * 3))
        volume_factor = min(100, (total_usd_volume / dynamic_cap) * 100)
        
        # Frequency Factor
        frequency_factor = (len(transfers) / 3) * 100
        
        # Recency Factor
        current_time = time.time()
        most_recent = max((tx.get('timestamp', 0) for tx in transfers), default=0)
        if current_time - most_recent < 3600:  # Within last hour
            recency_factor = 100
        elif current_time - most_recent < 86400:  # Within last 24 hours
            recency_factor = 50
        else:
            recency_factor = 0
            
        # Final Score
        final_score = (volume_factor + frequency_factor + recency_factor) / 3
        return int(final_score)
    except Exception as e:
        print(f"Error calculating momentum score: {e}")
        return 0

def get_token_pulse(token):
    if not VYBE_API_KEY:
        return "Error: API key not configured. Please contact admin."
    
    token = token.upper()
    mint_address = TOKEN_MINTS.get(token, token)
    url = f"{BASE_URL}/token/{mint_address}"
    headers = {"X-API-Key": VYBE_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return f"No data available for {token}. Please verify the token symbol."
            
        volume = data.get("usdValueVolume24h", 0)
        if isinstance(volume, str):
            volume = float(volume.replace('$', '').replace(',', ''))
        
        return f"{token}: Volume ${volume:,.2f}. More at AlphaVybe: https://alphavybe.com"
    except requests.RequestException as e:
        print(f"API Error for {token}: {str(e)}")
        return f"Unable to fetch data for {token}. Please try again later."

def get_whale_analysis(address):
    """Analyze whale activity for a wallet"""
    try:
        holdings = get_token_holdings(address)
        transfers = get_recent_transfers(address)
        
        # Calculate total USD value
        total_value = sum(float(token['usdValue']) for token in holdings)
        is_whale = total_value > 100000
        
        # Find high-impact moves
        whale_moves = []
        for tx in transfers:
            if float(tx['usdValue']) > 50000:
                whale_moves.append(f"• Moved {tx['amount']} {tx['symbol']} (${float(tx['usdValue']):,.2f})")
        
        response = (
            f"🐋 Whale Analysis for {address[:4]}...{address[-4:]}\n\n"
            f"Portfolio Value: ${total_value:,.2f}\n"
            f"Whale Status: {'🔵 Active Whale' if is_whale else '⚪ Not a whale'}\n\n"
        )
        
        if whale_moves:
            response += "Recent High-Impact Moves:\n" + "\n".join(whale_moves)
        else:
            response += "No recent high-impact moves detected."
            
        return response
    except Exception as e:
        return f"Error analyzing whale activity: {str(e)}"

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
