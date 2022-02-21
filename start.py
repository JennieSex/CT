import vk_api, random as r, time
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

TOKEN = '' # токен по управлению бота
TOKENS = [
    ''

] # тут токены


STATUS = False # если будет True, то бот будет сразу работать
sleep = 60 # задержка в секундах
text = 'Ты зайка' # текст
peer = id # peer id лс/сообщества, куда отправлять текст


def START_LP():
    vk = vk_api.VkApi(token=TOKEN)
    lp = VkLongPoll(vk)


    def send_msg(peer, textsend, imgs='', ids=None):
        vk.method('messages.send', {
            'peer_id': peer,
            'random_id': r.randint(0, 2 ** 64),
            'disable_mentions': 0,
            'message': textsend,
            'attachment': imgs,
            'reply_to': ids})


    while True:
        try:
            for event in lp.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    global STATUS, sleep, peer, text
                    peer_id = event.peer_id
                    msg = event.text.lower()
                    if msg == '.ф стоп':
                        STATUS = False
                        send_msg(peer_id, '✅| остановлено')
                    if msg == '.ф старт':
                        STATUS = True
                        send_msg(peer_id, '✅| запущено')
                    if msg.startswith('.ф задержка'):
                        sleep = int(msg[12:])
                        send_msg(peer_id, f'✅| задержка теперь: {sleep}')
                    if msg.startswith('.ф текст'):
                        text = event.text[8:]
                        send_msg(peer_id, f'✅|, текст теперь: {text}')
        except Exception as ex:
            print(ex)


def START_SEND(tok): # функция отправки смс боту
    vk = vk_api.VkApi(token=tok)
    while True:
        global STATUS, sleep, peer, text
        if STATUS is True:
            try:
                vk.method("messages.send", {'message': text, 'random_id': r.randint(0, 2 ** 64), 'peer_id': peer})
                time.sleep(sleep)
            except:
                pass


for key in TOKENS:
    try:
        Thread(target=START_SEND, args=[key]).start() # запуск юзеров, которые будут писать боту
    except:
        pass

START_LP() # запуск LP
