from create_bot import bot
import json, asyncio
from keyboards import user_kb

def update(loop):
        print('Проверяю')
        file_products = open('./DB/json_product.json', 'r')
        file_products_for_bot = open('./DB/json_product_for_bot.json', 'r')
        file_user_products = open('./DB/json_user_product.json', 'r')

        products = json.load(file_products)
        products_for_bot = json.load(file_products_for_bot)
        user_products_for_bot = json.load(file_user_products)


        file_products.close()
        file_products_for_bot.close()
        file_user_products.close()

        for item in products_for_bot.keys():
            if products[item][0] < products_for_bot[item][0]:
                for j in user_products_for_bot.keys():
                    if item in user_products_for_bot[j]:
                       asyncio.ensure_future(bot.send_message(j, f'Цена на товар <b>{products_for_bot[item][1]}\n{products_for_bot[item][2]} снизилась </b>'
                                                                 f'на <b>{float(products_for_bot[item][0]) - float(products[item][0])}</b>\n'
                                                                 f'Теперь <b>{products[item][0]}</b>',reply_markup=user_kb.user_kb , parse_mode='html' ))
            products_for_bot[item] = products[item]

        file_products_for_bot = open('./DB/json_product_for_bot.json', 'w')
        json.dump(products_for_bot, file_products_for_bot)
        file_products_for_bot.close()

        print('Проверил')
        loop.call_later(100, update, loop)