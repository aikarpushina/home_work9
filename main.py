"""
1) Напишите Бота, удаляющего из текста все слова, содержащие "абв". (Ввод от пользователя)
2) Создайте Бота для игры с конфетами человек против бота. (Дополнительно)
"""

import security
import telebot
import words

bot = telebot.TeleBot(security.get_token())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    words.word_bot(bot, message)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
