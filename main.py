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
from logging.handlers import TimedRotatingFileHandler

bot = telebot.TeleBot(security.get_token())

file_name = r"logs/mylog.log"

logger = logging.getLogger("root loger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename=file_name, when="midnight", interval=1, backupCount=7)
handler.suffix = "%Y-%m-%d %H:%M:%S"
logger.addHandler(handler)


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
        if message.text == "/restart":
            launched_bot.set(launched_bot="")
            logger.info(f"user {message.from_user.first_name} restarted")
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


if __name__ == "__main__":
    logger.info(f"----------------------------------------------------------------------------------")
    logger.info(f"----------------------------------START-------------------------------------------")
    logger.info(f"----------------------------------------------------------------------------------")
    bot.polling(none_stop=True, interval=0)
