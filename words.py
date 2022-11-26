"""
Модуль бота работы со словами
"""

import re


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


def word_bot(bot, message):
    replacement_text = ReplacementText()
    if message.text[:4] == "/reg":
        replace_text = message.text[5:]
        if len(replace_text.rstrip()) > 0:
            replacement_text.set(replacement_text=replace_text)
            bot.send_message(message.from_user.id,
                             f"Запомнил. Буду удалять слова с сочетанием '{replace_text}'")
        else:
            bot.send_message(message.from_user.id, f"Ошибка! Необходимо указать символ.")
    elif replacement_text.get() == "":
        bot.send_message(message.from_user.id,
                         "Чтоб зарегестрировать сивлолы для удаления, напиши '/reg а', "
                         "буду удалять все слова с символом 'а' в словах (регистр важен)")
    else:
        text = fix_text(text=message.text, replacement_text=replacement_text.get())
        if text.strip() != "":
            bot.send_message(message.from_user.id, text)


def fix_text(text: str, replacement_text: str) -> str:
    return re.sub(f"\s?\S*{replacement_text}\S*\s?", " ", text)
