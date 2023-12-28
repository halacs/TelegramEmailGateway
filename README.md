# Goal
The doal of this project is to forward notification emails comming from security cameras to a specific Telegram client.

# Environment
* Postfix (tested on 3.6.4-1ubuntu1.1)
* Python (tested on 2.7.15rc1 and on 3.10.12)

# How to use
In the below config, `tobepiped@example.com` is used as the email address where security cameras can send emails. This email address must be properly configured on your postfix server. In the readme I won't descript how to do so, only the extra lines need to be added to use this script.

In this example config, if `sender-email-address@sender.example.com` is the sender of the email arrived to `tobepiped@example.com`, plain text email content and the attachements will be forwarded as Telegram message to the chat id given under the key of `chat_id`. `BotApiKey` is the key of your Telegram bot you want to send Telegram messages on behalf of.

## Configure Telegram bot credentials and forward map
```
users = {
            'sender-email-address@sender.example.com':
                {
                    'BotApiKey' : '[YOUR-TELEGRAMBOT-KEY]',
                    'chat_id' : '[YOUR-TELEGRAM-CHAT-ID-MESSAGE-WILL-BE-SENT]'
                },
#            'default':
#                {
#                    'BotApiKey' : '[YOUR-TELEGRAMBOT-KEY]',
#                    'chat_id' : '[YOUR-TELEGRAM-CHAT-ID-MESSAGE-WILL-BE-SENT]'
#                }
        }
```

## Configure your Posfix server
You need to configure your Postfix server to pipe incomming emails into the standard input of this script.

Edit `/etc/aliases` file to pipe incomming messages of `script@localhost` into `/root/mail.py`. Obviously, `/root/` is not the best location for `mail.py` so it is up to you where you want to store it.
```bash
# See man 5 aliases for format
#postmaster:    root
script: "|/root/mail.py"
```

Add below line to `/etc/postfix/virtual` file. Please note, that `tobepiped@example.com` needs to be your valid email address which will be piped into the script.
```bash
tobepiped@example.com script@localhost
```

Add below line to `/etc/postfix/main.cf` file:
```bash
virtual_alias_maps = hash:/etc/postfix/virtual
```

`virtual` needs to be compiled into berkeley db files:
```bash
postmap /etc/postfix/virtual
```

Finally postfix needs to be restarted to apply changes:
```bash
systemctl restart postfix
```

## Configure your forwarder script
* Download the python script
* Install mail-parser python library
```bash
 pip install mail-parser
 ```
* Install request python library
```bash
  pip install requests
```

# Links
* Telegram bot API: https://core.telegram.org/bots/api 
* mail-parser python library: https://pypi.org/project/mail-parser/
* requests python library: http://docs.python-requests.org/en/master/   
