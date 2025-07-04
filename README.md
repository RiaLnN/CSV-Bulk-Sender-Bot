# 📩 CSV Bulk Sender Bot

A **Telegram bot** that reads a `.csv` file and sends personalized messages to users by their Telegram `chat_id`. Useful for basic broadcasting or internal message delivery.

---

## ✅ Features

- Upload a `.csv` file and send messages from it.
- Sends each message to the corresponding user.
- Ignores rows that fail (invalid ID, blocked bot, etc.).
- Uses `aiogram 3.x` and handles errors gracefully.

---

## 🚀 How to Use
- Start the bot with /start.
- Send a CSV file with the structure above.
- The bot will begin sending messages immediately.
- Any failed deliveries will be skipped silently.
---
## 📄 CSV Format

The bot expects the following structure:
```csv
name,chat_id,message
John,123456789,Hello John!
Anna,987654321,Hi Anna, how are you?
