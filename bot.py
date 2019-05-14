import constants
from time import sleep
from datetime import datetime
import requests
import _thread

URL = 'https://api.telegram.org/bot' + constants.TOKEN + '/'
chat_ids = set()
global last_update_id
last_update_id = 0


def get_updates():
    url = URL + 'getupdates'
    response = requests.get(url)
    return response.json()


def get_message():
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']
        message = {'chat_id': chat_id,
                   'text': message_text}
        return message
    return None


def send_message(chat_id, text='Wait a second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def add_user_listener():
    while True:
        answer = get_message()
        if answer is not None:
            chat_id = answer['chat_id']
            text = answer['text']

            if text == '/start':
                if chat_id in chat_ids:
                    send_message(chat_id, 'hiiiii again\njobStarted')
                else:
                    send_message(chat_id, 'hiiiii\njobStarted')
                    chat_ids.add(chat_id)

            elif text == '/end':
                if chat_id in chat_ids:
                    send_message(chat_id, 'byeeeeee\njobStoped')
                    chat_ids.remove(chat_id)
                else:
                    send_message(chat_id, 'byeeeeee again\njobStoped')

            else:
                send_message(chat_id)
                sleep(1)
                send_message(chat_id, 'not learn this yet :))')


def send_to_all():
    for chat_id in chat_ids:
        send_message(chat_id, 'سلام بچه ها\nرزرو غذا یادتون نره\n \n hey guys\ndont forget to reserve food:)')


def start():
    while True:
        day = datetime.today().weekday()  # Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
        hour = datetime.now().hour
        if day == 2 and 8 < hour < 9:
            send_to_all()
            sleep(60 * 60)
        sleep(60)


def main():
    send_message(62262733, 'start working...')
    _thread.start_new_thread(add_user_listener, ())
    _thread.start_new_thread(start, ())


if __name__ == '__main__':
    main()
