import mysql.connector
from datetime import datetime
from mysql.connector import errorcode

class DBHelper:   

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
            print("Connection success")
        else:
            print("Connection failed")

    def get_data_karyawan(self):
        query = "select * from karyawan"
        cur = self.cnx.cursor()

        cur.execute(query)
        data_kar = []

        for data in cur:
            data_kar.append(data)

        cur.close()
        return data_kar

    def get_data_absen(self):
        query = "select * from absensi"
        cur = self.cnx.cursor()

        cur.execute(query)

        data_abs = []
        for data in cur:
            data_abs.append(data)

        cur.close()
        return data_abs

    def get_detail_absen(self):
        query = "SELECT b.`nama`, a.`jam_masuk`, a.`jam_pulang` FROM absensi a, karyawan b WHERE a.`id_karyawan`=b.`id`"
        cur = self.cnx.cursor()

        cur.execute(query)

        data_detail_abs = []
        for data in cur:
            data_detail_abs.append(data)

        cur.close()
        return data_detail_abs

    


db = DBHelper('absen_bot', 'root', 'mysql', '127.0.0.1')
asd = db.get_detail_absen()
print(asd)