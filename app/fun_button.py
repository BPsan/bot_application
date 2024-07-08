from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


register_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Регистрация через код", callback_data="riec_registrate")]])


#request_submit = ReplyKeyboardMarkup(inline_keyboard=[
#    [KeyboardButton(text="Подать заявку", callback_data="request_sub")]])
user_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Оставить заявку"),
     KeyboardButton(text="Мои заявки")],
    [KeyboardButton(text="Что умеет бот?")]
],resize_keyboard=True)

application_list = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Не работает интернет", callback_data="error_group")],
    [InlineKeyboardButton(text="Приложение выдает ошибку", callback_data="error_group")],
    [InlineKeyboardButton(text="Проблемы с клавиатурой и мышью", callback_data="error_group")],
    [InlineKeyboardButton(text="Компьютер выдает ошибку", callback_data="error_group")],
    [InlineKeyboardButton(text="Компьютер перестал включатся", callback_data="error_group")],
    [InlineKeyboardButton(text="Моей проблемы здесь нет", callback_data="error_group")]])