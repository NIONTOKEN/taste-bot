import telebot
from telebot import types
import os
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎁 Günlük Ödül", callback_data="daily"),
        types.InlineKeyboardButton("👥 Davet Et", callback_data="invite"),
        types.InlineKeyboardButton("💰 Satın Al", callback_data="buy"),
        types.InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
        types.InlineKeyboardButton("🚀 MiniApp", url="https://t.me/taste_launch_bot/taste"),
        types.InlineKeyboardButton("📢Kanal", url="https://t.me/taste2025")
    )
    bot.send_message(message.chat.id, "🍕 *TASTE Bot'a Hoş Geldin!*\n\nAşağıdaki butonları kullan 👇", parse_mode="Markdown", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == "daily":
        bot.send_message(call.message.chat.id, "🎁 Günlük ödül: 50 TASTE!\nMiniApp'i açarak topla!")
    elif call.data == "invite":
        link = f"https://t.me/AirdropTasteBot?start=ref_{call.from_user.id}"
        bot.send_message(call.message.chat.id, f"👥 Davet linkin:\n{link}\n\nHer davet = 100 TASTE!")
    elif call.data == "buy":
        bot.send_message(call.message.chat.id, "💰 STON.fi'de satın al:\nhttps://app.ston.fi/swap?ft=TON&tt=EQB0beTxStmdhVri4s-cYlwYJaG_ZiR5lpLufCNC2VWUxZc-")
    elif call.data == "leaderboard":
        bot.send_message(call.message.chat.id, "🏆 Leaderboard yakında aktif!")
print("Bot starting...")
bot.polling(none_stop=True)
