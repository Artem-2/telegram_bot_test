from tgbot.db import BotDB
import os.path

try:
    p = os.path.join(".","DB","tests.db")
    BotDB = BotDB(p)
except:
    print("Не удается подключиться к базе данных")
