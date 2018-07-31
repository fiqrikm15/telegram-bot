from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, date, timedelta
from mysql.connector.errors import *
import pytz

class DBHandler:
    waktu = datetime.now()

    def __init__(self, _db, _username, _host, _password=""):
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
        # self.cnx.set_autocommit(True)

        if self.cnx:
            print("Connection: OK")
        else:
            print("Connection failed, please check your database connection")

        # try:
        #     self.cnx = mysql.connector.connect(
        #     user=self.username,
        #     password=self.password,
        #     host=self.host,
        #     database=self.db
        #     )

        #     self.cnx.set_autocommit(True)

        #     if self.cnx:
        #         print("Connection: OK")
        #     else:
        #         print("Connection failed, please check your database connection")
        # except:
        #     print("asdf")


    def insert_karyawan(self, kcontact, nama, spv):
        insert = "insert into karyawan(kcontact, nama, spv) values('" + kcontact.upper() + "','" + nama + "','" + spv.upper() +"')"
        cursor = self.cnx.cursor()

        cursor.execute(insert)
        self.cnx.commit()
        cursor.close()


    def insert_absen(self, kcontact, waktu):
        insert = "insert into absen(kcontact, waktu) values('"+ kcontact.upper() + "','" + str(waktu) +"')"
        cursor = self.cnx.cursor()

        cursor.execute(insert)

        self.cnx.commit()
        cursor.close()


    def get_karyawan(self):
        try:
            get = "select * from karyawan"
            cursor = self.cnx.cursor()
            data_kar = []

            cursor.execute(get)
            for data in cursor:
                data_kar.append(data)

            self.cnx.commit()
            cursor.close()

            return data_kar
        except mysql.connector.Error as e:            
            print(e.msg)


    def get_absen(self):
        get = "select * from absen"
        cursor = self.cnx.cursor()
        data_abs = []

        cursor.execute(get)
        for data in cursor:
            data_abs.append(data)

        self.cnx.commit()
        cursor.close()
        return data_abs

    def get_absen_id(self, kcontact):
        get = "select * from absen where kcontact=kcontact"
        cursor = self.cnx.cursor()
        data_abs = []

        cursor.execute(get)
        for data in cursor:
            data_abs.append(data)

        self.cnx.commit()
        cursor.close()
        return data_abs

    def get_sto_abs(self):
        # get = "select karyawan.spv, count(karyawan.spv), count(absen.id) as absen from karyawan left join absen on absen.kcontact = karyawan.kcontact group by  karyawan.spv order by absen DESC"
        get = "SELECT karyawan.`spv`, COUNT(DISTINCT(karyawan.`kcontact`)) AS karyawa, COUNT(absen.`id`) AS absensi FROM karyawan JOIN absen ON karyawan.`kcontact` = `absen`.`kcontact` GROUP BY karyawan.`spv` ORDER BY absensi DESC"
        cursor = self.cnx.cursor()
        data_abs = []

        cursor.execute(get)
        for data in cursor:
            data_abs.append(data)

        self.cnx.commit()
        cursor.close()
        return data_abs

    def get_kcontact(self):
        query = "select kcontact from karyawan"
        cursor = self.cnx.cursor()
        data_kacontact = []

        cursor.execute(query)

        for data in cursor:
            data_kacontact.append(data)

        self.cnx.commit()
        cursor.close()
        return data_kacontact

    def count_data(self):
        query = "select count(*) from karyawan"
        cursor = self.cnx.cursor()

        cursor.execute(query)

        res = cursor.fetchone()
        self.cnx.commit()
        cursor.close()
        return res[0]

    def get_totalK(self):
        query = "select spv, count(*) from karyawan group by (spv)"
        cursor = self.cnx.cursor()
        data_kar = []

        cursor.execute(query)

        for i in cursor:
            data_kar.append(i)

        cursor.close()
        return data_kar


    def check_registered(self, kcontact):
        cursor = self.cnx.cursor()
        query = "select count(kcontact) from karyawan where kcontact='"+str(kcontact)+"'"

        cursor.execute(query)
        count = cursor.fetchone()[0]

        if(count == 1):
            self.cnx.commit()
            cursor.close()
            return True
        else:
            self.cnx.commit()
            cursor.close()
            return False

    def get_kcontact_abs(self, y, m, kcontact):
        query = "SELECT kcontact, YEAR(waktu), MONTH(waktu), day(waktu), TIME(waktu),hour(waktu) FROM absen where year(waktu)=" + y +" and month(waktu)="+ m +" and kcontact='"+ kcontact +"' ORDER BY(waktu) ASC;"
        cursor = self.cnx.cursor()
        data_abs_bln = []

        cursor.execute(query)
        result = cursor.fetchall()

        for data in result:
            data_abs_bln.append(data)

        self.cnx.commit()
        cursor.close()
        return data_abs_bln

    def get_spv_abs(self, spv, y, m):
        # query = "select karyawan.spv, count(absen.id) as absen from karyawan left join absen on absen.kcontact = karyawan.kcontact where karyawan.spv='" + spv +"' group by  karyawan.spv order by absen"
        query = "SELECT karyawan.`kcontact`, COUNT(`absen`.`waktu`) AS Total FROM karyawan, absen WHERE karyawan.`kcontact` = absen.`kcontact` AND karyawan.`spv` = '" + spv + "' AND YEAR(absen.waktu)='"+ y +"' AND MONTH(absen.waktu)='"+ m +"' GROUP BY(karyawan.`kcontact`) ORDER BY(Total) DESC; "
        cursor = self.cnx.cursor()
        data_bs_spv = []

        cursor.execute(query)

        for data in cursor:
            data_bs_spv.append(data)

        self.cnx.commit()
        cursor.close()
        return data_bs_spv


# db = DBHandler('absen_bot', 'root', '127.0.0.1')
# print(db.get_totalK()[2][1])
