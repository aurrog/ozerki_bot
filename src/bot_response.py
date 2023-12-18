import src.parsing_functions as pf
import telebot
import src.settings as settings
import src.account as account


def request_to_user(bot, message):
    city = account.check_user_city(message.from_user.id)
    if city:
        object_url, code = pf.find_url(message.text, city)
        if object_url:
            if code == 'product':
                response = pf.parce_information_for_bot(object_url, code)
                pf.get_url_to_img(object_url)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(message.text, url=object_url)
                markup.add(button1)
                bot.send_photo(message.from_user.id, open('images/img.jpg', 'rb'), caption=response, reply_markup=markup)
            else:
                response = pf.parce_information_for_bot(object_url, code)
                letter = ''
                for i in response:
                    letter+=i
                bot.send_message(message.from_user.id, letter)
        else:
            bot.send_message(message.from_user.id, 'Извините, произошла ошибка.')
    else:
        check_registration(bot, message)


def check_registration(bot, message):
    bot.send_message(message.from_user.id, 'Для продолжения работы бота, необходимо добавить Ваш город. напишите '
                                           'команду\n'
                                           '/set_city [нужный вам город] (Без квадратных скобок)')


def command_messages(bot, message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Введите название лекарства, а бот выдаст его цену и наличие в аптеках.')
        bot.send_message(message.from_user.id, 'Чтобы выбрать нужный Вам город, напишите команду\n'
                                               '/set_city [нужный вам город] (Без квадратных скобок)\n'
                                               'Чтобы посмотреть выбранный вами город, напишите команду\n'
                                               '/my_city')
        check_registration(bot, message)
    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Чтобы выбрать нужный Вам город, напишите команду\n'
                                               '/set_city [нужный вам город] (Без квадратных скобок)\n'
                                               'Чтобы посмотреть выбранный вами город, напишите команду\n'
                                               '/my_city')
    if '/set_city' in message.text:
        city = message.text[10:len(message.text)]
        if city.lower() in settings.CITY_LIST:
            account.add_account(message.from_user.id, city)
            bot.send_message(message.from_user.id, f'Город {city} успешно добавлен.')
        else:
            bot.send_message(message.from_user.id, f'Извините, произошла ошибка. Проверьте правильность написания Вашего'
                                                   f'города и проверьте его наличие в списке доступных городов:\n'
                                                   f'{settings.CITY_LIST}')
    if message.text == '/my_city':
        bot.send_message(message.from_user.id, f'Ваш город: {account.check_user_city(message.from_user.id).capitalize()}.')


