# MarketPulse Bot

A Telegram bot for crypto data using Vybe APIs, built for the Vybe Telegram Bot Challenge by Superteam Earn.

## Overview

MarketPulse Bot provides real-time and historical crypto data for Solana tokens directly on Telegram. It’s designed for traders and DeFi users, offering live volume, historical prices, and volume-based alerts. The bot is built in Python using the Telebot library, integrates with Vybe APIs, and is hosted on Render with UptimeRobot for reliability.

## Features

- **/pulse <token>**: Get live trading volume (e.g., /pulse SOL).
- **/alert <token> <condition>**: Set volume alerts (e.g., /alert SOL volume>50).
- **/history <token>**: View historical prices (e.g., /history SOL for prices 1 day and 7 days ago).
- *Command Menu*: Access all commands via /start or /help.
- *AlphaVybe Links*: Every message includes a link to AlphaVybe for deeper analytics.
- *Cartoon Robot Profile*: A fun, user-friendly bot avatar set via BotFather.

## Setup

1. *Clone the Repository*:
   ```bash
   git clone https://github.com/japhetjohn/MarketPulseBot
   cd MarketPulseBot
