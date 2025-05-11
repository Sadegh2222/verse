import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from download import download_song
from genius import get_lyrics
from translations import trans

load_dotenv()

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(trans['start_message'])

def search_song(update: Update, context: CallbackContext):
    song_name = " ".join(context.args)
    if not song_name:
        update.message.reply_text(trans['empty_song_name'])
        return

    update.message.reply_text(trans['downloading_song'])

    # Download the song and return the path
    song_path = download_song(song_name)

    # Send the song to the user
    with open(song_path, 'rb') as song:
        update.message.reply_audio(song, caption=trans['song_sent'])

    # Send similar songs and lyrics buttons
    keyboard = [
        [InlineKeyboardButton(trans['similar_songs'], callback_data='similar_songs')],
        [InlineKeyboardButton(trans['show_lyrics'], callback_data='show_lyrics')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(trans['song_downloaded'], reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'similar_songs':
        query.edit_message_text(trans['similar_songs_text'])
        # Fetch and show similar songs here

    elif query.data == 'show_lyrics':
        query.edit_message_text(trans['fetching_lyrics'])
        lyrics = get_lyrics(query.message.text)  # Use the song name or something else
        query.message.reply_text(lyrics)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_song))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    return "Bot is alive!"

if __name__ == '__main__':
    main()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
