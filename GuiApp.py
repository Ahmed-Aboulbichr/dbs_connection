import tkinter as tk
from tkinter import PhotoImage, StringVar
import re
from MysqlConn import MysqlConn
from PostgresConn import PostgresConn
from SqliteConn import SqliteConn
import ttkbootstrap as ttk


class GuiApp(ttk.Window):

    def __init__(self, *args, **kwargs):
        super(GuiApp, self).__init__(*args, **kwargs)
        self.geometry("1500x550")
        self.title("Student Management")
        self.resizable(False, False)

        self.soo = ttk.Style(theme='superhero')

        self.conn = MysqlConn()

        self.tabControl = ttk.Notebook(self, name="note", bootstyle="secondary")
        self.tabControl.bind("<<NotebookTabChanged>>", self.select_tab)

        self.lblDB = ttk.Label(self)

        self.tabs = {
            "MySQL": ttk.Frame(self.tabControl),
            "SQLite": ttk.Frame(self.tabControl),
            "PostgreSQL": ttk.Frame(self.tabControl)}

        # Create the tabs in the notebook
        for t in self.tabs.keys():
            print(type(self.tabs[t]))
            self.tabControl.add(self.tabs[t], text=t, underline=0, sticky='nsew')

        self.tabControl.pack(expand=1, fill="both")

        imgSupprimer = PhotoImage(file="img/delete.png")
        imgAjouter = PhotoImage(file="img/add.png")
        imgAfficher = PhotoImage(file="img/search.png")
        imgModifer = PhotoImage(file="img/edit.png")

        # Create a button - this is the widget we wish to appear on all tabs
        self.btnAjouter = ttk.Button(self, image=imgAjouter, command=self.add_student_btn, bootstyle="light-link")
        self.btnSupprimer = ttk.Button(self, image=imgSupprimer, command=self.delete_student_btn, bootstyle="light-link")
        self.btnModifier = ttk.Button(self, image=imgModifer, command=self.edit_student_btn, bootstyle="light-link")
        self.btnAfficher = ttk.Button(self, image=imgAfficher, command=self.show_student_btn, bootstyle="light-link")

        self.cols = ('ID', 'CNE', 'CNI', 'Nom', 'Prenom', 'Date de Naissance', 'Mail Académique')

        self.etudiant_id = StringVar()
        self.cne = StringVar()
        self.txtCne = ttk.Entry(self, textvariable=self.cne, width=35, font=("Helvetica", 10), bootstyle="light")
        self.cni = StringVar()
        self.txtCni = ttk.Entry(self, textvariable=self.cni, width=35, font=("Helvetica", 10), bootstyle="light")
        self.nom = StringVar()
        self.txtNom = ttk.Entry(self, textvariable=self.nom, width=35, font=("Helvetica", 10), bootstyle="light")
        self.pre = StringVar()
        self.txtPrenom = ttk.Entry(self, textvariable=self.pre, width=35, font=("Helvetica", 10), bootstyle="light")
        self.dateN = StringVar()
        self.txtdnaissance = ttk.Entry(self, textvariable=self.dateN, width=35, font=("Helvetica", 10), bootstyle="light")
        self.mail = StringVar()
        self.txtmail = ttk.Entry(self, textvariable=self.mail, width=35, font=("Helvetica", 10), bootstyle="light")

        self.errors = StringVar()


        self.mainloop()

    def GetValue(self, event):
        nbr = self.listBox.selection()[0]
        select = self.listBox.set(nbr)
        self.cne.set(select["CNE"])
        self.cni.set(select["CNI"])
        self.nom.set(select["Nom"])
        self.pre.set(select["Prenom"])
        self.dateN.set(select["Date de Naissance"])
        self.mail.set(select["Mail Académique"])
        self.etudiant_id.set(select["ID"])
        #self.txtNom.configure(bootstyle="danger")

        #self.txtNom.configure(bootstyle="danger" if re.search("\w+", nom) else "success")

    def clear(self):
        self.cne.set("")
        self.cni.set("")
        self.nom.set("")
        self.pre.set("")
        self.dateN.set("")
        self.mail.set("")

    def add_student_btn(self):
        rep = self.conn.insert(self.cne.get(), self.cni.get(), self.nom.get(), self.pre.get(), self.dateN.get(), self.mail.get())
        self.errors.set(rep if rep is not None else f"Etudiant {self.nom.get()} a été ajouté avec succès!")
        self.after(7000, lambda: self.errors.set(""))
        self.show()
        self.clear()

    def delete_student_btn(self):
        rep = self.conn.remove(self.cne.get(), self.cni.get())
        self.errors.set(rep if rep is not None else f"Etudiant {self.nom.get()} a été supprimé avec succès!")
        self.after(5000, lambda: self.errors.set(""))
        self.show()
        self.clear()

    def edit_student_btn(self):
        rep = self.conn.update(self.cne.get(), self.cni.get(), self.nom.get(), self.pre.get(), self.dateN.get(), self.mail.get(), self.etudiant_id.get())
        self.errors.set(rep if rep is not None else f"Etudiant {self.nom.get()} a été modifié avec succès!")
        self.after(5000, lambda: self.errors.set(""))
        self.show()
        self.clear()

    def show_student_btn(self):
        rep = self.conn.getEtudiant(self.cne.get())
        self.showRep(rep)
        self.clear()

    def create_top_bar(self, key, frame: tk.Frame):
        top_frame = tk.Frame(frame, height=70)
        # top Frame  row=0, column=0
        top_frame.grid(row=0, columnspan=3, sticky='NWE')

    def create_left_form(self, key, frame: tk.Frame):
        left_frame = tk.Frame(frame, height=600)
        # left Frame row=1, column=
        left_frame.grid(row=1, column=0, sticky='W', padx=40, pady=15)
        tk.Label(left_frame, text="CNE", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, in_=left_frame,padx=2, pady=10, ipadx=2, ipady=3, sticky="W")
        self.txtCne.grid(row=0, column=1, in_=left_frame, pady=5, padx=3, ipadx=5, ipady=3)

        tk.Label(left_frame, text="CNI", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, in_=left_frame,padx=2, pady=10, ipadx=2, ipady=3, sticky="W")
        self.txtCni.grid(row=1, column=1, in_=left_frame, pady=5, padx=3, ipadx=2, ipady=3)

        tk.Label(left_frame, text="Nom", fg="white", font=("Helvetica", 12)).grid(row=2, column=0, in_=left_frame,padx=2, pady=10, ipadx=2, ipady=3, sticky="W")
        self.txtNom.grid(row=2, column=1, in_=left_frame, pady=5, padx=3, ipadx=2, ipady=3)

        tk.Label(left_frame, text="Prenom", fg="white", font=("Helvetica", 12)).grid(row=3, column=0, in_=left_frame,padx=2, pady=10, ipadx=2, ipady=3, sticky="W")
        self.txtPrenom.grid(row=3, column=1, in_=left_frame, pady=5, padx=3, ipadx=2, ipady=3)

        tk.Label(left_frame, text="Date Naissance", fg="white", font=("Helvetica", 12)).grid(row=4, column=0, in_=left_frame,padx=2, pady=5, ipadx=2, ipady=3, sticky="W")
        self.txtdnaissance.grid(row=4, column=1, in_=left_frame, pady=5, padx=3, ipadx=2, ipady=3)

        tk.Label(left_frame, text="Mail Académique", fg="white", font=("Helvetica", 12)).grid(row=5, column=0, in_=left_frame,padx=2, pady=5, ipadx=2, ipady=3, sticky="W")
        self.txtmail.grid(row=5, column=1, in_=left_frame, pady=5, padx=3, ipadx=2, ipady=3)


    def create_right_tab(self, key, frame: tk.Frame):
        right_frame = tk.Frame(frame, height=600)
        # right frame row=1, column=1

        right_frame.grid(row=1, column=1, sticky='W', padx=5, pady=5)
        self.listBox = ttk.Treeview(right_frame, columns=self.cols, show='headings', height=13, bootstyle="info")
        self.listBox.bind('<Double-Button-1>', self.GetValue)
        for col in self.cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col, minwidth=0, width=[100 if col != self.cols[-1] else 220])
            self.listBox.grid(row=0, columnspan=2, sticky="ns")

    def create_bottom_buttons(self, key, frame: tk.Frame):
        bottom_frame = tk.Frame(frame)
        # bottom frame row=2, column=0
        bottom_frame.grid(row=2, column=0, sticky='SWE', columnspan=3, padx=40)

        self.btnAjouter.grid(row=0, column=0, padx=10, sticky='E', in_=bottom_frame)
        self.btnSupprimer.grid(row=0, column=1, padx=10, sticky='E', in_=bottom_frame)
        self.btnModifier.grid(row=0, column=2, padx=10, sticky='E', in_=bottom_frame)
        self.btnAfficher.grid(row=0, column=3, padx=10, sticky='E', in_=bottom_frame)
        self.lblErrors = tk.Label(self, textvariable=self.errors, font=("Helvetica", 12))
        self.lblErrors.place(x=600, y=20, in_=bottom_frame)

    def showRep(self, rep):
        self.deleteTable()
        for i, value in enumerate(rep):
            print(rep)
            self.listBox.insert("", "end", values=(value[0], value[1], value[2], value[3], value[4], value[5], value[6]))

    def show(self):
        self.deleteTable()
        for i, value in enumerate(self.conn.fetch()):
            self.listBox.insert("", "end", values=(value[0], value[1], value[2], value[3], value[4], value[5], value[6]))

    def deleteTable(self):
        for item in self.listBox.get_children():
            self.listBox.delete(item)

    def select_tab(self, event):
        id = self.tabControl.select()
        self.name = self.tabControl.tab(id, "text")
        frame = self.tabs[self.name]
        self.create_top_bar(self.name, frame)
        self.create_left_form(self.name, self.tabs[self.name])
        self.create_right_tab(self.name, self.tabs[self.name])
        self.create_bottom_buttons(self.name, frame)
        self.conn = self.getConn(self.name)
        self.show()


    def getConn(self, name):
        if name == "MySQL":

            self.soo.theme_use("darkly")
            return MysqlConn()
        elif name == "SQLite":
            self.soo.theme_use("superhero")
            return SqliteConn()
        elif name == "PostgreSQL":
            self.soo.theme_use("solar")
            return PostgresConn()
        return False


if __name__ == "__main__":
    app = GuiApp()
