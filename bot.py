import telebot
import src.settings as st
import src.system_functions as system_functions
import src.user_interactive as user_interactive


bot = telebot.TeleBot(st.BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text not in st.BOT_COMMAND_LIST:
        user_interactive.request_to_user(bot, message)
    else:
        user_interactive.command_messages(bot, message)
    system_functions.load_logs(message)
    system_functions.cache_clean()


bot.polling(none_stop=True, interval=0)
