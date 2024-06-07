from utils.trascriber import ElaborateMp4
from utils.t_bot import split_text
import os
from time import sleep


class Data_Structure:
    video_path: str

    def __init__(self, video_path: str, message, bot):
        self.video_path = video_path
        self.message = message
        self.bot = bot
    
    def elaborate(self):

        self.bot.reply_to(self.message, "Elaborazione in corso")
        elaboration = ElaborateMp4(self.video_path)
        elaboration.max_duration = 10
        text = elaboration.transcribe()

        texts = split_text(text)
        self.bot.reply_to(self.message, texts[0])
        for t in texts[1:]:
            self.bot.send_message(self.message.chat.id, t)

        sleep(1)
        os.remove(self.video_path)