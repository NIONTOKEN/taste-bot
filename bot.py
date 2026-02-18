import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Taste Bot Aktif 🚀")

@bot.message_handler(commands=['invite'])
def invite(message):
    bot.reply_to(message, "Invite sistemi yakında aktif.")

@bot.message_handler(commands=['daily'])
def daily(message):
    bot.reply_to(message, "Günlük ödül: 50 TASTE")

@bot.message_handler(commands=['buy'])
def buy(message):
    bot.reply_to(message, "Satın alma modülü yakında.")

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    bot.reply_to(message, "Leaderboard hazırlanıyor.")

bot.polling()
