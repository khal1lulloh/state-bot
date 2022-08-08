import sqlite3
class Sql:
    def __init__(self):
        self.connection = sqlite3.connect('class1.db')
        self.cursor = self.connection.cursor()

    def tablitsa_yaratish(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS baza (
                tel_id integer,
                username varchar(60),
                fio varchar(40) NULL,
                tel varchar(12) NULL
                )
                """)

    def tablitsa_qushish(self, tel_id, username):    
        self.cursor.execute("INSERT INTO baza VALUES ({},'{}',NULL,NULL)".format(tel_id,username))
        return self.connection.commit()

    def id_user(self,tel_id):
        self.cursor.execute(f"SELECT tel_id FROM baza WHERE tel_id = {tel_id}")
        data = self.cursor.fetchone()
        return data

    def userlar(self):
        self.cursor.execute(f"SELECT COUNT(tel_id) FROM baza")
        info = self.cursor.fetchall()
        r = None
        for i in info:
            r = i[0]
        return r

    def telefonlar(self):
        self.cursor.execute(f"SELECT COUNT(tel) FROM baza")
        info = self.cursor.fetchall()
        r = None
        for i in info:
            r = i[0]
        return r

    def tablitsa_uz(self,tel_id,fio,tel):
        self.cursor.execute(f"UPDATE  baza SET fio = '{fio}',tel = '{tel}' Where tel_id='{tel_id}'")
        return self.connection.commit()

    def rec(self):
        self.cursor.execute(f"SELECT * FROM baza")
        idila = self.cursor.fetchall()      
        return idila

    def phone(self):
        self.cursor.execute(f"SELECT * FROM baza WHERE tel ")
        idila = self.cursor.fetchall()      
        return idila

    def add_kurs(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS kurslar (
                nomi varchar(60),
                izoh text,
                narxi varchar(12)
                )
                """)

    def kurs(self,nomi,izoh,narxi):
        self.cursor.execute("INSERT INTO kurslar VALUES ('{}','{}','{}')".format(nomi,izoh,narxi))
        return self.connection.commit()

        
    def edit_kurs(self,nomi,izoh,narxi):
        self.cursor.execute(f"UPDATE kurslar SET izoh = '{izoh}',narxi = '{narxi}' Where nomi='{nomi}'")
        return self.connection.commit()

    def select_all(self):
        self.cursor.execute("SELECT nomi FROM kurslar")
        data = self.cursor.fetchall()
        return data

    def ochirish(self,nomi):
        self.cursor.execute(f"DELETE FROM kurslar WHERE nomi='{nomi}'")
        self.connection.commit()
        return f"O'chdi"

    def sel(self,nomi):
        self.cursor.execute(f"SELECT izoh FROM kurslar WHERE nomi = '{nomi}'")
        info = self.cursor.fetchall()
        return info

    def sell(self,nomi):
        self.cursor.execute(f"SELECT narxi FROM kurslar WHERE nomi = '{nomi}'")
        info = self.cursor.fetchone()
        return info


