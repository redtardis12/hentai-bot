from flask import Flask, request, json
import os
import vk_api
import random
from random import randint
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


vk = vk_api.VkApi(token="group token")   # token of group in vk settings

def photo(user_id, photo_name, folder_id, b_message):  # sending photos function - takes 4 arguments: chat's id, name of file, id of google drive folder (url), text of message
    try:
        file1 = drive.CreateFile({'parents': [{'id': folder_id}]})  # creating object in google drive folder
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()  # getting the list of files in folder
        for file1 in file_list:  # searching for file
            if file1['title'] == photo_name:
                file1.GetContentFile(photo_name)  # downloading a file on host server with bot itself from google drive
        a = vk.method("photos.getMessagesUploadServer", {"peer_id": user_id})
        b = requests.post(a['upload_url'], files={'photo': open(photo_name, 'rb')}).json()
        c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]  # uploading the file on vk server
        d = 'photo{}_{}'.format(c['owner_id'], c['id'])  # sending a message with file attachment
        vk.method('messages.send', {'peer_id': user_id, "message": b_message, 'attachment': d, "random_id": random.randint(1, 2147483647)})
        os.remove(photo_name)  # removing a photo from host server
    except:  # throw an error in case of missing file with users warning
        vk.method("messages.send", {"peer_id": user_id, "message": "Упс, кажется что-то пошло не так!", "random_id": random.randint(1, 2147483647)})

app = Flask(__name__)  # initiation flask app

@app.route('/', methods = ["POST"])  # getting data from vk events
def main():  # main bot's function
    data = json.loads(request.data)
    if data["type"] == "confirmation":
        return "secret code"  # server must return special code to add a bot and make it work
    elif data["type"] == "message_new":  # getting new message (in chat and personal messages at the same time, for sending messages too)
        object = data["object"]  # object of a message
        id = object["peer_id"]  # id where to send
        body = object["text"]  # text of the message
        if body.lower() == "!привет":  # commands
            if object["from_id"] == 345145438:  # checking id of sender
               vk.method("messages.send", {"peer_id": id, "message": "Привет, создатель! &#128525; &#128525; &#128525;", "random_id": random.randint(1, 2147483647)})
            elif object["from_id"] == 398033132:
                vk.method("messages.send", {"peer_id": id, "message": "Приветик, братек &#128540;", "random_id": random.randint(1, 2147483647)})
            elif object["from_id"] == 344782276:
                vk.method("messages.send", {"peer_id": id, "message": "Привет... Как мне к тебе обращаться? Тян или кун? Я немного запуталась..", "random_id": random.randint(1, 2147483647)})
            else:
                vk.method("messages.send", {"peer_id": id, "message": "Привет, сенпай! &#128524;", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == '!список команд':
            vk.method("messages.send", {"peer_id": id, "message": "Список команд для тебя, сенпай! &#128540;\n 1. !привет - моё приветствие\n2. !хентай - классический хентай\n3. !лоли - миленькие лоли\n4. !милф - хентай с милфами\n5. !фут - фут фетиш\n6. !фурри - пушистые фурри\n7. !неко - милые кошкодевочки\n8. !тенткл - хентай с щупальцами\n9. !фута - футанари\n 10. !трап - хентай с трапами", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == '!хентай':
            photo(object["peer_id"], 'a{}.jpg'.format(randint(1,204)), '1bxxme1LEziESois_OFJ-jnlzuJo_SNOi', 'ммм &#129316;')
        elif body.lower() == '!лоли':
            photo(object["peer_id"], 'b{}.jpg'.format(randint(1,19)), '1cyaWmV4PCdPRh7k_66mo1K1IMlS1Ijlx', 'она уже взрослая, нравится тебе это или нет! &#128544;')
        elif body.lower() == '!милф':
            photo(object["peer_id"], 'c{}.jpg'.format(randint(1,3)), '1WWkiXjX54_LNnoCO-6bjUxUdzug2erW-', 'мне ещё долго до неё расти... &#128553;')
        elif body.lower() == '!фут':
            photo(object["peer_id"], 'd{}.jpg'.format(randint(1,3)), '1g1zz6VsledcbhuMB2AvtlDxWMrJBQC77', 'ножки &#128525;')
        elif body.lower() == '!фурри':
            photo(object["peer_id"], 'e{}.jpg'.format(randint(1,2)), '17Ur0JWj8lHDtd-0O0wVS68OYizTKG7h_', 'люблю зверушек &#128535;')
        elif body.lower() == '!неко':
            photo(object["peer_id"], 'f{}.jpg'.format(randint(1,6)), '1kquzNKSy0DyTcR52JvgvEa-wXWvaTdkq', 'котики &#128522;')
        elif body.lower() == '!тенткл':
            photo(object["peer_id"], 'g{}.jpg'.format(randint(1,10)), '1mwF7c0roU8Eo8DTN8l-TdWVc-iDLxxJy', 'они лезут отовсюду! &#128534;')
        elif body.lower() == '!фута':
            photo(object["peer_id"], 'h{}.jpg'.format(randint(1,2)), '1uQgWGsyI8iebenjUb1PYXoFq-k6c3N8p', 'они большие! &#128534;')
        elif body.lower() == '!трап':
            photo(object["peer_id"], 't{}.jpg'.format(randint(1,75)), '1rZreiRJc2NamG3zS28XeNPt7vlXtfcOR', '&#9786;')
    return "ok"  # after every action server must return 'ok' string