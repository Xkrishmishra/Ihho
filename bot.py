import telebot
import requests
from telebot import types

TOKEN = "7082422086:AAFdWEghh628ZnFjlHwI3v0jQfyM0UB8Fk4"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

bot = telebot.TeleBot(TOKEN)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "➕ Add Me To Group",
            url=f"https://t.me/{bot.get_me().username}?startgroup=true"
        )
    )

    bot.send_message(
        message.chat.id,
        "✅ Bot is running successfully!",
        reply_markup=markup
    )


@bot.message_handler(commands=['tell'])
def tell(message):
    question = message.text.replace('/tell', '', 1).strip()

    if not question:
        bot.reply_to(message, "Usage:\n/tell Hello")
        return

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()

        answer = response.json()["choices"][0]["message"]["content"]

        bot.reply_to(message, answer[:4000])

    except Exception as e:
        bot.reply_to(message, f"Error:\n{e}")


@bot.edited_message_handler(
    content_types=[
        'text',
        'photo',
        'video',
        'document',
        'sticker',
        'audio'
    ]
)
def edited(message):
    try:
        bot.delete_message(
            message.chat.id,
            message.message_id
        )

        bot.send_message(
            message.chat.id,
            f"⚠️ {message.from_user.first_name} edited a message."
        )

    except Exception as e:
        print(e)


print("Bot Started...")
bot.infinity_polling(
    skip_pending=True,
    timeout=60,
    long_polling_timeout=60
)
