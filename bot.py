import json
import requests
import time
import urllib
import mysql.connector
import datetime
from mysql.connector import errorcode

from DBHandler import DBHandler

#TOKEN = '535790419:AAFRBVqpDbw81agwWROi2BM410wR_AkUW3Y'
TOKEN = '687645081:AAHPxLI1CM29sxIvGa730MiqjblJK-8wiV4'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

"""
Database connection for mysql
database = 'absen_bot'
usernama = 'root'
password = 'mysql'
host = 127.0.0.1/localhost
"""
db = DBHandler('absen_bot', 'root', 'mysql', '127.0.0.1')


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
        # txt = str(update['message']['text'])
        items = None

        if text == "/start":
            msg = "Halo " + first_name + " jika ingin ke menu /menu"
            send_message(msg, chat)

        elif text == "/help":
            msg = "Daftar Key Word:\n"
            msg += "1. /help lihat daftar seluruh karyawan\n"
            msg += "2. /absen format: /absen;kcontact\n"
            msg += "3. /register format: /register;spv;kcontact;nama\n"
            msg += "4. /rekap format: /rekap;kcontact;tahun;bulan\n"
            msg += "5. /rekap format: /rekap;spv;tahun;bulan\n"
            msg += "6. /rekap format: /rekap;sto\n"

            send_message(msg, chat)

        elif text == "/register":
            msg = "Format salah, klik /help untuk bantuan"
            send_message(msg, chat)

        elif text.startswith("/absen;"):
            a = text
            b = text.split(";")
            msg = ""

            if db.check_registered(b[1]):
                db.insert_absen(str(b[1]), str(datetime.datetime.now()))
                msg = "Anda telah absen tangga: " + str(datetime.datetime.now().day) + " pada jam: " +str(datetime.datetime.now().strftime("%H:%M"))
            else:
                msg = "Anda belum terdaftar"

            send_message(msg, chat)

        elif text.startswith("/register;"):
            a = text
            b = a.split(";")

            spv = b[1]
            kcontact = b[2]
            nama = b[3]

            msg = ""

            try:
                if db.check_registered(kcontact):
                    msg = "Anda sudah terdaftar"
                else:
                    db.insert_karyawan(kcontact, nama, spv.upper())
                    msg = "Anda berhasil terdaftar"

            except mysql.connector.Error as e:
                if e.errno == errorcode.ER_DUP_ENTRY:
                    print(e.msg)

            send_message(msg, chat)

        elif text.startswith("/rekap;"):
            a = text.split(";")
            msg = ""

            if a[1] == "LS" or \
                    a[1] == "SM" or \
                    a[1] == 'DK' or \
                    a[1] == "ls" or \
                    a[1] == "sm" or \
                    a[1] == "dk":
                msg = ""
                try:
                    data_sb_spv = db.get_spv_abs(a[1], a[2], a[3])
                    count = 0

                    if len(data_sb_spv) > 0:
                        for i in data_sb_spv:
                            msg += str(count + 1) + ". " + str(i[0]) + ": " + str(i[1]) + " kali masuk.\n"
                    else:
                        msg = "Tidak ada data yang tersedia"

                except IndexError as e:
                    msg = "Format input salah, silahkan ketik /help untuk bantuan"

                send_message(msg, chat)

            elif a[1] == 'STO' or a[1] == "sto":
                data_sto = db.get_sto_abs()

                for i in data_sto:
                    msg += "1. " + i[0] + "\n- Jumlah Karyawan: " + str(i[1]) + "\n- Jumlah Kehadiran: " + str(
                        i[2]) + "\n\n"

                send_message(msg, chat)
            else:
                kct = db.get_kcontact()
                msg = ""
                check = False

                for i in kct:
                    if a[1] == i[0]:
                        check = True
                        break
                    else:
                        check = False

                try:
                    if check:
                        data_kcontact_abs = db.get_kcontact_abs(a[2], a[3], a[1])
                        bulan = ""
                        if a[3] == "1":
                            bulan = "Januari"
                        elif a[3] == '2':
                            bulan = "Februari"
                        elif a[3] == '3':
                            bulan = 'Maret'
                        elif a[3] == '4':
                            bulan = "April"
                        elif a[3] == '5':
                            bulan = "Mei"
                        elif a[3] == '6':
                            bulan = "Juni"
                        elif a[3] == '7':
                            bulan = "Juli"
                        elif a[3] == '8':
                            bulan = "Agustus"
                        elif a[3] == '9':
                            bulan = "September"
                        elif a[3] == '10':
                            bulan = "Oktober"
                        elif a[3] == '11':
                            bulan = "November"
                        elif a[3] == '12':
                            bulan = "Desember"

                        msg = "Tahun: " + a[2] + ", " + "Bulan: " + bulan

                        count = 0
                        for i in data_kcontact_abs:
                            msg += "\n" + str(count+1) + ". " + "Tanggal " + str(i[3]) + ", hadir pada jam " + str(i[4])
                            count += 1

                except IndexError as e:
                    msg = "Format input salah, silahkan ketik /help untuk bantuan"

                send_message(msg, chat)

        else:
            msg = "Pesan tidak dapat dimengerti"
            send_message(msg, chat)


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
