from telebot import types

from config.setup import lc


def init_payment_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=lc('payment completed button'))
    keyboard.add(payment)
    return keyboard


def request_membership_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=lc('request membership button'))
    keyboard.add(payment)
    return keyboard


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rules = types.KeyboardButton(text=lc('rules button'))
    register = types.KeyboardButton(text=lc('registration button'))
    status = types.KeyboardButton(text=lc('status button'))
    keyboard.add(rules, register, status)
    return keyboard


def participant_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_bet = types.KeyboardButton(text=lc('make bet button'))
    rules = types.KeyboardButton(text=lc('rules button'))
    status = types.KeyboardButton(text=lc('status button'))
    keyboard.add(make_bet, rules, status)
    return keyboard


class Keyboards:
    PAY = init_payment_keyboard()
    START = start_keyboard()
    REQUEST = request_membership_keyboard()
    MEMBER = participant_keyboard()
