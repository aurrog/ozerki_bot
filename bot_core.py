import telebot
import settings as st
import bot_functions as bf


bot = telebot.TeleBot(st.BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text not in st.BOT_COMMAND_LIST:
        response = bf.parce_information_for_bot(bf.find_url(message.text))
        bot.send_message(message.from_user.id, response)
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Введите название лекарства, а бот выдаст его цену и наличие в аптеках.')
    bf.load_logs(message)


bot.polling(none_stop=True, interval=0)
