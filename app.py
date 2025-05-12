import os
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask
from download import download_song

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"  # صفحه اصلی برای نگه‌داشتن سرور

def handle_message(update, context):
    query = update.message.text
    update.message.reply_text(f"🎵 در حال جستجو: {query}")
    
    download_output = download_song(query)  # جستجو و دانلود آهنگ

    # ارسال فایل و متن آهنگ
    with open(download_output, 'rb') as audio:
        update.message.reply_audio(audio)
    os.remove(download_output)  # پاک کردن فایل بعد از ارسال

def run_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()  # شروع به دریافت پیام‌ها
    updater.idle()

if __name__ == '__main__':
    from threading import Thread
    Thread(target=run_bot).start()  # بات را در یک thread جداگانه اجرا کن
    app.run(host='0.0.0.0', port=8080)  # راه‌اندازی سرور Flask
