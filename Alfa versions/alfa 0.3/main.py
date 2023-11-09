import telebot
from telebot import types
import time
import random

bot = telebot.TeleBot('6756308071:AAFc6keNWbdYw0B0wLE3vDR0tTY2ne6H_yo')

stats = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1=types.KeyboardButton('Бросить кубик🎲')
    btn2=types.KeyboardButton('Орел или решка🎱')
    btn3=types.KeyboardButton('Разработчики🤓')
    markup.add(btn1,btn2,btn3)
    
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы посмотреть список команд.",reply_markup=markup)
    
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Жми', url='https://github.com/Kasinit/RoboCop-bot')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на гитхаб проекта", reply_markup = markup)    


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Вот список доступных команд:\n/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/version - версия бота")


@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно кикнуть администратора.")
        else:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")


@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60#4D4D4D#4D4D4D
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")


@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")


@bot.message_handler(commands=['version'])
def ver(message):
    bot.send_message(message.chat.id, 'alfa 0.3')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Бросить кубик🎲':
        bot.send_message(message.chat.id, 'На кубике выпало: ' + str(random.randint(1,6)))
        
    if message.text == 'Орел или решка🎱':
        a = 0
        a = random.randint(1,2)
        if a == 1:
            bot.send_message(message.chat.id, 'Выпал орел🎰')
        if a == 2:
            bot.send_message(message.chat.id, 'Выпала решка🎰')
            
    if message.text == 'Разработчики🤓':
        bot.send_message(message.chat.id, '@elonmas_k\n@aspxps')


bot.infinity_polling(none_stop=True)
