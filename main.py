from utils.data_structure import Data_Structure
from utils.dev import is_dev_env
from utils.t_bot import get_video, user_message_id
import telebot
from datetime import datetime
import json

import threading
import queue
import time

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import dotenv
dotenv.load_dotenv()
MY_ID = int(os.getenv("MY_ID"))
TOKEN_API = os.getenv("TOKEN_API")
TMP_FOLDER = os.getenv("BOT_FOLDER")
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE"))


bot = telebot.TeleBot(TOKEN_API)
bot.send_message(MY_ID, "Program started")
q = queue.Queue()

VALID_IDS = []
with open("valid_ids.json", "r") as file:
    VALID_IDS = json.load(file)
VALID_IDS.append(int(MY_ID))
VALID_IDS = set(VALID_IDS)


def process_queue(q):
    while True:
        item = q.get()  # Block and wait for an item from the queue
        if item is None:  # Use None as a signal to stop the thread
            break
        item.elaborate()
        print(f"Processing item: {item}")
        q.task_done()  # Indicate that the item has been processed


@bot.message_handler(func=lambda message: user_message_id(message) not in VALID_IDS)
def not_me(message):
    bot.reply_to(message, "Bot ad uso personale di Dosisido")


@bot.message_handler(content_types=["video"])
def video_handler(message):
    try:
        if q.qsize() >= MAX_QUEUE_SIZE:
            bot.reply_to(message, f"La coda è piena, attendere che venga elaborato un video")
            return

        if not os.path.isdir(TMP_FOLDER):
            os.mkdir(TMP_FOLDER)

        if is_dev_env(): bot.reply_to(message, "Downloading video")
        video_path = os.path.join(TMP_FOLDER, "video{:-%Y%m%d%H%M%S}.mp4".format(datetime.now()))
        get_video(message, bot, video_path)

        d = Data_Structure(video_path, message, bot)
        q.put(d)


    except Exception as e:
        bot.reply_to(message, f"Errore durante l'elaborazione: {e}")
        print("Error:", e)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello!")

@bot.message_handler(commands=["allowed"])
def allowed(message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    bot.reply_to(message, f"Lista utenti autorizzati:\n{'\n'.join(tuple(str(i) for i in VALID_IDS))}")

@bot.message_handler(commands=["add_id"])
def add_id(message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    try:
        user_id = message.text.split(" ")[1]
        VALID_IDS.add(int(user_id))
        with open("valid_ids.json", "w") as file:
            json.dump(list(VALID_IDS), file)
        bot.reply_to(message, f"Utente {user_id} aggiunto alla lista")
    except Exception as e:
        bot.reply_to(message, f"Errore: {e}")

@bot.message_handler(commands=["queue_size"])
def queue_size(message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    bot.reply_to(message, f"Dimensione della coda: {q.qsize()}")

@bot.message_handler(commands=["remove_id"])
def remove_id(message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    try:
        user_id = message.text.split(" ")[1]
        VALID_IDS.remove(int(user_id))
        with open("valid_ids.json", "w") as file:
            json.dump(list(VALID_IDS), file)
        bot.reply_to(message, f"Utente {user_id} rimosso dalla lista")
    except Exception as e:
        bot.reply_to(message, f"Errore: {e}")



thread = threading.Thread(target=process_queue, args=(q,))
thread.start()
bot.polling(timeout=10, long_polling_timeout=5)
