import os

import telebot
from telebot import types
from dotenv import load_dotenv
from currency_converter import CurrencyConverter

currency = CurrencyConverter()

load_dotenv()
bot_key = os.environ.get("BOT")

bot = telebot.TeleBot(bot_key)

amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите сумму")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Введите сумму")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("JPY/USD", callback_data="jpy/usd")
        btn4 = types.InlineKeyboardButton("USD/JPY", callback_data="usd/jpy")
        btn5 = types.InlineKeyboardButton("другое", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4,btn5)
        bot.send_message(message.chat.id, "Выбери валюту", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число меньше 0. Введите сумму")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data != 'else':
        values = call.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слеш')
        bot.register_next_step_handler(call.message, else_curr)


def else_curr(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Не корректно введено значение. Введите еще раз")
        bot.register_next_step_handler(message, else_curr)










bot.polling(none_stop=True)
