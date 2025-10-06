1. Клонирование репозитория 

```git clone /Artem-2/telegram_bot_test```
2. Создание виртуального окружения

```py -m venv venv```

3. Активация виртуального окружения

для Windows (cmd.exe): '''venv\Scripts\activate.bat'''

для Windows (PowerShell): '''venv\Scripts\Activate.ps1'''

для macOS и Linux (bash/zsh): '''source venv/bin/activate'''

4. Переход в папку проекта

```cd .\telegram_bot_test\```

5. Установка зависимостей

```pip install -r requirements.txt```

6. Первый запуск телеграмм бота (необходим для создания конфиг файла)

```py bot.py```

7. В рабочей директории появится файл config.env, необходимо его заполнить (инструкция прописана внутри)
