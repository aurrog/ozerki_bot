import json


def check_user_city(user_id):
    with open('config/accounts.json', 'r', encoding='utf-8') as file:
        accounts_data = json.load(file)

    return accounts_data[str(user_id)] if str(user_id) in accounts_data.keys() else False


def add_account(user_id, city):
    with open('config/accounts.json', 'r', encoding='utf-8') as file:
        accounts_data = json.load(file)
        accounts_data[str(user_id)] = city

    with open('config/accounts.json', 'w', encoding='utf-8') as file:
        json.dump(accounts_data, file, ensure_ascii=False)
