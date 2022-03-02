import sqlite3

from create_bot import bot
import asyncio, requests, time
from keyboards import user_kb
from scripts.main import HEADERS


def get_price(url_api):
    s = requests.Session()
    response = s.get(url=url_api, headers=HEADERS)
    data = response.json()
    price = data['prices']['price_min']['amount']

    return price



def send_messages_for_invalid():

   with sqlite3.connect("./DB/ParserBot.db") as con:
       cur = con.cursor()
       for invalid in  cur.execute("""SELECT users_products.user_id,
                                              products.name,
                                              products.url
                                      FROM users_products
                                      JOIN products ON product_id == products.id
                                      WHERE products.is_invalid == 1"""):



        asyncio.ensure_future(bot.send_message(invalid[0],f'На данный момент товара <b>{invalid[1]}</b>\n'
                                                f'{invalid[2]}\nнет в наличии\n'
                                                f'При вызове методе /show отобразится '
                                                f'последняя сохраненная цена на него', parse_mode='html', reply_markup=user_kb.user_kb))

def update(loop):


        with sqlite3.connect("./DB/ParserBot.db") as con:
            cur = con.cursor()

            items = cur.execute(f"""SELECT price, api_url, name, url FROM products""").fetchall()
            for item in items:
                time.sleep(2)
                print(f'Проверяю {item[2]}')
                try:

                    new_price = get_price(item[1])

                except:

                    cur.execute(f"""UPDATE products SET is_invalid = 1 WHERE api_url == '{item[1]}'""")

                else:

                    if float(item[0]) != float(new_price):
                        user_id = cur.execute(f"""SELECT user_id FROM users_products
                                                    JOIN products ON product_id == products.id
                                                    WHERE products.api_url == '{item[1]}'""").fetchone()

                        if user_id != None:
                            asyncio.ensure_future(bot.send_message(user_id[0], f"Цена на товар <b>{item[2]}</b>\n"
                                                                               f"{item[3]}\n"
                                                                               f"изменилась с <b>{item[0]}</b> на <b>{new_price}</b>",
                                                                               reply_markup=user_kb.user_kb, parse_mode='html'))

                    cur.execute(f"""UPDATE products SET price = '{float(new_price)}', is_invalid = 0 WHERE api_url == '{item[1]}'""")




        print('Проверил')
        send_messages_for_invalid()
        loop.call_later(3600*12, update, loop)