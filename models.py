import pandas as pd
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correspondence.db'
db = SQLAlchemy(app)

class Departament(db.Model):
    depID = db.Column(db.Integer, primary_key=True)
    depName = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.relationship('Employee', backref='department', lazy=True)
    correspondences = db.relationship('Correspondence', backref='department', lazy=True)
    # def __init__(self):
    #     self.departments = pd.DataFrame(columns=["ID departamentu", "Nazwa departamentu", "ID Menagera"])
    #
    # def add_department(self, depID, depName, emp_id):
    #     self.departments = pd.concat([
    #         self.departments,
    #         pd.DataFrame([[depID, depName, emp_id]], columns=self.departments.columns)
    #     ])

class Employee(db.Model):
    empID = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(100), nullable=False, unique=True)
    empEmail = db.Column(db.String(100), nullable=False, unique=True)
    empIsManager = db.Column(db.Boolean, default=False)
    depID = db.Column(db.Integer, db.ForeignKey('departament.depID'), nullable=False)
    correspondences = db.relationship('Correspondence', backref='employee', lazy=True)
    # def __init__(self):
    #     self.employees = pd.DataFrame(columns=["ID pracownika", "Imię i Nazwisko", "email", "Czy manager?",
    #                                            "ID departamentu"]
    #                                   )
    #
    # def add_employee(self, empID, empName, empEmail, empIsManager, dep_id):
    #     self.employees = pd.concat([
    #         self.employees,
    #         pd.DataFrame([[empID, empName, empEmail, empIsManager, dep_id]],
    #                      columns=self.employees.columns)
    #     ])

class Correspondence(db.Model):
    corID = db.Column(db.Integer, primary_key=True)
    corSubject = db.Column(db.String(100), nullable=False, unique=True)
    corContent = db.Column(db.String(255), nullable=False, unique=True)
    corDate = db.Column(db.Date, nullable=False)
    corType = db.Column(db.Integer, nullable=False)
    corSenderName = db.Column(db.String(100), nullable=False)
    corSenderAddress = db.Column(db.String(255), nullable=False)
    corRecipientName = db.Column(db.String(100), nullable=False)
    corRecipientAddress = db.Column(db.String(255), nullable=False)
    depID = db.Column(db.Integer, db.ForeignKey("departament.depID"), nullable=True)
    empID = db.Column(db.Integer, db.ForeignKey("employee.empID"), nullable=True)
    attachments = db.relationship("Attachment", backref="correspondence", lazy=True)

    # def __init__(self):
    #     self.correspondence = pd.DataFrame(
    #         columns=["ID korespondencji", "Przedmiot", "Opis", "Data rejestracji", "Typ", "Nadawca", "Adres nadawcy",
    #                  "Odbiorca", "Adres odbiorcy", "ID departamentu", "ID pracownika"]
    #     )
    #
    # def add_correspondence(self, corID, corSubject, corContent, corDate, corType, corSenderName, corSenderAddress,
    #                        corRecipientName, corRecipientAddress, depID, empID
    #                        ):
    #     corDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.correspondence = pd.concat([
    #         self.correspondence,
    #         pd.DataFrame([[corID, corSubject, corContent, corDate, corType, corSenderName, corSenderAddress,
    #                        corRecipientName, corRecipientAddress, depID, empID]], columns=self.correspondence.columns)
    #     ])

class Attachment(db.Model):
    attID = db.Column(db.Integer, primary_key=True)
    corID = db.Column(db.Integer, db.ForeignKey("correspondence.corID"), nullable=True)
    fileName = db.Column(db.String(100), nullable=False, unique=True)
    filePath = db.Column(db.String(200), nullable=False, unique=True)
    # def __init__(self):
    #     self.attachemnts = pd.DataFrame(columns=["ID_zalacznika", "ID_korespondencji", "Nazwa_pliku", "Sciezka_dostepu"])
    #
    # def add_attachment(self, attID, corID, FileName, FilePath):
    #     self.attachmets = pd.concat([
    #         self.attachmets,
    #         pd.DataFrame([[attID, corID, FileName, FilePath]],
    #                      columns=self.attachmets.columns)
    #     ])

###################################################################################################
# # Przykład użycia
# departamenty = Departament()
# departamenty.dodaj_departament(1, "IT", 101)
#
# pracownicy = Pracownicy()
# pracownicy.dodaj_pracownika(1, "Jan", "Kowalski", "jan.kowalski@example.com", 1, True)
#
# korespondencja = Korespondencja()
# korespondencja.dodaj_korespondencje(1, "Oferta współpracy", "Szczegóły oferty...", "przychodzące", "Firma ABC", 1, 1, "brak")
#
# logi = Logi()
# logi.dodaj_log(1, 1, "Rejestracja pisma", 1)
#
# zalaczniki = Zalaczniki()
# zalaczniki.dodaj_zalacznik(1, 1, "oferta.pdf", "/path/to/oferta.pdf")
#
# # Podgląd tabel
# print("Departamenty:")
# print(departamenty.departments)
# print("\nPracownicy:")
# print(pracownicy.pracownicy)
# print("\nKorespondencja:")
# print(korespondencja.korespondencja)
# print("\nLogi:")
# print(logi.logi)
# print("\nZałączniki:")
# print(zalaczniki.zalaczniki)
#
#
# def pisma_realizowane_przez_departament(korespondencja, logi, id_departamentu):
#     realizacja = logi.logi[logi.logi["Rodzaj_operacji"] == "realizacja"]
#     pisma = pd.merge(realizacja, korespondencja.korespondencja, left_on="ID_korespondencji", right_on="ID_korespondencji")
#     pisma_departament = pisma[pisma["ID_departamentu"] == id_departamentu]
#     return pisma_departament[["ID_korespondencji", "Temat", "Treść", "Typ", "Nadawca", "ID_pracownika_obsługującego"]]
#
#
# id_departamentu = 1  # Podaj ID departamentu
# pisma_departament = pisma_realizowane_przez_departament(korespondencja, logi, id_departamentu)
# print(f"Pisma realizowane przez departament o ID {id_departamentu}:")
# print(pisma_departament)
#
#
# def pisma_realizowane_przez_pracownika(korespondencja, logi, id_pracownika):
#     realizacja = logi.logi[(logi.logi["Rodzaj_operacji"] == "realizacja") & (logi.logi["ID_pracownika"] == id_pracownika)]
#     pisma = pd.merge(realizacja, korespondencja.korespondencja, left_on="ID_korespondencji", right_on="ID_korespondencji")
#     return pisma[["ID_korespondencji", "Temat", "Treść", "Typ", "Nadawca", "ID_departamentu"]]
#
# id_pracownika = 1  # Podaj ID pracownika
# pisma_pracownik = pisma_realizowane_przez_pracownika(korespondencja, logi, id_pracownika)
# print(f"Pisma realizowane przez pracownika o ID {id_pracownika}:")
# print(pisma_pracownik)
#
#
# def pisma_w_realizacji(korespondencja, logi):
#     realizacja = logi.logi[logi.logi["Rodzaj_operacji"] == "realizacja"]
#     pisma = pd.merge(realizacja, korespondencja.korespondencja, left_on="ID_korespondencji", right_on="ID_korespondencji")
#     return pisma[["ID_korespondencji", "Temat", "Treść", "Typ", "Nadawca", "ID_departamentu", "ID_pracownika_obsługującego"]]
#
#
# pisma_realizacja = pisma_w_realizacji(korespondencja, logi)
# print("Pisma w realizacji:")
# print(pisma_realizacja)
#
#
# class Logi:
#     def __init__(self):
#         self.logi = pd.DataFrame(columns=["ID_loga", "ID_korespondencji", "Rodzaj_operacji", "ID_pracownika", "Data_operacji"])
#
#     def dodaj_log(self, id_loga, id_korespondencji, rodzaj_operacji, id_pracownika):
#         data_operacji = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.logi = pd.concat([
#             self.logi,
#             pd.DataFrame([[id_loga, id_korespondencji, rodzaj_operacji, id_pracownika, data_operacji]],
#                          columns=self.logi.columns)
#         ])
