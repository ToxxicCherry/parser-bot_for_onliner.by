import requests, re, sqlite3

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36'
}

def get_price(url_api):
    s = requests.Session()
    response = s.get(url=url_api, headers=HEADERS)
    data = response.json()
    price = data['prices']['price_min']['amount']
    name = data['name']

    return price, name


def save_user_id(user_id):
    with sqlite3.connect("./DB/ParserBot.db") as con:
        cur = con.cursor()

        try:
            cur.execute(f"""INSERT INTO users (id) VALUES ({user_id}) """)
        except:
            print("Такой id уже есть")




def get_info_for_user(user_id):
    result = []
    i = 1
    with sqlite3.connect("./DB/ParserBot.db") as con:
        cur = con.cursor()


        for value in cur.execute(f""" SELECT products.name, products.price, products.url 
                        FROM users
                        JOIN users_products ON users.id == users_products.user_id
                        JOIN products ON product_id == products.id
                        WHERE user_id == {user_id} """):
            result.append(': '.join([str(i) + '. ' + value[0], '<b>' + str(value[1]) + ' BYN'+'</b>' + '\n' + value[2]]))
            i += 1
    del i
    if result == []:
        return 'Твой список пуст'
    else:
        return '\n'.join(result)


async def set_data(link, user_id):
    link_api = f'https://catalog.api.onliner.by/products/' + re.findall(r'/([^/]+$)', link)[0]


    with sqlite3.connect("./DB/ParserBot.db") as con:
        cur = con.cursor()

        fl = 1
        for url in cur.execute("""SELECT url FROM products"""):
            if link == url[0]:
                fl = 0
                break


        if fl:
            price_name = get_price(link_api)

            cur.execute(f"""INSERT INTO products (name, price, url, api_url ) 
            VALUES (?, ?, ?, ?)""", (price_name[1], price_name[0], link, link_api))
            con.commit()


        product_id = cur.execute(f"""SELECT id FROM products WHERE url == '{link}'""").fetchone()
        fl2 = 1
        for value in cur.execute("""SELECT * FROM users_products"""):
            if (user_id, product_id[0]) == value:
                fl2 = 0
                break
        if fl2:
            cur.execute("""INSERT INTO users_products VALUES (?, ?)""", (user_id, product_id[0]))
            con.commit()



async def del_item(user_id, number):
    with sqlite3.connect("./DB/ParserBot.db") as con:
        cur = con.cursor()

        user_list = cur.execute(f""" SELECT products.id
                            FROM users
                            JOIN users_products ON users.id == users_products.user_id
                            JOIN products ON product_id == products.id
                            WHERE user_id == {user_id} """).fetchall()

        cur.execute(f"""DELETE FROM users_products WHERE product_id == '{user_list[int(number)-1][0]}'""")
        con.commit()






