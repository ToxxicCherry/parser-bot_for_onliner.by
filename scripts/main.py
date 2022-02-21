import requests, json, re

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36'
}

def save_user_id(user_id):
    file = open('./DB/users_id.json', 'r')
    users = json.load(file)
    file.close()

    if user_id not in users:
        users.append(user_id)

    file = open('./DB/users_id.json', 'w')
    json.dump(users, file)
    file.close()


async def del_item(user_id, number):
    save_user_id(user_id)
    file = open('./DB/json_user_product.json', 'r')
    user_products = json.load(file)
    file.close()

    if len(user_products[str(user_id)]) > 0 and str(user_id) in user_products.keys():
        del user_products[str(user_id)][int(number)-1]

    file = open('./DB/json_user_product.json', 'w')
    json.dump(user_products, file)
    file.close()



def get_info_for_user(user_id):
    save_user_id(user_id)
    result = []
    user_id = str(user_id)
    file_products = open('./DB/json_product.json', 'r')
    file_user_products = open('./DB/json_user_product.json', 'r')

    products = json.load(file_products)
    user_products = json.load(file_user_products)

    file_products.close()
    file_user_products.close()

    if user_id not in user_products.keys():
        return 'Твой список пуст, пес\nИли я просто почистил базу...'

    i = 1
    for item in user_products[user_id]:
        result.append(': '.join([str(i) + '. ' + products[item][1], '<b>' + products[item][0] + ' BYN'+'</b>' + '\n' + products[item][2]]))
        i += 1

    return '\n'.join(result)


async def set_json(link, user_id):
    save_user_id(user_id)
    user_id = str(user_id)
    s = requests.Session()
    link_api = f'https://catalog.api.onliner.by/products/' + re.findall(r'/([^/]+$)', link)[0]
    response = s.get(url=link_api, headers=HEADERS)
    data = response.json()
    price = data['prices']['price_min']['amount']
    name = data['name']

    file = open('./DB/json_product.json', 'r')
    products_dict = json.load(file)
    file.close()

    if link_api not in products_dict.keys():
        products_dict[link_api] = [price, name, link]

    file = open('./DB/json_product.json', 'w')
    json.dump(products_dict, file)
    file.close()

    # --------USER---------------------
    file = open('./DB/json_user_product.json', 'r')
    user_products = json.load(file)
    file.close()

    if user_id not in user_products.keys():
        user_products[user_id] = []
        user_products[user_id].append(link_api)
    elif link_api not in user_products[user_id]:
        user_products[user_id].append(link_api)

    file = open('./DB/json_user_product.json', 'w')
    json.dump(user_products, file)
    file.close()

