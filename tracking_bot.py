import asyncio,json
from aiogram import executor
from create_bot import bot, dispatcher
from keyboards import user_kb
from handlers import users
from scripts.update import update




async def on_startup(_):
    file = open('DB/users_id.json', 'r')
    users = json.load(file)
    file.close()
    for id in users:
         await bot.send_message(id, 'Я перезапустился', reply_markup=user_kb.user_kb)
         await bot.send_sticker(id,r'CAACAgIAAxkBAAED9WViDlkoWl8yl0RR9zIrq-XNXkVMeQACHAADD27HLxMGmvf9kXwrIwQ')




users.register_handlers_users(dispatcher)


loop = asyncio.get_event_loop()
loop.call_later(1, update, loop)

executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
