"""
Модуль бота игры в конфеты
"""

import random


class Candies(object):
    candies = -1
    my_step = True

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Candies, cls).__new__(cls)
        return cls.instance

    def get(self) -> int:
        return self.candies

    def set(self, candies: int) -> None:
        self.candies = candies

    def revert_step(self):
        self.my_step = not self.my_step

    def get_step(self):
        return self.my_step


def step_user(bot, message, candies):
    candy_user = message.text
    if candy_user.isdigit():
        candy = int(candy_user)
        if 0 < candy <= 28 and candies.get() - candy >= 0:
            candies.set(candies.get() - candy)
            bot.send_message(message.from_user.id, f"На столе осталось {candies.get()} конфет.")
            candies.revert_step()
            if candies.get() == 0:
                bot.send_message(message.from_user.id, f"Ура! Вы победили!.")
                candies.set(-1)
        else:
            bot.send_message(message.from_user.id, f"Взять можно от 0 до 28 конфет, "
                                                   f"но не болнн {candies.get()} конфет.")
    else:
        bot.send_message(message.from_user.id, f"Введите число.")


def step_bot(bot, message, candies):
    candy = random.randint(1, 28 if candies.get() >= 28 else candies.get())
    bot.send_message(message.from_user.id, f"Компьютер взял {candy} конфет.")
    candies.set(candies.get() - candy)
    candies.revert_step()
    if candies.get() == 0:
        bot.send_message(message.from_user.id, f"Упс! Победили бот!.")
        candies.set(-1)


def candy_bot(bot, message):
    candies = Candies()
    if message.text[:6] == "/start":
        candies.set(candies=int(message.text[7:]))
        bot.send_message(message.from_user.id,
                         f"Игра началась. На столе '{message.text[7:]}' конфен. "
                         f"Ваш ход первый. За ход можно взять не более 28 конфет.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         f"Для начала игры введите '/start 2021', 2021 - это сколько конфет на столе в начале игры.")
    elif candies.get() == -1:
        bot.send_message(message.from_user.id,
                         f"Я тебя не понимаю введи /help")
    else:
        if candies.get_step():
            step_user(bot=bot, message=message, candies=candies)
        else:
            step_bot(bot=bot, message=message, candies=candies)
