
# CryptoPulse Bot

A comprehensive Telegram bot for analyzing Solana wallets and tracking whale activity using Vybe APIs.

## Features

### Wallet Analysis
- **/pulse <wallet_address>**: Get comprehensive wallet analysis
- **/whale <address>**: Track whale activity and high-impact moves
- **/wallet <address>**: Detailed wallet information
- **/holdings <address>**: Token holdings with USD values
- **/transfers <address>**: Recent transfer history
- **/volume <token>**: Token volume information
- **/history <token>**: Price history
- **/alert <token> <condition>**: Set volume alerts

### Whale Tracking
- Identifies wallets with >$100,000 in tokens
- Tracks transfers exceeding $50,000
- Monitors similar whale activity
- Cross-wallet pattern detection

## Setup Instructions

1. Configure environment variables in Replit Secrets:
   - BOT_TOKEN (Telegram Bot Token)
   - VYBE_API_KEY (Vybe Network API Key)

2. Run the bot:
   ```bash
   python bot.py
   ```

## Usage Examples

```
/pulse 5eXh...2f2f   # Get wallet analysis
/whale 5eXh...2f2f   # Track whale activity
/alert SOL volume>50 # Set volume alert
```

Example output:
```
🐋 Whale Analysis for 5eXh...2f2f

Portfolio Value: $150,000
Whale Status: 🔵 Active Whale

Recent High-Impact Moves:
• Moved 1000 SOL ($50,000)
• Received 100K USDC ($100,000)
```

## Deployment Notes
- Bot runs on Replit's free tier
- Uses Flask server for uptime monitoring
- Configure Always On for 24/7 operation
