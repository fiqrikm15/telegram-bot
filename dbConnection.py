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
            print("Connection failed, please check your datbase connection")

    def get_jumlah_data(self):
        query = "select count(*) from karyawan"
        cur = self.cnx.cursor()

        cur.execute(query)

        res = cur.fetchone()

        return res[0]
    

    def get_detail_karyawan(self, nik):
        query = "select * from karyawan where id=" + str(nik)
        cur = self.cnx.cursor()
        data_kar = []

        cur.execute(query)

        for i in cur:
            data_kar.append(i)

        return data_kar


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


    def get_count(self):
        cur = self.cnx.cursor()
        query = "SELECT a.nama, b.id_karyawan, COUNT(*) FROM karyawan a, absensi b WHERE b.`id_karyawan` = a.`id` GROUP BY(id_karyawan);"

        cur.execute(query)

        data_count = []
        for data in cur:
            data_count.append(data)

        cur.close()
        return data_count

    def search_data(self, nik):
        query = "SELECT a.nama, b.id_karyawan, COUNT(*) FROM karyawan a, absensi b WHERE b.`id_karyawan` = a.`id` and a.id=" + str(nik) +" GROUP BY(id_karyawan);"
        cur = self.cnx.cursor()

        cur.execute(query)

        data_karyawan = []
        for i in cur:
            data_karyawan.append(i)

        cur.close()
        return data_karyawan

# db = DBHelper('absen_bot', 'root', 'mysql', '127.0.0.1')
# a = db.get_detail_karyawan(1)
# print(a[0])
