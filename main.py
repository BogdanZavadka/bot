import telebot
from telebot import types
import psycopg2

bot = telebot.TeleBot('5728154756:AAE6bRH8TuCDACbrUkxHBidCwPd348MyAtY')
host = "ella.db.elephantsql.com"
user = "yxqfwklx"
password = "cWmYO0EkdU_nDVvGgWXKsJEf4RQLSR8F"
db_name = "yxqfwklx"


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'group':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Bot info', callback_data='info'),
                   types.InlineKeyboardButton('Website', url='https://www.youtube.com/c/STERNENKO'))
        bot.send_message(message.chat.id, 'Hello. This bot designed only for groups', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == 'info':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Bot info', callback_data='info'),
                   types.InlineKeyboardButton('Website', url='https://www.youtube.com/c/STERNENKO'))
        bot.send_message(call.message.chat.id, 'This bot can help you detect ads in your group.'
                         ' Just add this bot to a group and give it admin rights.', reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                              text='Hello. This bot designed only for groups')


@bot.message_handler(content_types=['text'])
def save_message(message):
    if 'https' in message.text or 'http' in message.text or '.com' in message.text:
        bot.send_message(message.chat.id, message)
        bot.send_message(message.chat.id, f'@{message.from_user.username}, your message seem to contain a link',
                         reply_to_message_id=message.id)
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        group_ids = []
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT group_id FROM tg_group;')
                group_ids = cursor.fetchall()
                print(group_ids)
        except Exception as ex:
            print('Error ', ex)

        try:
            with connection.cursor() as cursor:
                if not group_ids:
                    cursor.execute(f"INSERT INTO tg_group VALUES ('{message.chat.id}', '{message.chat.title}');")
                cursor.execute(f'INSERT INTO tg_user(user_id, username) VALUES ({message.from_user.id}, '
                               f"'{message.from_user.username}');")
                cursor.execute(
                    f"INSERT INTO tg_message VALUES ({message.id}, '{message.text}', {message.chat.id}, "
                    f"{message.from_user.id});")
                connection.commit()
                # cursor.execute('SELECT * FROM test_table;')
                # a = cursor.fetchall()
                # b = ''
                # for i in a:
                #     b += str(i)
                # print(b)
                # bot.send_message(message.chat.id, b)
        except Exception as _ex:
            print("[INFO] Error", _ex)
        connection.close()


bot.polling(none_stop=True)
