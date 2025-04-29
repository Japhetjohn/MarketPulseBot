# MarketPulseBot

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

MarketPulseBot is a Telegram bot for the Vybe Telegram Bot Challenge, delivering real-time Solana blockchain analytics using Vybe Network APIs. It provides wallet analysis, whale tracking, token transfers, volume stats, price trends, and custom alerts, with a user-friendly inline keyboard and robust error handling. The project now includes a web frontend interface for enhanced user interaction. Hosted on Render for 24/7 availability, it's open-source (MIT) and designed for traders, analysts, and Solana enthusiasts.

---

## Table of Contents

- [Features](#features)
- [Metrics Provided](#metrics-provided)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Vybe API Integration](#vybe-api-integration)
- [Why MarketPulseBot?](#why-marketpulsebot)
- [Contributing](#contributing)
- [License](#license)

---

## Features

MarketPulseBot offers the following features:

### Telegram Bot Commands

- `/pulse <address>`: Quick wallet analysis (total value, token count, top tokens).
- `/whale <address>`: Tracks activity of known whale accounts.
- `/holdings <address>`: Detailed portfolio overview (token names, symbols, amounts).
- `/transfers <address>`: Recent token transfer transactions (amount, value, sender/receiver).
- `/volume <token>`: 7-day token transfer volume in USD (supports symbols like SOL, USDC).
- `/history <token>`: 5-day price trends (open/close prices, supports symbols).
- `/alert <token> <condition>`: Custom volume-based alerts (e.g., `/alert USDC >1000`).
- **Inline Keyboard**: Interactive navigation for all commands.
- **Vybe Network Links**: Directs users to [Vybe Network](https://alpha.vybenetwork.com) for deeper analytics.

### Web Frontend Interface

- **Interactive Dashboard**: Access all bot features through a modern web interface
- **Real-time Updates**: Live data updates without page refresh
- **Responsive Design**: Optimized for both desktop and mobile devices
- **User-friendly Interface**: Clean and intuitive design for easy navigation

---

## Metrics Provided

The bot delivers key Solana blockchain metrics via Vybe APIs:

- **Wallet Balances**: Total USD value and token count (`/account/token-balance/{ownerAddress}`).
- **Whale Activity**: Labeled whale accounts with metadata (`/account/known-accounts`).
- **Token Transfers**: Transaction details (amount, USD value, addresses, timestamp) (`/token/transfers`).
- **Token Volume**: Aggregated USD volume over 7 days (`/token/{mintAddress}/transfer-volume`).
- **Price History**: Daily OHLC prices for tokens (`/price/{mintAddress}/token-ohlcv`).
- **Alerts**: Real-time volume monitoring with user-defined thresholds.

---

## Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Telegram Account**: To interact with the bot
- **Render Account**: For deployment (free tier available)
- **Vybe API Key**: Obtain from [@ericvybe](https://t.me/ericvybe) on Telegram
- **Bot Token**: Create via [@BotFather](https://t.me/BotFather) on Telegram
- **Web Browser**: Modern browser with JavaScript enabled
- **Dependencies**:
  - `pyTelegramBotAPI`: Telegram bot framework
  - `requests`: HTTP requests for Vybe APIs
  - `python-dotenv`: Environment variable management
  - `schedule`: Periodic alert checks
  - Static files served from `public/` directory

---

## Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/japhetjohn/marketpulsebot.git
   cd marketpulsebot
   ```

2. **Install Dependencies:**

   ```sh
   pip install pyTelegramBotAPI requests python-dotenv schedule
   ```

   For Windows, use the same command. For macOS/Linux, consider a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install pyTelegramBotAPI requests python-dotenv schedule
   ```

3. **Configure Environment:**
   Create a `.env` file in the project root:

   ```env
   BOT_TOKEN=your_bot_token_from_botfather
   VYBE_API_KEY=your_vybe_api_key
   ```

4. **Set Up Frontend:**

   ```sh
   # The frontend files are located in the public directory
   public/
   ├── index.html    # Main HTML file
   ├── styles.css    # CSS styles
   └── script.js     # JavaScript functionality
   ```

5. **Run the Bot and Frontend:**
   ```sh
   python bot.py
   # Access the web interface at http://localhost:YOUR_PORT
   ```

---

## Usage

### Telegram Bot

- Add [@MarketPulseTGBot](https://t.me/MarketPulseTGBot) to a Telegram group or chat directly.
- Use commands with valid Solana addresses or token inputs:
  - **Wallet Address Example:** `DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa`
  - **Token Symbol Example:** `SOL`, `USDC`
  - **Token Mint Example:** `So11111111111111111111111111111111111111112` (SOL)

### Commands

- `/start`: Displays welcome message and inline keyboard.
- `/pulse <address>`: Wallet summary.
- `/whale <address>`: Whale activity check.
- `/holdings <address>`: Token holdings.
- `/transfers <address>`: Recent transfers.
- `/volume <token>`: Token volume stats (e.g., `/volume SOL`).
- `/history <token>`: Price history (e.g., `/history USDC`).
- `/alert <token> <condition>`: Set volume alerts (e.g., `/alert USDC >1000`).

### Web Interface

Access the web interface through your browser:

- Navigate to the deployed URL or local development server
- Use the intuitive dashboard to:
  - View wallet analytics
  - Track whale activity
  - Monitor token transfers
  - Set up custom alerts
  - Access historical data
  - View real-time market trends

---

## Example Outputs

Below are formatted outputs for key commands, simulating Telegram responses from [@MarketPulseTGBot](https://t.me/MarketPulseTGBot):

```
/pulse DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa

📊 Wallet Analysis:
- Total Value: $0.50
- Total Tokens: 1
- Top Tokens:
  - USD Coin (USDC): 0.50 tokens

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa)

/holdings DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa

💰 Token Holdings:
- USD Coin (USDC): 0.50 tokens

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa)

/transfers DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa

🔄 Recent Transfers for `DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa`:

💸 Transfer:
- Token: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
- Amount: 0.50 tokens
- Value: $0.50
- From: `DVDXQgzc...`
- To: `ABC12345...`
- Date: Apr 27, 2025 10:30 AM

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/address/DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa)

/volume SOL

📊 Token Volume for `SOL`:
Total Volume (7 days): $1,234,567.89

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/So11111111111111111111111111111111111111112)

/history USDC

📈 Price History for `USDC`:
- 2025-04-23: Open: $1.00, Close: $1.01
- 2025-04-24: Open: $1.01, Close: $1.00
- 2025-04-25: Open: $1.00, Close: $1.02
- 2025-04-26: Open: $1.02, Close: $1.01
- 2025-04-27: Open: $1.01, Close: $1.00

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)

/alert USDC >1000

✅ Alert set for USDC when >1000.

Later, if triggered:

🚨 Alert Triggered for USDC:
Condition: Volume > $1,000.00
Current Volume: $1,234.56

🔍 View more at [Vybe Network](https://alpha.vybenetwork.com/token/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
```

---

## Deployment

### Render

1. **Create a Render Account:** Sign up at [Render](https://render.com) (free tier available).
2. **Create a New Web Service:**
   - Go to the Render Dashboard and click "New" > "Web Service".
   - Connect your GitHub repository (e.g., https://github.com/japhetjohn/marketpulsebot).
3. **Configure the Web Service:**
   - Name: `marketpulsebot`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Instance Type: Free or Starter (for testing)
   - Static Site: The `public` directory will be served automatically
4. **Set Environment Variables:**
   - In the Render Dashboard, go to "Environment" and add:
     ```env
     BOT_TOKEN=your_bot_token_from_botfather
     VYBE_API_KEY=your_vybe_api_key
     ```
5. **Add Required Files:**
   - Create a `requirements.txt`:
     ```txt
     pyTelegramBotAPI==4.14.0
     requests==2.31.0
     python-dotenv==1.0.0
     schedule==1.2.0
     ```
   - Ensure `.gitignore` excludes `.env`:
     ```gitignore
     .env
     venv/
     __pycache__/
     *.pyc
     ```
6. **Deploy:**
   - Push changes to your GitHub repository:
     ```sh
     git add .
     git commit -m "Deploy MarketPulseBot to Render"
     git push origin main
     ```
   - Render will auto-detect the push and deploy. Monitor the build logs in the Render Dashboard.
7. **Verify Deployment:**
   - Check the deployed URL (e.g., https://marketpulsebot.onrender.com).
   - Ensure the bot responds at [@MarketPulseTGBot](https://t.me/MarketPulseTGBot).
   - View logs in the Render Dashboard for errors.

### Local Testing Before Deployment

- Run locally to verify:
  ```sh
  python bot.py
  ```
- Test all commands with [@MarketPulseTGBot](https://t.me/MarketPulseTGBot) to ensure functionality.

---

## Troubleshooting

- **Syntax Errors (e.g., Pylance: "(" was not closed):**
  - Verify code matches the latest `bot.py` from the repo.
  - Check line numbers in error messages (e.g., line 275 for `/history`).
- **API Errors (404, 400):**
  - Use valid Solana addresses/tokens (e.g., SOL: `So11111111111111111111111111111111111111112`).
  - Verify `VYBE_API_KEY`.
- **Bot Not Responding:**
  - Ensure [@MarketPulseTGBot](https://t.me/MarketPulseTGBot) is added to a group with permissions.
  - Check `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).
  - Review Render logs for crashes.
- **Endpoint Issues:**
  - `/whale`: Address must be a known whale (`/account/known-accounts`).
  - `/transfers`: Wallet must have recent transfers.
  - `/volume`: Token must have volume data.
  - Test with: `/pulse DVDXQgzcsYU9BthFXWyAMvDxjr8LMiHfLCUnhUGQrMAa`, `/volume SOL`.
- **Alert Not Triggering:**
  - Ensure scheduler is running (run_scheduler logs).
  - Use realistic conditions (e.g., `>100` for low-volume tokens).
- **Pylance Errors:**
  - Install Pylance in VS Code.
  - Ensure python interpreter is set to the virtual environment.
- **Render Deployment Issues:**
  - Check build logs for dependency errors.
  - Ensure `requirements.txt` is correct.
  - Verify environment variables in the Render Dashboard.

---

## Vybe API Integration

MarketPulseBot uses the following Vybe API endpoints:

- `/account/token-balance/{ownerAddress}`: Wallet balances (total USD value, token details).
- `/account/known-accounts`: Whale account metadata (name, labels, date added).
- `/token/transfers`: Token transfer transactions (amount, USD value, addresses, timestamp).
- `/token/{mintAddress}/transfer-volume`: Aggregated USD volume over time.
- `/price/{mintAddress}/token-ohlcv`: OHLC price data for tokens.

All requests include error handling for HTTP status codes (400, 404, 500) and network issues, ensuring a robust user experience.

**Headers:**

```
VYBE_API_KEY: <VYBE_API_KEY>
```

---

## Why MarketPulseBot?

MarketPulseBot stands out in the Vybe Telegram Bot Challenge for:

- **Innovation (25%)**: Token symbol support (e.g., SOL, USDC) for alerts and analytics, surpassing competitors like PhanesBot.
- **User Experience (25%)**: Inline keyboard, loading indicators, and formatted outputs for seamless interaction.
- **Technical Execution (25%)**: Robust error handling, efficient API calls, and Render deployment for reliability.
- **Commercial Viability (10%)**: Links to [Vybe Network](https://alpha.vybenetwork.com) drive user engagement with Vybe’s platform.
- **Documentation Quality (15%)**: This README provides clear setup, usage, and troubleshooting, with example outputs and deployment guides.

Test it at [@MarketPulseTGBot](https://t.me/MarketPulseTGBot) and explore the code on [GitHub](https://github.com/japhetjohn/marketpulsebot).

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

---

## License

MIT License

Copyright (c) 2025 Japhet John

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
