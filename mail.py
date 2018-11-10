#!/usr/bin/python
import re
import json
import sys
import base64
import mailparser   # https://pypi.org/project/mail-parser/
import requests     # http://docs.python-requests.org/en/master/

users = {
            'SENDER_EMAIL_ADDRESS1':
                {
                    'BotApiKey' : 'BOT_API_KEY',
                    'chat_id' : 'USER_ID'
                },
            'SENDER_EMAIL_ADDRESS2':
                {
                    'BotApiKey' : 'BOT_API_KEY',
                    'chat_id' : 'USER_ID'
                }
#            'default':
#                {
#                    'BotApiKey' : 'BOT_API_KEY',
#                    'chat_id' : 'USER_ID'
#                }
        }

# https://core.telegram.org/bots/api#sendmessage
def sendMessage(chat_id, text):
    params = (
                    ('chat_id', chat_id),
                    ('disable_web_page_preview', '1'),
                    ('text', text),
                    ('parse_mode', 'Markdown')
             )

    response = requests.get(url+"/sendMessage", params=params)
    print(response.json())

# https://core.telegram.org/bots/api#sendphoto
#def sendPhoto():
#    params = (
#                    ('chat_id', chat_id),
#                    ('text', text),
#             )
#
#    response = requests.get(url+"/sendPhoto", params=params)
#    print(response.json())

# https://core.telegram.org/bots/api#sendmediagroup
def sendMediaGroup(chat_id, photos):

    media = []
    files = {}

    for photo in photos:
        media.append( { 'type' : 'photo', 'media' : "attach://"+photo['filename'] } )
        files.update( { photo['filename'] : photo['data'] } )

    params = (
                ('chat_id', chat_id),
                ('media', json.dumps(media))
             )

    if len(media) > 0:
        response = requests.post(url+"/sendMediaGroup", params=params, files=files)
        print(response.json())
    else:
        print("Nothing to send. Skip REST call.")

# Parase RAW email from STDIN
mail = mailparser.parse_from_file_obj(sys.stdin)

print(mail.from_)
print(mail.delivered_to)
print(mail.to)
#print(mail.body)

# Determine Telegram Bot API key and ID of the user who will get the message we will send
try:
    key = mail.from_[0][1]
    #user_key = re.search('\+(.+?)\@', key).group(1) # use +something part in the sender's email address as key
    user_key = key # use sender's email address as key
except AttributeError:
    print("Use default user key (if set)")
    user_key = 'default'

try:
    BotApiKey = users[user_key]['BotApiKey']
    chat_id = users[user_key]['chat_id']
    url="https://api.telegram.org/bot"+BotApiKey
except KeyError:
    print("Unknown key found! " + key)
    sys.exit()

print("user key: " + user_key)
print("bot api key: " + BotApiKey)
print("chat id: " + chat_id)

message = mail.body
photos = []

for attachement in mail.attachments:
    #binary, mail_content_type, payload, filename, content_transfer_encoding, content-id
    if attachement["mail_content_type"] == "image/jpeg":
        data = bytearray(base64.b64decode(attachement["payload"]))
        photos.append( { 'filename' : attachement["filename"], 'data' : data } )

# Send to Telegram
sendMediaGroup(chat_id, photos)
sendMessage(chat_id, message)

