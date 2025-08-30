import telebot
from config import API_TOKEN
from logic_ai import get_class

bot = telebot.TeleBot(API_TOKEN)

SAVE_DIR = "images"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот который классифицирует шарики по цветам.")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    file_path = SAVE_DIR + '/' + file_name
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    class_name, score = get_class(file_path)

    if score < 0.5:
        bot.send_message(message.chat.id, "Не могу определить цвет шарика. Попробуй другое фото.")
    else:
        bot.send_message(message.chat.id, f"Это {class_name} с точностью {score*100:.2f}%")

bot.polling()