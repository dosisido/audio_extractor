import telebot
import os
import dotenv
dotenv.load_dotenv()
MY_ID = int(os.getenv("MY_ID"))
TOKEN_API = os.getenv("TOKEN_API")

bot = telebot.TeleBot(TOKEN_API)

# use in for delete with the necessary scope and language_code if necessary
bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("allowed", "Lista degli utenti autorizzati"),
        telebot.types.BotCommand("start", "Inizia il bot"),
        telebot.types.BotCommand("add_id", "Aggiungi un id alla lista degli utenti autorizzati"),
        telebot.types.BotCommand("remove_id", "Rimuovi un id dalla lista degli utenti autorizzati"),
        telebot.types.BotCommand("queue_size", "Dimensione della coda")        


        
    ],
    scope=telebot.types.BotCommandScopeChat(MY_ID)  # use for personal command for users
    # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
)

# check command
cmd = bot.get_my_commands(language_code=None)
print([c.to_json() for c in cmd])


print('done')