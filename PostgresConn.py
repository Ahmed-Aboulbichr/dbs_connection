import psycopg2 as ps
from psycopg2 import Error

import ReadConfig as rc


class PostgresConn:
    def __init__(self):
        d = rc.read_ini("config_postgres.ini")
        self.conn = ps.connect(host=d["host"], user=d["user"], password=d["password"], dbname=d["dbname"])

    def getEtudiant(self, cne):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM etudiant where cne like %s", ("%{}%".format(cne),))
                rows = cur.fetchall()
                return rows
        except Error as e:
            return f"Erreur : {e}"

    def getEtudiant(self, cne):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM etudiant where cne like %s", ("%{}%".format(cne),))
                rows = cur.fetchall()
                return rows
        except Error as e:
            return f"Erreur : {e}"

    def fetch(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM etudiant")
                print(cur.rowcount)
                rows = cur.fetchall()
                return rows
        except Error as e:
            return f"Erreur : {e}"

    def insert(self, cne, cni, nom, prenom, date, mail):
        print(cne, cni, nom, prenom, date, mail)
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO etudiant(cne, cni, nom, prenom, date_naissance, mail_academique) VALUES (%s, %s, %s, %s, %s, %s)",
                    (cne, cni, nom, prenom, date, mail))

                self.conn.commit()
                print(cur.rowcount)

        except Error as e:
            return f"Erreur : {e}"

    def remove(self, cne, cni):
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM etudiant WHERE cne=%s and cni= %s", (cne, cni,))
                self.conn.commit()
                print(cur.rowcount)
        except Error as e:
            return f"Erreur : {e}"

    def update(self, cne, cni, nom, prenom, date, mail, e_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE etudiant SET cne = %s, cni = %s, nom = %s, prenom = %s, date_naissance = %s, mail_academique = %s WHERE id = %s",
                    (cne, cni, nom, prenom, date, mail, e_id))
                self.conn.commit()
        except Error as e:
            return f"Erreur : {e}"

    def __del__(self):
        print("closed")
        if self.conn is not None:
            self.conn.close()
