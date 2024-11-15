
import requests
from typing import Tuple
from telebot import util, TeleBot
from telebot.types import Message

from lib.config import TOKEN_API


def get_file(file_id, bot: TeleBot, file_path):
    
    # Get the file info
    file_info = bot.get_file(file_id)
    
    # Create the file path URL
    remote_file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN_API}/{remote_file_path}"

    # Download the file
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception("Errore durante il download del video")


    with open(file_path, 'wb') as file:
        file.write(response.content)

def split_text(text, max_length= 3500) -> Tuple[str]:
    assert max_length <= 4096, "max_length must be less than or equal to 4096"
    # Splits by last '\n', '. ' or ' ' in exactly this priority.
    # smart_split returns a list with the splitted text.
    splitted_text = util.smart_split(text, chars_per_string=max_length)
    return tuple(splitted_text)

def user_message_id(message: Message) -> int:
    return message.from_user.id
