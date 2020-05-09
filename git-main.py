import vk_api
import vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import json
import os
import requests
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from random import *

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)  # main google drive api object - !important


vk_session = vk_api.VkApi(token='group token here') # token of group in vk settings
longpoll = VkBotLongPoll(vk_session, group_id)  # group_id - id number of your group mast be placed here
ls = vk_session.get_api()  # main vk api object - !important

def photo(user_id, photo_name, folder_id, b_message):  # sending photos in chat function - takes 4 arguments: chat's id, name of file, id of google drive folder (url), text of message
    try:
        file1 = drive.CreateFile({'parents': [{'id': folder_id}]})  # creating object in google drive folder
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList() # getting the list of files in folder
        for file1 in file_list:  # searching for file
            if file1['title'] == photo_name:
                file1.GetContentFile(photo_name)  # downloading a file on host server with bot itself from google drive

        a = vk_session.method("photos.getMessagesUploadServer") 
        b = requests.post(a['upload_url'], files={'photo': open(photo_name, 'rb')}).json()
        c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0] # uploading the file on vk server
        ls.messages.send(
            chat_id=user_id,  # to whom send the message
            random_id=get_random_id(), # a special random id for every message (let vk generate by itself)
            message=b_message, # the text of message
            attachment = f'photo{c["owner_id"]}_{c["id"]}' # file attachment
        )  # sending a message with file attachment
        os.remove(photo_name)  # removing a photo from host server
    except:  # throw an error in case of missing file with users warning
        ls.messages.send(chat_id=user_id, random_id=get_random_id(), message='Упс, кажется что-то пошло не так...')
        print(photo_name)

def photo_ls(user_id, photo_name, folder_id, b_message):  # the same file sending function but for personal messages (changed only vk id option)
    try:
        file1 = drive.CreateFile({'parents': [{'id': folder_id}]})
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
        for file1 in file_list:
            if file1['title'] == photo_name:
                file1.GetContentFile(photo_name)

        a = vk_session.method("photos.getMessagesUploadServer")
        b = requests.post(a['upload_url'], files={'photo': open(photo_name, 'rb')}).json()
        c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
        ls.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=b_message,
            attachment = f'photo{c["owner_id"]}_{c["id"]}'
        )
        os.remove(photo_name)
    except:
        ls.messages.send(user_id=user_id, random_id=get_random_id(), message='Упс, кажется что-то пошло не так...')

def main():  # main bot's function
    for event in longpoll.listen():  # registering vk events
        if event.type == VkBotEventType.MESSAGE_NEW:  # if we got a new message
            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.obj.from_id)
            print('Текст:', event.obj.text)
            print()  # printing on console (not necessary, just for debugging)
            if event.from_user:  # if message from personal vk messages
                if event.obj.text == '!привет':  # '!привет' command
                    if event.obj.from_id == 111:
                        ls.messages.send(user_id=event.obj.from_id, random_id=get_random_id(), message='Привет, создатель! &#128525; &#128525; &#128525;')
                    elif event.obj.from_id == 112:
                        ls.messages.send(user_id=event.obj.from_id, random_id=get_random_id(), message='Приветик, Антон &#128540;')
                    elif event.obj.from_id == 113:
                        ls.messages.send(user_id=event.obj.from_id, random_id=get_random_id(), message='Признайся, ты трап?) &#128540;')
                    else:
                        ls.messages.send(user_id=event.obj.from_id, random_id=get_random_id(), message='Привет, сенпай! &#128524;') # bot has different reaction on different users (ids not real!!!)
                elif event.obj.text == '!список команд':
                    ls.messages.send(user_id=event.obj.from_id, random_id=get_random_id(), message='Список команд для тебя, сенпай! &#128540;\n 1. !привет - я с вами поздоровуюсь\n2. !хентай - классический хентай\n3. !лоли - миленькие лоли\n4. !милф - хентай с милфами\n5. !фут - фут фетиш\n6. !фурри - пушистые фурри\n7. !неко - милые кошкодевочки\n8. !тенткл - хентай с щупальцами\n9. !фута - футанари\n 10. !трап - хентай с трапами')
                elif event.obj.text == '!хентай':
                    photo_ls(event.obj.from_id, 'a{}.jpg'.format(randint(1,204)), '1bxxjnlzuJo_SNOi', 'ммм &#129316;')
                elif event.obj.text == '!лоли':
                    photo_ls(event.obj.from_id, 'b{}.jpg'.format(randint(1,19)), '1cyaWmV1K1IMlS1Ijlx', 'она уже взрослая, нравится тебе это или нет! &#128544;')
                elif event.obj.text == '!милф':
                    photo_ls(event.obj.from_id, 'c{}.jpg'.format(randint(1,2)), '1WWkiXjXzug2erW-', 'мне ещё долго до неё расти... &#128553;')
                elif event.obj.text == '!фут':
                    photo_ls(event.obj.from_id, 'd{}.jpg'.format(randint(1,3)), '1g1zz6VslrJBQC77', 'ножки &#128525;')
                elif event.obj.text == '!фурри':
                    photo_ls(event.obj.from_id, 'e{}.jpg'.format(randint(1,2)), '17Ur0JOYizTKG7h_', 'люблю зверушек &#128535;')
                elif event.obj.text == '!неко':
                    photo_ls(event.obj.from_id, 'f{}.jpg'.format(randint(1,2)), '1kquzwXWvaTdkq', 'котики &#128522;')
                elif event.obj.text == '!тенткл':
                    photo_ls(event.obj.from_id, 'g{}.jpg'.format(randint(1,3)), '1mwF7c0c-iDLxxJy', 'они лезут отовсюду! &#128534;')
                elif event.obj.text == '!фута':
                    photo_ls(event.obj.from_id, 'h{}.jpg'.format(randint(1,2)), '1uQg-k6c3N8p', 'они большие! &#128534;')
                elif event.obj.text == '!трап':
                    photo_ls(event.obj.from_id, 't{}.jpg'.format(randint(1,75)), '1rZNPt7vlXtfcOR', '&#9786;')  
#  others commands with random photo attachment using randint with interval = quantity of images in google drive folder
            elif event.from_chat:  # the same, but if the messages from chat
                if event.obj.text == '!привет':
                    if event.obj.from_id == 345145438:
                        ls.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Привет, создатель! &#128525; &#128525; &#128525;')
                    elif event.obj.from_id == 398033132:
                        ls.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Приветик, братек &#128540;')
                    elif event.obj.from_id == 344782276:
                        ls.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Признайся, ты трап?) &#128540;')
                    else:
                        ls.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Привет, сенпай! &#128524;')
                elif event.obj.text == '!список команд':
                    ls.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='Список команд для тебя, сенпай! &#128540;\n 1. !привет - я с вами поздоровуюсь\n2. !хентай - классический хентай\n3. !лоли - миленькие лоли\n4. !милф - хентай с милфами\n5. !фут - фут фетиш\n6. !фурри - пушистые фурри\n7. !неко - милые кошкодевочки\n8. !тенткл - хентай с щупальцами\n9. !фута - футанари\n 10. !трап - хентай с трапами')
                elif event.obj.text == '!хентай':
                    photo(event.chat_id, 'a{}.jpg'.format(randint(1,204)), '1bxxzuJo_SNOi', 'ммм &#129316;')
                elif event.obj.text == '!лоли':
                    photo(event.chat_id, 'b{}.jpg'.format(randint(1,19)), '1cyaWlS1Ijlx', 'она уже взрослая, нравится тебе это или нет! &#128544;')
                elif event.obj.text == '!милф':
                    photo(event.chat_id, 'c{}.jpg'.format(randint(1,2)), '1WWkidzug2erW-', 'мне ещё долго до неё расти... &#128553;')
                elif event.obj.text == '!фут':
                    photo(event.chat_id, 'd{}.jpg'.format(randint(1,3)), '1g1zrJBQC77', 'ножки &#128525;')
                elif event.obj.text == '!фурри':
                    photo(event.chat_id, 'e{}.jpg'.format(randint(3,4)), '17Ur0YizTKG7h_', 'люблю зверушек &#128535;')
                elif event.obj.text == '!неко':
                    photo(event.chat_id, 'f{}.jpg'.format(randint(1,2)), '1kquzNKSXWvaTdkq', 'котики &#128522;')
                elif event.obj.text == '!тенткл':
                    photo(event.chat_id, 'g{}.jpg'.format(randint(1,3)), '1mwF7c0rWVc-iDLxxJy', 'они лезут отовсюду! &#128534;')
                elif event.obj.text == '!фута':
                    photo(event.chat_id, 'h{}.jpg'.format(randint(1,2)), '1uQgWGsyIk6c3N8p', 'они большие! &#128534;')
                elif event.obj.text == '!трап':
                    photo(event.chat_id, 't{}.jpg'.format(randint(1,75)), '1rZrt7vlXtfcOR', '&#9786;')
if __name__ == '__main__':  # running bot's main function
    while True: 
        try:
            main()
        except:
            continue  # !important for constant bot's work, even it is doing nothing
