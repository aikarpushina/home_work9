"""
1) Напишите Бота, удаляющего из текста все слова, содержащие "абв". (Ввод от пользователя)
2) Создайте Бота для игры с конфетами человек против бота. (Дополнительно)
"""

import security
import telebot
import words
import candies
import logging

bot = telebot.TeleBot(security.get_token())

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    )


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
        logging.debug(f"launched_bot = {launched_bot.get()}; "
                      f"input text = {message.text}; "
                      f"user: {message.from_user.id}; "
                      f"{message.from_user.username}; "
                      f"{message.from_user.last_name}; "
                      f"{message.from_user.first_name}")
        print(f"launched_bot = {launched_bot.get()}")
        print(f"input text = {message.text}")
        print(f"user: {message.from_user.id}; "
              f"{message.from_user.username}; "
              f"{message.from_user.last_name}; "
              f"{message.from_user.first_name}")
        print("----------------------------------------")
        if message.text == "/word":
            launched_bot.set(launched_bot="word")
            # bot.send_message(message.from_user.id, f"Бот запущен для помощи введи /help")
        if message.text == "/candy":
            launched_bot.set(launched_bot="candy")
            # bot.send_message(message.from_user.id, f"Бот запущен для помощи введи /help")
        if message.text == "/restart":
            launched_bot.set(launched_bot="")
        if launched_bot.get() == "word":
            words.word_bot(bot=bot, message=message)
        if launched_bot.get() == "candy":
            candies.candy_bot(bot=bot, message=message)
        if launched_bot.get() == "":
            bot.send_message(message.from_user.id,
                             f"Какого бота запустить?\n"
                             f"Удаление слов введи /word\n"
                             f"Игра конфеты введи /candy\n"
                             f"Перезапуск /restart\n")
    except BaseException:
        logging.exception(f"An exception was thrown! username = {message.from_user.username}")
        bot.send_message(message.from_user.id, f"Произошла ошибка, мы работаем над устронением ошибки.")
        bot.send_message(message.from_user.id, f"Перезапуск.")
        bot.send_message(message.from_user.id,
                         f"Какого бота запустить?\n"
                         f"Удаление слов введи /word\n"
                         f"Игра конфеты введи /candy\n"
                         f"Перезапуск /restart\n")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
