from flask import Flask, request, json
import os
import vk_api
from vk_api.utils import get_random_id
import random
import requests
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth() 
gauth.LoadCredentialsFile("mycreds.txt")  # Try to load saved client credentials
if gauth.credentials is None:
    gauth.LocalWebserverAuth()  # Authenticate if they're not there
elif gauth.access_token_expired:
    gauth.Refresh()  # Refresh them if expired
else:
    gauth.Authorize()  # Initialize the saved creds
gauth.SaveCredentialsFile("mycreds.txt")  # Save the current credentials to a file
drive = GoogleDrive(gauth)

vk = vk_api.VkApi(token="group token")  # token of group in vk settings

def photo(user_id, photo_name_s, folder_id, b_message):  # sending photos function - takes 4 arguments: chat's id, random file id, id of google drive folder (url), text of message

    try:
        file1 = drive.CreateFile({'parents': [{'id': folder_id}]})  # creating object in google drive folder
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()  # getting the list of files in folder
        photo_name = '{}{}.jpg'.format(photo_name_s, random.randint(1, len(file_list)))  # getting name of file from max files in folder
        for file1 in file_list:
            if file1['title'] == photo_name:
                file1.GetContentFile(photo_name)
        a = vk.method("photos.getMessagesUploadServer", {"peer_id": user_id})
        b = requests.post(a['upload_url'], files={'photo': open(photo_name, 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
        d = 'photo{}_{}'.format(c['owner_id'], c['id'])
        vk.method('messages.send', {'peer_id': user_id, "message": b_message, 'attachment': d, "random_id": get_random_id()})
        os.remove(photo_name)
    except:
        vk.method("messages.send", {"peer_id": user_id, "message": "Упс, кажется что-то пошло не так!", "random_id": get_random_id()})


def video_sent(user_id, ran):  # video sent function takes 2 arguments: chat id and random value 
    vlist = open('videos.txt', 'r')  # file with videos' urls
    for i, line in enumerate(vlist):  # searching line with url
        line = line.replace("\n", "")
        if i == ran:
            try:
                vk.method("messages.send", {"peer_id": user_id, "message":"Твоё видео, сенпай!&#128538;\n" + str(line), "random_id": get_random_id()})
            except:
                vk.method("messages.send", {"peer_id": user_id, "message": "Упс, кажется что-то пошло не так!", "random_id": get_random_id()})

app = Flask(__name__)  # initiation flask app

@app.route('/', methods = ["POST"])  
def main():  # main bot's function
    data = json.loads(request.data)  # getting data from vk events
    if data["type"] == "confirmation":
        return "secret code"  # server must return special code to confirm server
    elif data["type"] == "message_new":  # getting new message (in chat and direct messages at the same time, for sending messages too)
        object = data["object"]  # object of a message
        id = object["peer_id"]  # id where to send
        body = object["text"]  # text of the message
        if body.lower() == "!привет":
            if object["from_id"] == some_id_1:  # checking id of sender
               vk.method("messages.send", {"peer_id": id, "message": "Привет, создатель! &#128525; &#128525; &#128525;", "random_id": get_random_id()})
            elif object["from_id"] == some_id_2:
                vk.method("messages.send", {"peer_id": id, "message": "Приветик, братек &#128540;", "random_id": get_random_id()})
            elif object["from_id"] == some_id_3:
                vk.method("messages.send", {"peer_id": id, "message": "Привет... Как мне к тебе обращаться? Тян или кун? Я немного запуталась..", "random_id": get_random_id()})
            else:
                vk.method("messages.send", {"peer_id": id, "message": "Привет, сенпай! &#128524;", "random_id": get_random_id()})
        elif body.lower() in ('!список', '! список', '!Список', '! Список'):
            vk.method("messages.send", {"peer_id": id, "message": "Список команд для тебя, сенпай! &#128540;\n !привет - моё приветствие\n!хентай - классический хентай\n!лоли - миленькие лоли\n!милф - хентай с милфами\n!фут - фут фетиш\n!фурри - пушистые фурри\n!неко - милые кошкодевочки\n!тентакл - хентай с щупальцами\n!фута - футанари\n!трап - хентай с трапами\n!видео - видосик с хентаем", "random_id": get_random_id()})
        elif body.lower() in ('!хентай', '! хентай', '!Хетнай', '! Хентай'):
            photo(object["peer_id"], 'a', '1bxxme1LEziESois_OFJ-jnlzuJo_SNOi', 'ммм &#129316;')
        elif body.lower() in ('!лоли', '! лоли', '!Лоли', '! Лоли'):
            photo(object["peer_id"], 'b', '1cyaWmV4PCdPRh7k_66mo1K1IMlS1Ijlx', 'она уже взрослая, нравится тебе это или нет! &#128544;')
        elif body.lower() in ('!милф', '! милф', '!Милф', '! Милф'):
            photo(object["peer_id"], 'c', '1WWkiXjX54_LNnoCO-6bjUxUdzug2erW-', 'мне ещё долго до неё расти... &#128553;')
        elif body.lower() in ('!фут', '! фут', '!Фут', '! Фут'):
            photo(object["peer_id"], 'd', '1g1zz6VsledcbhuMB2AvtlDxWMrJBQC77', 'ножки &#128525;')
        elif body.lower() in ('!фурри', '! фурри', '!Фурри', '! Фурри'):
            photo(object["peer_id"], 'e', '17Ur0JWj8lHDtd-0O0wVS68OYizTKG7h_', 'люблю зверушек &#128535;')
        elif body.lower() in ('!неко', '! неко', '!Неко', '! Неко'):
            photo(object["peer_id"], 'f', '1kquzNKSy0DyTcR52JvgvEa-wXWvaTdkq', 'котики &#128522;')
        elif body.lower() in ('!тентакл', '! тентакл', '!Тентакл', '! Тентакл'):
            photo(object["peer_id"], 'g', '1mwF7c0roU8Eo8DTN8l-TdWVc-iDLxxJy', 'они лезут отовсюду! &#128534;')
        elif body.lower() in ('!фута', '! фута', '!Фута', '! Фута'):
            photo(object["peer_id"], 'h', '1uQgWGsyI8iebenjUb1PYXoFq-k6c3N8p', 'они большие! &#128534;')
        elif body.lower() in ('!трап', '! трап', '!Трап', '! Трап'):
            photo(object["peer_id"], 't', '1rZreiRJc2NamG3zS28XeNPt7vlXtfcOR', '&#9786;')
        elif body.lower() in ('!видео', '! видео', '!Видео', '! Видео'):
            video_sent(object["peer_id"], random.randint(0,34))
    return "ok"
