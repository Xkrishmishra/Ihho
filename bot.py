import telebot
import random
import requests
import time
from telebot import types

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

OPENROUTER_API_KEY = "PUT_YOUR_OPENROUTER_API_KEY_HERE"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def escape(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(['\\' + c if c in escape_chars else c for c in text])

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is running!")

def get_openrouter_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "AI service unavailable."

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
