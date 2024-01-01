import json
import time
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyUnregisteredError
from config import *
import itertools
import random
import base64

# Функция для преобразования байтов в base64
def bytes_to_base64(value):
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('utf-8')
    return value

def search_queries(count_symbol=2):
    alphabets = [
        "qwertyuiopasdfghjklzxcvbnm",
        "йцукенгшщзхъёфывапролджэячсмитьбю",
        "1234567890",
    ]

    for alphabet in alphabets:
        for pair in itertools.permutations(alphabet, count_symbol):
            yield "".join(pair)
            
api_id = API_ID
api_hash = API_HASH 
with TelegramClient('name', API_ID, API_HASH, system_version="4.16.30-vxCUSTOM") as client:
    try:
        participants = {}
        channel_name = CHANNEL_NAME
        for query in search_queries(1):
            print(query)
            try:
                for res in client.iter_participants(channel_name, search=query): 
                    res_dict = res.to_dict()
                    for k,v in res_dict.items():
                        res_dict[k] = str(v)
                    participants[res.id] = res_dict
                    print(f'{res.id}|{res.first_name}|{res.last_name}|{res.username}')
            except Exception as e:
                client.disconnect()
                print(f"Ошибка при получении участников: {e}")
            time.sleep(random.random() * 3)
            
        for query in search_queries(2):
            print(query)
            try:
                for res in client.iter_participants(channel_name, search=query): 
                    res_dict = res.to_dict()
                    for k,v in res_dict.items():
                        res_dict[k] = str(v)
                    participants[res.id] = res_dict
                    print(f'{res.id}|{res.first_name}|{res.last_name}|{res.username}')
            except Exception as e:
                client.disconnect()
                print(f"Ошибка при получении участников: {e}")
            time.sleep(random.random() * 3)        

        try:
            with open(f'{CHANNEL_NAME.split("/")[-1]}_subs.json', 'w', encoding="utf-8") as json_file:
                json.dump(participants, json_file, ensure_ascii=False, indent=4)
            print(f'Файл {CHANNEL_NAME.split("/")[-1]}_subs.json успешно записан')
        except Exception as ex:
            print('Не удалось верно записать json', ex)

        try:
            for k, v in participants.items():
                with open(f'{CHANNEL_NAME.split("/")[-1]}_subs.txt', 'a', encoding="utf-8") as f:
                    f.write(f"{v['first_name']}|{v['last_name']}|https://t.me/{v['username']}\n")
            print(f'Файл {CHANNEL_NAME.split("/")[-1]}_subs.txt успешно записан')
        except Exception as ex:
            print('Не удалось верно записать txt', ex)

        try:
            for k, v in participants.items():
                
                about = ''
                # try:
                #     user = client.get_entity(v['username'])
                #     about = user.about
                # except:
                #     pass
                with open(f'{CHANNEL_NAME.split("/")[-1]}_subs.md', 'a', encoding="utf-8") as f:
                    f.write(f"""## {v['first_name']} {v['last_name']}
#### https://t.me/{v['username']}
About:
{about}
(id:{k})
""")               
            print(f'Файл {CHANNEL_NAME.split("/")[-1]}_subs.md успешно записан')
        except Exception as ex:
            print('Не удалось верно записать md', ex)
        
    finally:
        client.disconnect()
        