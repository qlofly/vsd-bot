from aiogram import types

token = 'TOKEN'

admin_id = 111111


sbuttons = ["Запуск", "Изменить данные"]										
startButton = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
startButton.add(*sbuttons)

spbuttons = ["Остановить скрипт"]										
stopButton = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
stopButton.add(*spbuttons)
