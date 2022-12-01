"""
1) Напишите Бота, удаляющего из текста все слова, содержащие "абв". (Ввод от пользователя)
2) Создайте Бота для игры с конфетами человек против бота. (Дополнительно)

github: https://github.com/aikarpushina/home_work9
"""

import security
import telebot
import words
import candies
import logging
from telebot import types
from fractions import Fraction
from logging.handlers import TimedRotatingFileHandler

bot = telebot.TeleBot(security.get_token())

file_name = r"logs/mylog.log"

logger = logging.getLogger("root loger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename=file_name, when="midnight", interval=1, backupCount=7)
handler.suffix = "%Y-%m-%d %H:%M:%S"
logger.addHandler(handler)

a, b = 0, 0
act = ""

class LaunchedBot(object):
    launched_bot = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LaunchedBot, cls).__new__(cls)
        return cls.instance

    def get(self) -> str:
        return self.launched_bot

    def set(self, launched_bot: str) -> None:
        self.launched_bot = launched_bot


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        launched_bot = LaunchedBot()
        logger.info(f"launched_bot = {launched_bot.get()}; "
                    f"input text = {message.text}; "
                    f"user: {message.from_user.id}; "
                    f"{message.from_user.username}; "
                    f"{message.from_user.last_name}; "
                    f"{message.from_user.first_name}")
        if message.text == "/word":
            logger.info(f"user {message.from_user.first_name} start word bot")
            launched_bot.set(launched_bot="word")
        if message.text == "/candy":
            logger.info(f"user {message.from_user.first_name} start candy bot")
            launched_bot.set(launched_bot="candy")
        if message.text == "/calc":
            logger.info(f"user {message.from_user.first_name} start calc bot")
            launched_bot.set(launched_bot="calc")
        if message.text == "/restart":
            launched_bot.set(launched_bot="")
            logger.info(f"user {message.from_user.first_name} restarted")
        if launched_bot.get() == "word":
            words.word_bot(bot=bot, message=message)
        if launched_bot.get() == "candy":
            candies.candy_bot(bot=bot, message=message)
        if launched_bot.get() == "calc":
            calc_bot(message=message)
        if launched_bot.get() == "":
            bot.send_message(message.from_user.id,
                             f"Какого бота запустить?\n"
                             f"Удаление слов введи /word\n"
                             f"Игра конфеты введи /candy\n"
                             f"Калькулятор /calc\n"
                             f"Перезапуск /restart\n")
    except BaseException as ex:
        logger.error(f"An exception was thrown! username = {message.from_user.username}")
        logger.error(ex)
        bot.send_message(message.from_user.id, f"Произошла ошибка, мы работаем над устронением ошибки.")
        bot.send_message(message.from_user.id, f"Перезапуск.")
        bot.send_message(message.from_user.id,
                         f"Какого бота запустить?\n"
                         f"Удаление слов введи /word\n"
                         f"Игра конфеты введи /candy\n"
                         f"Перезапуск /restart\n")


def calc_bot(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Рациональный', callback_data='rational')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Комплексный ', callback_data='complex')
    keyboard.add(key_no)
    question = 'Какой калькулятор запустим?'
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'rational')
def call_calc_rational(call):
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: start rational calc")
    keyboard_rational = types.InlineKeyboardMarkup()  # наша клавиатура
    key_plus = types.InlineKeyboardButton(text='a+b', callback_data='calc_plus')  # кнопка «Да»
    key_minus = types.InlineKeyboardButton(text='a-b ', callback_data='calc_minus')
    key_multiply = types.InlineKeyboardButton(text='a*b', callback_data='calc_multiply')  # кнопка «Да»
    key_divide = types.InlineKeyboardButton(text='a/b ', callback_data='calc_divide')
    keyboard_rational.add(key_plus, key_minus, key_multiply, key_divide)
    question = 'Выберете операцию:'
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard_rational)


@bot.callback_query_handler(func=lambda call: call.data == 'complex')
def call_calc_complex(call):
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: start complex calc")
    bot.send_message(call.message.chat.id, 'Упс... Пока не работает.')
    bot.send_message(call.message.chat.id, f"Для выхода /restart")
    calc_bot(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'calc_plus')
def calc_plus_rational(call):
    global act
    act = "+"
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: select {act} operation")
    input_(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'calc_minus')
def calc_plus_rational(call):
    global act
    act = "-"
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: select {act} operation")
    input_(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'calc_multiply')
def calc_plus_rational(call):
    global act
    act = "*"
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: select {act} operation")
    input_(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'calc_divide')
def calc_plus_rational(call):
    global act
    act = "/"
    logger.info(f"user {call.message.from_user.id} {call.message.from_user.username}: select {act} operation")
    input_(call.message)


def input_(message):
    bot.send_message(message.chat.id, 'Введите а (формат 2/1): ')
    bot.register_next_step_handler(message, input_a)

def input_a(message):
    global a
    a = Fraction(message.text)
    logger.info(f"user {message.from_user.id} {message.from_user.username}: input a = {a}")
    bot.send_message(message.chat.id, 'Введите b (формат 2/1): ')
    bot.register_next_step_handler(message, input_b)


def input_b(message):
    global b
    b = Fraction(message.text)
    logger.info(f"user {message.from_user.id} {message.from_user.username} input a = {b}")
    calculate(message)


def calculate(message):
    global a, b, act
    if act == "+":
        bot.send_message(message.chat.id, f'a + b = {a + b}')
        logger.info(f"user {message.from_user.id} {message.from_user.username}: {a} {act} {b} = {a + b}")
    elif act == "-":
        bot.send_message(message.chat.id, f'a - b = {a - b}')
        logger.info(f"user {message.from_user.id} {message.from_user.username}: {a} {act} {b} = {a - b}")
    elif act == "*":
        bot.send_message(message.chat.id, f'a * b = {a * b}')
        logger.info(f"user {message.from_user.id} {message.from_user.username}: {a} {act} {b} = {a * b}")
    elif act == "/":
        bot.send_message(message.chat.id, f'a / b = {a / b}')
        logger.info(f"user {message.from_user.id} {message.from_user.username}: {a} {act} {b} = {a / b}")
    else:
        bot.send_message(message.chat.id, f'Неверная операция.')
        logger.info(f"user {message.from_user.id} {message.from_user.username}: выбрана неверная операция")
    bot.send_message(message.from_user.id, f"Для выхода /restart")
    calc_bot(message)


if __name__ == "__main__":
    logger.info(f"----------------------------------------------------------------------------------")
    logger.info(f"----------------------------------START-------------------------------------------")
    logger.info(f"----------------------------------------------------------------------------------")
    bot.polling(none_stop=True, interval=0)
