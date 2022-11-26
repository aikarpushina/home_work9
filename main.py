"""
1) Напишите Бота, удаляющего из текста все слова, содержащие "абв". (Ввод от пользователя)
2) Создайте Бота для игры с конфетами человек против бота. (Дополнительно)
"""

import security
import telebot
import re

bot = telebot.TeleBot(security.get_token())


class ReplacementText(object):
    replacement_text = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ReplacementText, cls).__new__(cls)
        return cls.instance

    def get(self) -> str:
        return self.replacement_text

    def set(self, replacement_text: str) -> None:
        self.replacement_text = replacement_text


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    replacement_text = ReplacementText()
    if message.text[:4] == "/reg":
        replacement_text.set(replacement_text=message.text[5:])
        bot.send_message(message.from_user.id,
                         f"Запомнил. Буду удалять строки с сочетанием букв '{message.text[5:]}'")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Чтоб зарегестрировать сивлолы для удаления, напиши '/reg а', "
                         "буду удалять все слова с символом 'а' в словах")
    elif replacement_text.get() == "":
        bot.send_message(message.from_user.id,
                         f"Я тебя не понимаю введи /help")
    else:
        text = fix_text(text=message.text, replacement_text=replacement_text.get())
        if text.strip() != "":
            bot.send_message(message.from_user.id, text)


def fix_text(text: str, replacement_text: str) -> str:
    return re.sub(f"\s?\S*{replacement_text}\S*\s?", " ", text)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
