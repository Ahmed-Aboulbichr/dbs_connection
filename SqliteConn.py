import sqlite3 as sql
from sqlite3 import Error


class SqliteConn:
    def __init__(self):
        self.conn = sql.connect("sqlitedb.db")
        self.cur = self.conn.cursor()

    def getEtudiant(self, cne):
        try:
            self.cur.execute("SELECT * FROM etudiant where cne like ?", ("%{}%".format(cne),))
            rows = self.cur.fetchall()
            return rows
        except Error as e:
            return f"Erreur : {e}"

    def fetch(self):
        print("fetch")
        try:

            print("start")
            self.cur.execute("SELECT * FROM etudiant")
            print(self.cur.rowcount)
            rows = self.cur.fetchall()
            return rows
        except Error as e:
            return f"Erreur : {e}"

    def insert(self, cne, cni, nom, prenom, date, mail):
        print(cne, cni, nom, prenom, date, mail)
        try:
            self.cur.execute("INSERT INTO etudiant(cne, cni, nom, prenom, date_naissance, mail_academique) VALUES (%s, %s, %s, %s, %s, %s)",
                            (cne, cni, nom, prenom, date, mail))

            self.conn.commit()
            print(self.cur.rowcount)

        except Error as e:
            return f"Erreur : {e}"

    def remove(self, cne, cni):
        try:
            self.cur.execute("DELETE FROM etudiant WHERE cne=? and cni= ?", (cne, cni,))
            self.conn.commit()
            print(self.cur.rowcount)
        except Error as e:
            return f"Erreur : {e}"

    def update(self, cne, cni, nom, prenom, date, mail, e_id):
        try:
            self.cur.execute(
                    "UPDATE etudiant SET cne = ?, cni = ?, nom = ?, prenom = ?, date_naissance = ?, mail_academique = ? WHERE id = ?",
                    (cne, cni, nom, prenom, date, mail, e_id))
            self.conn.commit()
        except Error as e:
            return f"Erreur : {e}"

    def __del__(self):
        print("closed")
        self.conn.close()
