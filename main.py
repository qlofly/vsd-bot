from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
import config
import os


storage = MemoryStorage()
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)

class data(StatesGroup):
     post_data = State()
     get_data = State()
     cc_data = State()

name_files = ['kudaotpr.txt', 'kudprim.txt', 'cc.txt']
for x in range(0, (len(name_files))):
	if not name_files[x] in str(os.listdir()):
		file = open(name_files[x],'w')
		file.close()
	else:
		pass

@dp.message_handler(commands="start")
async def start(message: types.Message):
    if message.chat.id == config.admin_id:
    	await bot.send_message(message.chat.id, 'Доступ разрешён', reply_markup=config.startButton)  
    elif message.chat.id != config.admin_id:
    	await bot.send_message(message.chat.id, 'Доступ запрещён.')

@dp.message_handler(state=None)
async def void(message: types.Message):
	if message.chat.id == config.admin_id:
		if message.text == 'Запуск':
			try:
				await bot.send_message(message.chat.id, 'Скрипт запущен', reply_markup=config.stopButton)
				# os.startfile('C:/users/server/desktop/script.exe')
				print('start script')
			except Exception as e:
				await bot.send_message(message.chat.id, 'Произошла ошибка на сервере', reply_markup=config.startButton)
				os.system('notify-send Err')
		elif message.text == 'Изменить данные':
			await message.answer("Откуда отправлять?")
			await data.post_data.set()
		elif message.text == 'Остановить скрипт':
			try:
				# os.system('Taskkill /IM script.exe /F')
				print('Taskkill')
				await bot.send_message(message.chat.id, 'Скрипт остановлен', reply_markup=config.startButton)
			except Exception as e:
				await bot.send_message(message.chat.id, 'Произошла ошибка на сервере', reply_markup=config.startButton)
				os.system('notify-send Err')

	elif message.chat.id != config.admin_id:
		await bot.send_message(message.chat.id, 'Доступ запрещён!')


@dp.message_handler(state=data.post_data)
async def enter_pil(message: types.Message, state: FSMContext):
    await state.update_data(post_data=message.text)
    with open('kudaotpr.txt', 'w') as post:
    	post.write(message.text)
    await message.answer("Куда принимать?")
    await data.get_data.set()

@dp.message_handler(state=data.get_data)
async def enter_fut(message: types.Message, state: FSMContext):
    await state.update_data(get_data=message.text)
    with open('kudprim.txt', 'w') as get:
    	get.write(message.text)
    await message.answer("Карта банка куда принимать итог:")
    await data.cc_data.set()

@dp.message_handler(state=data.cc_data)
async def enter_fut(message: types.Message, state: FSMContext):
    await state.update_data(cc_data=message.text)
    with open('cc.txt', 'w') as cc:
    	cc.write(message.text)
    await bot.send_message(message.chat.id, "Данные обновлены", reply_markup=config.startButton)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)