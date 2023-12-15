import src.parsing_functions as pf
import telebot


def request_to_user(bot, message):
    object_url = pf.find_url(message.text)
    if object_url:
        response = pf.parce_information_for_bot(object_url)
        pf.get_url_to_img(object_url)
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(message.text, url=object_url)
        markup.add(button1)
        bot.send_photo(message.from_user.id, open('images/img.jpg', 'rb'), caption=response, reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Извините, произошла ошибка.')


def registration():
    pass


def command_messages(bot, message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Введите название лекарства, а бот выдаст его цену и наличие в аптеках.')
    if message.text == '/help':
        bot.send_message(message.from_user.id, '/set_city')
    if message.text == '/set_city':
        bot.send_message(message.from_user.id, 'Введите нужный Вам город.')
