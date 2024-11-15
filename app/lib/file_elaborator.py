from lib.trascriber import transcribe
from lib.utils_bot import split_text
import os
from time import sleep
from telebot import TeleBot
from lib.config import BOT_FOLDER
from lib.config import MESSAGE_MAX_LEN_WITHOUT_FILE
from telebot.types import Message


class FileElaborator:
    file_path: str

    def __init__(self, bot: TeleBot, message: Message, file_path: str, file_name: str, file_ext: str):
        self.bot = bot
        self.message = message
        self.file_path = file_path
        self.file_name = file_name
        self.file_ext = file_ext
    
    def elaborate(self):
        try:
            self.bot.reply_to(self.message, "Elaborazione in corso")
            text = transcribe(self.file_path)["text"]
            tmp_path= None

            if len(text) >= MESSAGE_MAX_LEN_WITHOUT_FILE:
                tmp_path = os.path.join(BOT_FOLDER, f"{self.file_name}.txt")
                with open(tmp_path, "w") as file:
                    file.write(text)
                self.bot.send_document(self.message.chat.id, open(tmp_path, "rb"), caption="Trascrizione", reply_to_message_id=self.message.message_id)
            else:
                self.bot.send_message(self.message.chat.id, text, reply_to_message_id=self.message.message_id)
        finally:
            sleep(1)
            os.remove(self.file_path)
            if tmp_path: os.remove(tmp_path)



    def __str__(self):
        return f"FileElaborator(file_path={self.file_path}, file_name={self.file_name}, file_ext={self.file_ext})"
