from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


#your telegram bot token
#                ⬇️⬇️
bot = Bot(token='  ')
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)