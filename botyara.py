import telebot
from math import *
import requests
from currency_converter import CurrencyConverter
import secret

cur = CurrencyConverter()


money = 0
bot = telebot.TeleBot(secret.BOT_TOKEN)
dollar = 82.65
@bot.message_handler(commands = ['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Приветсвую')
@bot.message_handler(commands = ['dollar'])
def first(message):
    bot.reply_to(message, f'<i> Введите сумму(к сожалению рубли не поддерживаются, пока что работаю над этим):</i>', parse_mode='html')
    bot.register_next_step_handler(message, summ)
def summ(message):
    global money
    try:
        money = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Формат не верный. Дебил блин цифры введи:')
        bot.register_next_step_handler(message, summ)
        return
    if money > 0:     
        money = message.text.strip()
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        bot1 = telebot.types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        bot2 = telebot.types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        bot3 = telebot.types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
        bot4 = telebot.types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
        bot5 = telebot.types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(bot1, bot2, bot3, bot4, bot5)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Формат не верный. Дебил блин положительную сумму введи:')
        bot.register_next_step_handler(message, summ)
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    value = call.data.upper().split('/')
    r = cur.convert(money, value[0], value[1])
    bot.send_message(call.message.chat.id,f'Выходит {r}. Можешь ввести сумму заново:')
    bot.register_next_step_handler(call.message, summ)
def mycur(message):
    try:
        value = message.data.upper().split('/')
        r = cur.convert(money, value[0],value[1])
        bot.send_message(message.chat.id,f'Выходит {r}. Можешь ввести сумму заново:')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send_message('Упс! Ошибочка вышла. введ заново:')
        bot.register_next_step_handler(message, mycur)

    
    
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    try:
        result = str(eval(message.text))
    except:
        result = 'lol debil vvedi normalno'
    bot.reply_to(message, result)
bot.infinity_polling()
