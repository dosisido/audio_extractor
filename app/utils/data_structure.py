from utils.trascriber import ElaborateMp4, transcribe
from utils.t_bot import split_text
import os
from time import sleep
from telebot import TeleBot, Message


class Data_Structure:
    video_path: str

    def __init__(self, video_path: str, message: Message, bot: TeleBot):
        self.video_path = video_path
        self.message = message
        self.bot = bot
    
    def elaborate(self):

        self.bot.reply_to(self.message, "Elaborazione in corso")
        text = transcribe(self.video_path)["text"]

        texts = split_text(text)
        self.bot.reply_to(self.message, texts[0])
        for t in texts[1:]:
            self.bot.send_message(self.message.chat.id, t)

        sleep(1)
        os.remove(self.video_path)