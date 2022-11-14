import telebot
from telebot import types
import requests

bot = telebot.TeleBot('5728154756:AAE6bRH8TuCDACbrUkxHBidCwPd348MyAtY')
host = "ella.db.elephantsql.com"
user = "yxqfwklx"
password = "cWmYO0EkdU_nDVvGgWXKsJEf4RQLSR8F"
db_name = "yxqfwklx"

base_adress = 'https://glacial-earth-93029.herokuapp.com/'


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
                                               ' Just add this bot to a group and give it admin rights.',
                         reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                              text='Hello. This bot designed only for groups')


@bot.message_handler(content_types=['text'])
def save_message(message):
    if 'https' in message.text or 'http' in message.text or '.com' in message.text:
        bot.send_message(message.chat.id, f'@{message.from_user.username}, your message seems to contain a link',
                         reply_to_message_id=message.id)
        name = message.from_user.first_name + ' ' + str(message.from_user.last_name)
        user_payload = {
            'userId': int(message.from_user.id),
            'name': str(name),
            'username': str(message.from_user.username),
            'phoneNumber': 'None'
        }
        group_payload = {
            'groupId': int(message.chat.id),
            'name': str(message.chat.title)
        }
        message_payload = {
            'messageId': int(message.message_id),
            'isAdvertisement': 'null',
            'messageBody': str(message.text),
            'sendDate': message.date,
            'group': {
                'groupId': int(message.chat.id),
                'name': str(message.chat.title)
            },
            'user': {
                'userId': int(message.from_user.id),
                'name': str(name),
                'username': str(message.from_user.username),
                'phoneNumber': 'null'
            }
        }
        print(requests.post(base_adress + 'users/', json=user_payload))
        print(requests.post(base_adress + 'groups/', json=group_payload))
        print(requests.post(base_adress + 'messages/', json=message_payload))


bot.polling(none_stop=True)
