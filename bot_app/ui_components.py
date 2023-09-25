from telebot import types

from config.setup import locale


def init_payment_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=locale.read('request_pay_proof'))
    keyboard.add(payment)
    return keyboard


def request_membership_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    payment = types.InlineKeyboardButton(text=locale.read('request_membership'))
    keyboard.add(payment)
    return keyboard


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    rules = types.KeyboardButton(text=locale.read('rules'))
    register = types.KeyboardButton(text=locale.read('register'))
    status = types.KeyboardButton(text=locale.read('status'))
    keyboard.add(rules, register, status)
    return keyboard


def participant_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    make_bet = types.KeyboardButton(text=locale.read('make_bet'))
    rules = types.KeyboardButton(text=locale.read('rules'))
    status = types.KeyboardButton(text=locale.read('status'))
    keyboard.add(make_bet, rules, status)
    return keyboard
