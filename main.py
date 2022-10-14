import telebot
import psycopg2

bot = telebot.TeleBot('5728154756:AAE6bRH8TuCDACbrUkxHBidCwPd348MyAtY')
host = "ella.db.elephantsql.com"
user = "yxqfwklx"
password = "cWmYO0EkdU_nDVvGgWXKsJEf4RQLSR8F"
db_name = "yxqfwklx"


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'group':
        bot.send_message(message.chat.id, 'Add this bot to your chat')


@bot.message_handler(content_types=['text'])
def save_message(message):
    if 'https' in message.text or 'http' in message.text or '.com' in message.text:
        bot.send_message(message.chat.id, 'Your message contains a link', reply_to_message_id=message.id)
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO test_table (messag) VALUES ('{message.text}');"
                )
                connection.commit()
                # cursor.execute('SELECT * FROM test_table;')
                # a = cursor.fetchall()
                # b = ''
                # for i in a:
                #     b += str(i)
                # print(b)
                # bot.send_message(message.chat.id, b)
        except Exception as _ex:
            print("[NFO] Error", _ex)


bot.polling(none_stop=True)

