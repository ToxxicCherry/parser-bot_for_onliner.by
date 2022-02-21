import requests, json, re, asyncio

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36'
}

link = 'https://catalog.onliner.by/videocard/palit/ne63060t19k9190a'





def test(user_id):
    file = open('users.json', 'r')
    users = json.load(file)
    file.close()

    users.append(user_id)

    file = open('users.json', 'w')
    json.dump(users, file)
    file.close()


test(549993023)