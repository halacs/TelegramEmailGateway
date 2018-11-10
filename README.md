# Goal
The doal of this project is to forward notification emails comming from security cameras to a specific Telegram client.

# Environment
* Postfix
* Python 2.7.15rc1

# How to use
## Configure your Posfix server
You need to configure your Postfix server to pipe incomming emails into this script's standard input stream.

TODO: how?

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
