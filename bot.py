import telebot
from telebot import types
import os
import threading
import time
import requests
import json
from datetime import datetime, timezone, timedelta

# ==========================================
# TASTE BOT - @taste_launch_bot
# Kanal: @taste2025 | Grup: @taste_miniapp
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@taste2025")  # Duyuru kanalı
GROUP_ID = os.getenv("GROUP_ID", "@taste_miniapp")   # Topluluk grubu

# TASTE Token bilgileri
TASTE_CONTRACT = "EQB0beTxStmdhVri4s-cYlwYJaG_ZiR5lpLufCNC2VWUxZc-"
STONFI_POOL = "EQCGEHrBuuoKVJ_0LqQy38F-c-pN-Jrz0M_ASdCtJxZL74nS"
WEBAPP_URL = "https://incandescent-gelato-cc11a4.netlify.app"
MINIAPP_LINK = "https://t.me/taste_launch_bot/app"
STONFI_SWAP_URL = f"https://app.ston.fi/swap?chartVisible=false&ft=TON&tt={TASTE_CONTRACT}"

bot = telebot.TeleBot(TOKEN)


# ==========================================
# 📊 FİYAT & VERİ SERVİSLERİ
# ==========================================

def get_taste_price():
    """GeckoTerminal API'den TASTE fiyatını çek"""
    try:
        url = f"https://api.geckoterminal.com/api/v2/networks/ton/pools/{STONFI_POOL}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {})
        price = float(attrs.get("base_token_price_usd", 0))
        change = float(attrs.get("price_change_percentage", {}).get("h24", 0))
        volume = float(attrs.get("volume_usd", {}).get("h24", 0))
        return {"price": price, "change": change, "volume": volume}
    except Exception as e:
        print(f"[Price Error] {e}")
        return {"price": 0.00135, "change": 0.0, "volume": 0}


def get_holders_count():
    """TonAPI'den holder sayısını çek"""
    try:
        url = f"https://tonapi.io/v2/jettons/{TASTE_CONTRACT}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data.get("holders_count", 0)
    except Exception as e:
        print(f"[Holders Error] {e}")
        return 0


def get_usd_try_rate():
    """USD/TRY kuru"""
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=8)
        data = resp.json()
        return data.get("rates", {}).get("TRY", 34.5)
    except:
        return 34.5


# ==========================================
# 🤖 BOT KOMUTLARI
# ==========================================

@bot.message_handler(commands=['start'])
def start(message):
    """Ana başlangıç menüsü"""
    user_name = message.from_user.first_name or "Kullanıcı"

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Mini App Aç", web_app=types.WebAppInfo(url=WEBAPP_URL)),
        types.InlineKeyboardButton("💰 TASTE Satın Al", url=STONFI_SWAP_URL),
        types.InlineKeyboardButton("📢 Duyuru Kanalı", url="https://t.me/taste2025"),
        types.InlineKeyboardButton("💬 Topluluk", url="https://t.me/taste_miniapp"),
        types.InlineKeyboardButton("📊 Fiyat Bilgisi", callback_data="price"),
        types.InlineKeyboardButton("👥 Davet Et", callback_data="invite"),
    )

    bot.send_message(
        message.chat.id,
        f"🍕 *Hoş geldin {user_name}!*\n\n"
        f"*TASTE Token* — TON blockchain üzerinde gastronomi odaklı token 🍔\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 *Kontrat:* `{TASTE_CONTRACT}`\n"
        f"🔒 %72 Kilitli (JVault)\n"
        f"💧 %20 Likidite (STON.fi)\n"
        f"📊 Toplam Arz: 25,000,000\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"Aşağıdaki butonları kullanarak başla! 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.message_handler(commands=['price', 'fiyat'])
def price_command(message):
    """Anlık fiyat bilgisi"""
    send_price_info(message.chat.id)


@bot.message_handler(commands=['buy', 'satin'])
def buy_command(message):
    """Satın alma linki"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 STON.fi'de Satın Al", url=STONFI_SWAP_URL),
        types.InlineKeyboardButton("🚀 Mini App", web_app=types.WebAppInfo(url=WEBAPP_URL)),
    )
    bot.send_message(
        message.chat.id,
        "💰 *TASTE Token Satın Al*\n\n"
        "STON.fi üzerinden TON ile TASTE satın alabilirsin!\n\n"
        f"📊 Kontrat: `{TASTE_CONTRACT}`\n\n"
        "1️⃣ Tonkeeper/TON Space cüzdanına TON yükle\n"
        "2️⃣ STON.fi'de swap yap\n"
        "3️⃣ TASTE token'ların cüzdanına gelsin! 🎉",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.message_handler(commands=['invite', 'davet'])
def invite_command(message):
    """Davet linki oluştur"""
    user_id = message.from_user.id
    invite_link = f"https://t.me/taste_launch_bot/app?startapp=ref_{user_id}"
    share_text = "🍕 TASTE Token - TON blockchain üzerinde gastronomi devrimi! Mini App'i dene 🚀"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📤 Linki Paylaş",
            url=f"https://t.me/share/url?url={invite_link}&text={requests.utils.quote(share_text)}"
        ),
        types.InlineKeyboardButton("💬 Gruba Katıl", url="https://t.me/taste_miniapp"),
    )

    bot.send_message(
        message.chat.id,
        f"👥 *Davet Sistemi*\n\n"
        f"Senin davet linkin:\n`{invite_link}`\n\n"
        f"🤝 Arkadaşlarını davet et, topluluğu büyüt!\n"
        f"💪 Birlikte daha güçlüyüz!",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.message_handler(commands=['help', 'yardim'])
def help_command(message):
    """Yardım menüsü"""
    bot.send_message(
        message.chat.id,
        "📋 *TASTE Bot Komutları*\n\n"
        "🚀 /start — Ana menü\n"
        "📊 /price — Anlık fiyat bilgisi\n"
        "💰 /buy — Satın alma linki\n"
        "👥 /invite — Davet linki\n"
        "📋 /help — Bu menü\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📢 Kanal: @taste2025\n"
        "💬 Grup: @taste\\_miniapp\n"
        "🤖 Mini App: @taste\\_launch\\_bot",
        parse_mode="Markdown"
    )


# ==========================================
# 🔘 CALLBACK HANDLERs
# ==========================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "price":
        bot.answer_callback_query(call.id, "📊 Fiyat bilgisi yükleniyor...")
        send_price_info(call.message.chat.id)

    elif call.data == "invite":
        bot.answer_callback_query(call.id)
        user_id = call.from_user.id
        invite_link = f"https://t.me/taste_launch_bot/app?startapp=ref_{user_id}"

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "📤 Paylaş",
                url=f"https://t.me/share/url?url={invite_link}&text=TASTE%20Mini%20App%20dene!%20🍕🚀"
            )
        )
        bot.send_message(
            call.message.chat.id,
            f"👥 Senin davet linkin:\n`{invite_link}`\n\n"
            f"Arkadaşlarına paylaş! 🎉",
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif call.data == "refresh_price":
        bot.answer_callback_query(call.id, "🔄 Güncelleniyor...")
        send_price_info(call.message.chat.id)


# ==========================================
# 📊 FİYAT BİLGİSİ GÖNDERİCİ
# ==========================================

def send_price_info(chat_id):
    """Fiyat bilgisini gönder"""
    price_data = get_taste_price()
    holders = get_holders_count()
    try_rate = get_usd_try_rate()

    price = price_data["price"]
    change = price_data["change"]
    volume = price_data["volume"]
    try_price = price * try_rate

    change_emoji = "🟢" if change >= 0 else "🔴"
    change_sign = "+" if change >= 0 else ""

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Yenile", callback_data="refresh_price"),
        types.InlineKeyboardButton("💰 Satın Al", url=STONFI_SWAP_URL),
    )

    bot.send_message(
        chat_id,
        f"📊 *TASTE Token — Anlık Fiyat*\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 *Fiyat:* ${price:.6f}\n"
        f"🇹🇷 *TRY:* ₺{try_price:.4f}\n"
        f"{change_emoji} *24s Değişim:* {change_sign}{change:.1f}%\n"
        f"📈 *24s Hacim:* ${volume:,.0f}\n"
        f"👥 *Holder:* {holders:,}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🔒 %72 Kilitli • 💧 %20 Likidite\n"
        f"📊 Toplam Arz: 25,000,000 TASTE\n\n"
        f"🕐 _{datetime.now(timezone(timedelta(hours=3))).strftime('%d.%m.%Y %H:%M')} (TR)_",
        parse_mode="Markdown",
        reply_markup=markup
    )


# ==========================================
# 📢 KANAL OTOMATİK POST FONKSİYONLARI
# ==========================================

def post_price_to_channel():
    """Kanala fiyat güncellemesi postala"""
    try:
        price_data = get_taste_price()
        holders = get_holders_count()
        try_rate = get_usd_try_rate()

        price = price_data["price"]
        change = price_data["change"]
        volume = price_data["volume"]
        try_price = price * try_rate

        change_emoji = "🟢" if change >= 0 else "🔴"
        change_sign = "+" if change >= 0 else ""

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🚀 Mini App", web_app=types.WebAppInfo(url=WEBAPP_URL)),
            types.InlineKeyboardButton("💰 Satın Al", url=STONFI_SWAP_URL),
            types.InlineKeyboardButton("💬 Topluluk", url="https://t.me/taste_miniapp"),
        )

        bot.send_message(
            CHANNEL_ID,
            f"📊 *TASTE — Fiyat Güncellemesi*\n\n"
            f"💎 *${price:.6f}* ({change_emoji} {change_sign}{change:.1f}%)\n"
            f"🇹🇷 ₺{try_price:.4f}\n"
            f"📈 24s Hacim: ${volume:,.0f}\n"
            f"👥 Holder: {holders:,}\n\n"
            f"🔒 %72 Kilitli • 💧 %20 Likidite\n\n"
            f"#TASTE #TON #Crypto",
            parse_mode="Markdown",
            reply_markup=markup
        )
        print(f"[Channel] ✅ Fiyat postu gönderildi - ${price:.6f}")
    except Exception as e:
        print(f"[Channel Error] Fiyat postu hatası: {e}")


def post_daily_report():
    """Kanala günlük topluluk raporu"""
    try:
        price_data = get_taste_price()
        holders = get_holders_count()
        try_rate = get_usd_try_rate()

        price = price_data["price"]
        change = price_data["change"]
        try_price = price * try_rate
        market_cap = price * 25_000_000

        now = datetime.now(timezone(timedelta(hours=3)))
        date_str = now.strftime("%d.%m.%Y")

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🚀 Mini App Aç", web_app=types.WebAppInfo(url=WEBAPP_URL)),
            types.InlineKeyboardButton("💰 TASTE Al", url=STONFI_SWAP_URL),
            types.InlineKeyboardButton("💬 Sohbete Katıl", url="https://t.me/taste_miniapp"),
        )

        bot.send_message(
            CHANNEL_ID,
            f"📋 *TASTE — Günlük Rapor*\n"
            f"📅 {date_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💎 Fiyat: ${price:.6f} (₺{try_price:.4f})\n"
            f"📊 Market Cap: ${market_cap:,.0f}\n"
            f"👥 Toplam Holder: {holders:,}\n"
            f"🔒 Kilitli: %72 (JVault)\n"
            f"💧 Likidite: %20 (STON.fi)\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"🍕 *Gastronomi devriminde yerinizi alın!*\n\n"
            f"#TASTE #DailyReport #TON",
            parse_mode="Markdown",
            reply_markup=markup
        )
        print(f"[Channel] ✅ Günlük rapor gönderildi - {date_str}")
    except Exception as e:
        print(f"[Channel Error] Günlük rapor hatası: {e}")


# ==========================================
# ⏰ ZAMANLANMIŞ GÖREVLER
# ==========================================

def scheduler_thread():
    """Arka planda çalışan zamanlayıcı"""
    print("[Scheduler] ⏰ Zamanlayıcı başlatıldı")

    while True:
        try:
            now = datetime.now(timezone(timedelta(hours=3)))
            hour = now.hour
            minute = now.minute

            # Her 4 saatte bir fiyat güncellemesi (06:00, 10:00, 14:00, 18:00, 22:00)
            if hour in [6, 10, 14, 18, 22] and minute == 0:
                print(f"[Scheduler] 📊 Fiyat güncellemesi gönderiliyor... ({hour}:00)")
                post_price_to_channel()

            # Her gün saat 09:00'da günlük rapor
            if hour == 9 and minute == 0:
                print("[Scheduler] 📋 Günlük rapor gönderiliyor...")
                post_daily_report()

            # Her dakika kontrol et
            time.sleep(60)

        except Exception as e:
            print(f"[Scheduler Error] {e}")
            time.sleep(60)


# ==========================================
# 👋 GRUBA KATILIM HOŞGELDİN MESAJI
# ==========================================

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    """Gruba yeni katılan üyelere hoşgeldin mesajı"""
    for new_member in message.new_chat_members:
        if new_member.is_bot:
            continue

        name = new_member.first_name or "Dostum"

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🚀 Mini App Aç", web_app=types.WebAppInfo(url=WEBAPP_URL)),
            types.InlineKeyboardButton("📢 Duyurular", url="https://t.me/taste2025"),
        )

        bot.send_message(
            message.chat.id,
            f"👋 *Hoş geldin {name}!*\n\n"
            f"🍕 TASTE Token topluluğuna katıldın!\n\n"
            f"İlk adımlar:\n"
            f"1️⃣ Mini App'i aç ve keşfet\n"
            f"2️⃣ @taste2025 kanalını takip et\n"
            f"3️⃣ Arkadaşlarını davet et!\n\n"
            f"Sorularını burada sorabilirsin 💬",
            parse_mode="Markdown",
            reply_markup=markup
        )


# ==========================================
# 🚀 BOT BAŞLATMA
# ==========================================

if __name__ == "__main__":
    print("=" * 50)
    print("🍕 TASTE Bot v2.0 başlatılıyor...")
    print(f"📢 Kanal: {CHANNEL_ID}")
    print(f"💬 Grup: {GROUP_ID}")
    print(f"🤖 Bot: @taste_launch_bot")
    print("=" * 50)

    # Zamanlayıcıyı arka planda başlat
    scheduler = threading.Thread(target=scheduler_thread, daemon=True)
    scheduler.start()
    print("[Scheduler] ✅ Arka plan zamanlayıcı aktif")

    # Bot'u başlat
    print("[Bot] ✅ Polling başlatılıyor...")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
