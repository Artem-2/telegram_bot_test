






def dot_env_craete():
    my_file = open("config.env", "w+", encoding="utf-8")
    my_file.write("""токен можно получить в BotFather
BOT_TOKEN=<bot_token>
id админов которые будут добавлены в телеграм бот(если несколько писать через запятую)
ADMINS=<admins>
адрес proxy сервера при наличии
PROXY=None
количество попыток изменения имени
number_of_changes_rename=1""")
    my_file.close()