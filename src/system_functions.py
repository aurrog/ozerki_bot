import datetime
import os


def load_logs(message):
    file = open('config/user_data.txt', 'a', encoding='utf-8')
    data = f'{str(message.from_user.id)}, {str(message.from_user.username)}, {message.from_user.first_name},' \
           f' {message.from_user.last_name}:   {message.text}      {datetime.datetime.today()}\n'
    file.write(data)

    file.close()


def cache_clean():
    for root, dirs, files in os.walk('\.cache'):
        for filename in files:
            os.rmdir(r'.cache\'+filename')
