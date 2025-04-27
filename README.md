
# 🚀 CryptoPulse Bot

A professional-grade Telegram bot providing real-time crypto insights powered by the Vybe API. Get instant access to wallet analytics, whale tracking, and token metrics with seamless integration to AlphaVybe's comprehensive analytics platform.

## 🎯 Features

### Core Analytics
- **📊 Wallet Analysis** (`/pulse <wallet_address>`)
  - Portfolio valuation
  - Token holdings breakdown
  - Transaction history
  - Momentum scoring
  - Direct link to AlphaVybe's detailed analysis

- **🐋 Whale Tracking** (`/whale <wallet_address>`)
  - Real-time whale activity monitoring
  - Large transaction alerts
  - Portfolio value assessment
  - Whale status classification

- **💰 Token Holdings** (`/holdings <wallet_address>`)
  - Complete token portfolio
  - USD valuations
  - Token distribution analysis
  - Historical balance changes

### Market Intelligence
- **🔄 Transfer Analysis** (`/transfers <wallet_address>`)
  - Recent transaction history
  - USD value tracking
  - Transaction categorization
  - Pattern identification

- **📈 Volume Tracking** (`/volume <token>`)
  - 7-day volume trends
  - Market activity analysis
  - Volume spike detection
  - Comparative metrics

- **📜 Price History** (`/history <token>`)
  - Historical price data
  - Trend analysis
  - Key price levels
  - Time-based comparisons

### Advanced Features
- **⏰ Custom Alerts** (`/alert <token> <condition>`)
  - Volume-based alerts
  - Price threshold notifications
  - Whale movement alerts
  - Example: `/alert USDC >1000000`

## 🛠️ Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/CryptoPulseBot.git
   cd CryptoPulseBot
   ```

2. **Environment Setup**
   Create a `.env` file with:
   ```
   BOT_TOKEN=your_telegram_bot_token
   VYBE_API_KEY=your_vybe_api_key
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Bot**
   ```bash
   python bot.py
   ```

## 📊 Example Metrics

### Wallet Analysis Example
```
🔍 WALLET ANALYSIS REPORT
Address: `7x4F...8j2K`

📈 Performance Metrics
• Momentum Score: 85/100

💼 Portfolio Overview
• 1000 USDC ($1,000.00)
• 50 SOL ($3,500.00)
• 10000 BONK ($100.00)

📊 Recent Transactions
• Received 500 USDC ($500.00)
• Sent 10 SOL ($700.00)
```

### Volume Analysis Example
```
📊 TOKEN VOLUME REPORT: USDC
• 24h Volume: $5.2M
• 7d Average: $4.8M
• Trend: +8.3%
```

## 🔐 Security

- Secure API key handling
- Rate limiting implementation
- Error handling and validation
- No storage of sensitive data

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines and submit pull requests.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
