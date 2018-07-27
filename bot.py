import json
import requests
import time
import urllib


from dbConnection import DBHelper

TOKEN = '535790419:AAFRBVqpDbw81agwWROi2BM410wR_AkUW3Y'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

"""
Database connection for mysql
database = 'absen_bot'
usernama = 'root'
password = 'mysql'
host = 127.0.0.1/localhost
"""
db = DBHelper('absen_bot', 'root', 'mysql', '127.0.0.1')


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        first_name = update["message"]["from"]["first_name"]
        chat = update["message"]["chat"]["id"]
        # items = db.get_data_karyawan(chat)
        txt = str(update['message']['text'])
        items = None

        if text == "/start":
            msg = "Halo " + first_name + " jika ingin ke menu /menu"
            # msg += "1. "
            send_message(msg, chat)

        elif text == "/menu":
            msg = "Daftar Key Word:\n"
            msg += "1. /list lihat daftar seluruh karyawan\n"
            msg += "2. /masuk <id> cari data karyawan\n"
            msg += "3. /detail <id> menampilkan detail karyawan\n"

            send_message(msg, chat)
        elif text == "/list":
            items = db.get_count()
            msg = ""
            for i in items:
                msg += "Nama: " + str(i[0]) + "\nJumlah Masuk: " + str(i[2]) + "\n\n"
            send_message(msg, chat)

        elif text == '/masuk '+txt[-1]:
            id_data = txt[-1]
            items = db.search_data(id_data)            
            msg = ""

            for i in items:
                msg += "Nama: " + str(i[0]) + "\nJumlah Masuk: " + str(i[2]) + "\n\n"

            send_message(msg, chat)

        elif text == '/detail '+txt[-1]:
            id_data = txt[-1]
            items = db.get_detail_karyawan(id_data)
            msg = ""

            for i in items:
                msg += "NIK: " + str(i[0])  
                msg += "\nNama: " + str(i[1]) 
                msg += "\nAlamat: " + str(i[2]) 
                msg += "\nKode Pos: " + str(i[3]) 
                msg += "\nJenis Kelamin: " + str(i[4])

            send_message(msg, chat)

        elif text == '/detail':
            msg = " tambahkan id karyawan dipisah menggunakan spasi(ex. /karyawan 1)"
            send_message(msg, chat)

        elif text == '/masuk':
            msg = " tambahkan id karyawan dipisah menggunakan spasi(ex. /search 1)"
            send_message(msg, chat)

        elif text == 'test':
            msg = first_name
            send_message(msg, chat)

        else:
            msg = "Pesan tidak dapat dimengerti"
            send_message(msg, chat)

        """        
        elif text.startswith("/"):
            msg = "Kata kunci salah"
            send_message(msg, chat)
        
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        
        elif text == "/start":
            send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", chat)
            # response = 
        
        elif text.startswith("/"):
            continue
        
        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        
        else:
            db.add_item(text, chat)
            items = db.get_items(chat)
            message = "\n".join(items)
            send_message(message, chat)
        """


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    # db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
