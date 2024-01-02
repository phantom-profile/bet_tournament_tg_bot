from telebot import types

from config.setup import l


def init_payment_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=l('payment completed button'))
    keyboard.add(payment)
    return keyboard


def request_membership_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=l('request membership button'))
    keyboard.add(payment)
    return keyboard


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rules = types.KeyboardButton(text=l('rules button'))
    register = types.KeyboardButton(text=l('registration button'))
    status = types.KeyboardButton(text=l('status button'))
    keyboard.add(rules, register, status)
    return keyboard


def participant_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_bet = types.KeyboardButton(text=l('make bet button'))
    rules = types.KeyboardButton(text=l('rules button'))
    status = types.KeyboardButton(text=l('status button'))
    keyboard.add(make_bet, rules, status)
    return keyboard
