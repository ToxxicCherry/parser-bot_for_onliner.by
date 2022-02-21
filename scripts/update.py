from create_bot import bot
import json, asyncio, requests, time
from keyboards import user_kb
from scripts.main import HEADERS


def get_price(url_api, url):
    s = requests.Session()
    response = s.get(url=url_api, headers=HEADERS)
    data = response.json()
    price = data['prices']['price_min']['amount']
    name = data['name']
    return [price, name, url]



def send_messages_for_invalid():
    file_user_products = open('./DB/json_user_product.json', 'r')
    invalid_file = open('./DB/json_invalid_products.json', 'r')
    list = json.load(invalid_file)
    user_products = json.load(file_user_products)
    file_user_products.close()

    file = open('./DB/json_product.json', 'r')
    products= json.load(file)
    file.close()


    for item in list:
        for user in user_products.keys():
            if item in user_products[user]:
                asyncio.ensure_future(bot.send_message(user,f'На данный момент товара <b>{products[item][1]}</b>\n'
                                                            f'{products[item][2]}\nнет в наличии\n'
                                                            f'При вызове методе /show отобразится последняя сохраненная цена на него', parse_mode='html'))

def update(loop):
        print('Проверяю')

        file = open('./DB/json_product.json', 'r')
        invalid_file = open('./DB/json_invalid_products.json', 'r')
        invalid_products = json.load(invalid_file)
        products= json.load(file)
        invalid_file.close()
        file.close()

        file_user_products = open('./DB/json_user_product.json', 'r')
        user_products = json.load(file_user_products)
        file_user_products.close()


        for item in products.keys():
            try:
                new_price = get_price(item, products[item][2])[0]
                if float(products[item][0]) != float(new_price):
                    for j in user_products.keys():
                        if item in user_products[j]:
                           asyncio.ensure_future(bot.send_message(j, f'Цена на товар <b>{products[item][1]}\n{products[item][2]} изменилась </b>'
                                                                     f'с <b>{float(products[item][0])}</b> на <b>{float(new_price)}</b>',reply_markup=user_kb.user_kb , parse_mode='html' ))
                           if item in invalid_products:
                               asyncio.ensure_future(bot.send_message(j, f'Этот товар снова в наличии ⬆️'))
                               invalid_products.remove(item)

                products[item][0] = new_price
                print(f'{products[item][1]} проверил')
                time.sleep(2)
            except KeyError:
                if item not in invalid_products:
                    invalid_products.append(item)


        invalid_file = open('./DB/json_invalid_products.json', 'w')
        file_products = open('./DB/json_product.json', 'w')
        json.dump(products, file_products)
        json.dump(invalid_products, invalid_file)
        file_products.close()
        invalid_file.close()

        print('Проверил')
        send_messages_for_invalid()
        loop.call_later(3600*12, update, loop)