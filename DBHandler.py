from __future__ import print_function
import mysql.connector
from datetime import datetime, date, timedelta
import pytz

class DBHandle:
    waktu = datetime.now()

    def __init__(self, _db, _username, _password, _host):
        self.username = _username
        self.password = _password
        self.db = _db
        self.host = _host

        self.cnx = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            database=self.db
        )

        if self.cnx:
            print("Connection: OK")
        else:
            print("Connection failed, please check your datbase connection")

    def get_data(self):
        pass


    def insert_karyawan(self, kcontact, nama, spv):
        insert = "insert into karyawan(kcontact, nama, spv) values('" + kcontact + "','" + nama + "','" + spv +"')"
        cursor = self.cnx.cursor()

        cursor.execute(insert)
        self.cnx.commit()
        cursor.close()
        self.cnx.close()


    def insert_absen(self, kcontact, waktu):
        insert = "insert into absen(kcontact, waktu) values('"+ kcontact + "','" + waktu +"')"
        cursor = self.cnx.cursor()

        cursor.execute(insert)
        self.cnx.commit()
        cursor.close()
        self.cnx.close()


db = DBHandle('absen_bot', 'root', 'mysql', '127.0.0.1')
print(db.insert_absen('AAK21', str(datetime.now())))

