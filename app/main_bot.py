import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


from lib.config import MY_ID, TOKEN_API, BOT_FOLDER as TMP_FOLDER, MAX_QUEUE_SIZE
from lib.file_elaborator import FileElaborator
from lib.dev import is_dev_env
from lib.utils_bot import get_file, user_message_id
from lib.utils import get_mime
import telebot
from telebot.types import Message
from datetime import datetime
import json
import signal

import threading
import queue


bot = telebot.TeleBot(TOKEN_API, threaded=False)
q = queue.Queue()
VALID_IDS = []
if not os.path.isfile("valid_ids.json"):
    with open("valid_ids.json", "w") as file:
        json.dump([MY_ID], file, indent=4)
with open("valid_ids.json", "r") as file:
    VALID_IDS = json.load(file)
    assert isinstance(VALID_IDS, list)
VALID_IDS.append(int(MY_ID))
VALID_IDS = set(VALID_IDS)  




def process_queue(q: queue.Queue):
    while True:
        item: FileElaborator = q.get()
        if item is None: break
        print(f"Processing item: {item}")
        item.elaborate()
        q.task_done()


@bot.message_handler(func=lambda message: user_message_id(message) not in VALID_IDS)
def not_me(message: Message):
    bot.reply_to(message, "User not allowed")


@bot.message_handler(content_types=["video", "audio", "document"], )
def video_handler(message: Message):
    try:
        if q.qsize() >= MAX_QUEUE_SIZE:
            bot.reply_to(message, f"Operazione fallita: coda piena")
            return

        content_type = message.content_type
        message_json = message.json
        mime_type = message_json[content_type]["mime_type"]
        file_id = message_json[content_type]["file_id"]
        ext = (mime_type).split("/")[-1]

        if not any(x in mime_type for x in ["audio", "video"]):
            bot.reply_to(message, "Tipo di file non supportato")
            return

        if not os.path.isdir(TMP_FOLDER):
            os.mkdir(TMP_FOLDER)

        if is_dev_env(): bot.reply_to(message, "Downloading file")
        filename = message_json[content_type].get("file_name", "unknown_name")
        file_path = os.path.join(TMP_FOLDER, "file{:-%Y%m%d%H%M%S%f}.".format(datetime.now())+ext)
        get_file(file_id, bot, file_path)
        
        real_mime = get_mime(file_path)
        if real_mime != mime_type:
            bot.reply_to(message, f"You tried to fool me! The file is not a {mime_type} but a {real_mime}")
            os.remove(file_path)
            return

        d = FileElaborator(bot, message, file_path, filename, ext)
        q.put(d)


    except Exception as e:
        bot.reply_to(message, f"Errore durante l'elaborazione: {e}")
        print("Error:", e)

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.reply_to(message, "User allowed")

@bot.message_handler(commands=["allowed"])
def allowed(message: Message):
    print(type(user_message_id(message)), type(MY_ID), user_message_id(message)== MY_ID)
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    bot.reply_to(message, "Lista utenti autorizzati:\n" + '\n'.join(str(i) for i in VALID_IDS))

@bot.message_handler(commands=["add_id"])
def add_id(message: Message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    try:
        user_id = message.text.split(" ")[1]
        VALID_IDS.add(int(user_id))
        with open("valid_ids.json", "w") as file:
            json.dump(list(VALID_IDS), file, indent=4)
        bot.reply_to(message, f"Utente {user_id} aggiunto alla lista")
    except Exception as e:
        bot.reply_to(message, f"Errore: {e}")

@bot.message_handler(commands=["queue_size"])
def queue_size(message: Message):
    if user_message_id(message) != MY_ID:
        bot.reply_to(message, "Non hai i permessi per eseguire questa azione")
        return
    bot.reply_to(message, f"Dimensione della coda: {q.qsize()}")

@bot.message_handler(commands=["remove_id"])
def remove_id(message: Message):
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



def main():
    def signal_handler(sig, frame):
        print('Stopping the program')
        q.put(None)  # Signal the queue processing thread to exit
        bot.stop_polling()  # Stop the bot polling
        if not is_dev_env(): bot.send_message(MY_ID, "Program stopped")
    
  

    bot.send_message(MY_ID, "Program started")
    print("Program started")
    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=process_queue, args=(q,))
    thread.start()
    bot.polling(
        timeout=10,
        long_polling_timeout=5,
    )

if __name__ == "__main__":
    main()
