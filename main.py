import telebot
from telebot import types
import requests
from urllib.error import HTTPError
from urllib.request import urlopen, Request
import json

bot = telebot.TeleBot('5829632205:AAF4h136vOa2_VjL3EWoLInYZLR5XDqHdT0')
base_address = 'https://tabservertest.azurewebsites.net/'


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'group':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Bot info', callback_data='info'),
                   types.InlineKeyboardButton('Website', url='https://www.youtube.com/c/STERNENKO'),
                   types.InlineKeyboardButton('My chats', callback_data='my_chats'))
        bot.send_message(message.chat.id, 'Hello. This bot designed only for groups', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == 'info':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Bot info', callback_data='info'),
                   types.InlineKeyboardButton('Website', url='https://www.youtube.com/c/STERNENKO'),
                   types.InlineKeyboardButton('My chats', callback_data='my_chats'))
        bot.send_message(call.message.chat.id, 'This bot can help you detect ads in your group.'
                                               ' Just add this bot to a group and give it admin rights.',
                         reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                              text='Hello. This bot designed only for groups')
    if call.data == 'my_chats':
        admins = requests.get(base_address + 'admin/chat')
        print(admins.json())
        for admin in admins.json():
            print(admin)


@bot.message_handler(content_types=['text'])
def save_message(message):
    admins = bot.get_chat_administrators(message.chat.id)
    admins_list = []
    for admin in admins:
        if not admin.user.is_bot:
            admins_list.append({'id': int(admin.user.id)})
    user_payload = {
        'id': int(message.from_user.id),
        'username': str(message.from_user.username)
    }
    group_payload = {
        'id': int(message.chat.id),
        'name': str(message.chat.title)
    }
    admin_chat_payload = {
        "id": int(message.chat.id),
        "title": str(message.chat.title),
        "admins": admins_list
    }
    print(requests.post(base_address + 'users/post', json=user_payload))
    print(requests.post(base_address + 'groups/post', json=group_payload))
    print(requests.post(base_address + 'admin/chat', json=admin_chat_payload))
    data = {
        "Inputs": {
            "input1":
                {
                    "ColumnNames": ["classification", "message"],
                    "Values": [["cls", "This text does not mean something. It is just test"]]
                }, }
    }
    body = str.encode(json.dumps(data))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/58e9e3b82bb947969b868e658dc33c78/services/61a5d322aafd4568913f440ea63ae193/execute?api-version=2.0&details=true'
    api_key = 'AfyEav8arcErW4IW/MWNskbbCZAO3CE+ZBXINzpvsAX7jBLLZ2t/qgqNFPk70nyo8eCjDKIdUyOm+AMC6WoreA=='
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = Request(url, body, headers)
    try:
        result = json.loads(urlopen(req).read().decode("utf-8"))
        if result['Results']['output1']['value']['Values'][0][1] == 'Spam':
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'A message seems to contain an advertisement!')
    except HTTPError as error:
        print(error.info())


if __name__ == '__main__':
    bot.polling(none_stop=True)
