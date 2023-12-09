import telebot
import settings as st
import bot_functions as bf


bot = telebot.TeleBot(st.BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text not in st.BOT_COMMAND_LIST:
        object_url = bf.find_url(message.text)
        response = bf.parce_information_for_bot(object_url)
        bf.get_url_to_img(object_url)
        bot.send_photo(message.from_user.id, open('images/img.jpg', 'rb'), caption=response)
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Введите название лекарства, а бот выдаст его цену и наличие в аптеках.')
    bf.load_logs(message)


bot.polling(none_stop=True, interval=0)
