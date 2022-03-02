import asyncio, sqlite3


from aiogram import executor
from create_bot import bot, dispatcher
from keyboards import user_kb
from handlers import users
from scripts.update import update




async def on_startup(_):
    with sqlite3.connect('DB/ParserBot.db') as con:
        cur = con.cursor()

        users_id = cur.execute("""SELECT * FROM users""").fetchall()

        for id in users_id:
            await bot.send_message(id[0], 'Я перезапустился', reply_markup=user_kb.user_kb)




users.register_handlers_users(dispatcher)


loop = asyncio.get_event_loop()
loop.call_later(1, update, loop)

executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
