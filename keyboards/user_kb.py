from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Show')
b_del = KeyboardButton('/Delete')
b_cancel = KeyboardButton('/Cancel')
b_add = KeyboardButton('/Add_url')


user_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(b1).add(b_add).insert(b_del)
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(b_cancel)
greetings_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(b_add)

