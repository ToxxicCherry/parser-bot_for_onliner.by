from scripts import main
from keyboards import user_kb
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from aiogram.dispatcher.filters import Text




async def start(message: types.Message):
    main.save_user_id(message.from_user.id)
    await message.answer('Ну здарова', reply_markup=user_kb.greetings_kb)
    await bot.send_sticker(message.from_user.id,r'CAACAgIAAxkBAAED9WViDlkoWl8yl0RR9zIrq-XNXkVMeQACHAADD27HLxMGmvf9kXwrIwQ')
    await message.answer('Я могу сохранять ссылки на товары с Onliner.by и проверять цены\n'
                         'Если цена изменится - я дам знать.\nТак же можно проверить самостоятельно.\n'
                         'Добавь хотя бы одну ссылку. После сможешь просмотреть список и отредактировать его\n(Нажми кнопку)')



async def show_list(message: types.Message):
    await message.answer(main.get_info_for_user(message.from_user.id), parse_mode='html', reply_markup=user_kb.user_kb)


#----------------------Машина состояний. Удаление товара из списка пользователя----------------------------------------
#Прерывание удаления
async def cancel_delete_or_add(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ок', reply_markup=user_kb.user_kb)


#Класс состояний для удаления
class Deleter(StatesGroup):
    item = State()



#Жмет на кнопку удалить и попадаем сюда
async def start_del(message: types.Message):
    answer = main.get_info_for_user(message.from_user.id)
    if answer == 'Твой список пуст':
        await message.answer(answer)
    else:
        await Deleter.item.set()
        await message.answer(answer, parse_mode='html')
        await message.answer('Введи номер', reply_markup=user_kb.cancel_kb)

#Ловим ответ
async def finish_del(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['item_to_delete'] = message.text  # Введенная инфа идет в оперативку

    async with state.proxy() as data:

        if message.text.isdigit() and int(message.text) > 0:
            try:
                await main.del_item(message.from_user.id, data['item_to_delete'])
                await state.finish()
                await message.answer('Ок')
                await message.answer(main.get_info_for_user(message.from_user.id), parse_mode='html', reply_markup=user_kb.user_kb)
            except:
                await message.answer('Шутник блять, вводи нормальный номер')
        else:
            await message.answer('Шутник блять, вводи нормальный номер')




#----------------------------------------------------------------------------------------------------------------------
#---------------------------------Машина состояний для ввода ссылки----------------------------------------------------

class Adder(StatesGroup):
    link = State()

#Жмет на кнопку добавить и попадаем сюда
async def start_add(message: types.Message):
    await Adder.link.set()
    await message.answer('Дай мне рабочую ссылку на товар Onliner', reply_markup=user_kb.cancel_kb)


#Ловим ответ
async def finish_add(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['item_need_to_add'] = message.text  # Введенная инфа идет в оперативку


    async with state.proxy() as data:
        try:
            await main.set_data(data['item_need_to_add'], message.from_user.id)
            await state.finish()
            await message.answer('Done')
            await message.answer(main.get_info_for_user(message.from_user.id), parse_mode='html', reply_markup=user_kb.user_kb)
        except:
            await message.answer('Ссылка не работает!')

#----------------------------------------------------------------------------------------------------------------------


def register_handlers_users(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cancel_delete_or_add, commands='Cancel', state="*")
    dispatcher.register_message_handler(cancel_delete_or_add, Text(equals='Cancel', ignore_case=True), state="*")
    dispatcher.register_message_handler(start, commands = 'start')
    dispatcher.register_message_handler(show_list, commands='Show')
    dispatcher.register_message_handler(start_del, commands='Delete', state=None)
    dispatcher.register_message_handler(finish_del, state=Deleter.item)
    dispatcher.register_message_handler(start_add, commands='Add_url', state=None)
    dispatcher.register_message_handler(finish_add, state=Adder.link)







