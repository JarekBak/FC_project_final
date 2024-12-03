import pandas as pd
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correspondence.db'
db = SQLAlchemy(app)

class Departament(db.Model):
    __tablename__ = 'departament'
    depID = db.Column(db.Integer, primary_key=True)
    depName = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.relationship('Employee', backref='departament', lazy=True)
    correspondences = db.relationship('Correspondence', backref='departament', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    empID = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(100), nullable=False, unique=True)
    empEmail = db.Column(db.String(100), nullable=False, unique=True)
    empIsManager = db.Column(db.Boolean, default=False)
    depID = db.Column(db.Integer, db.ForeignKey('departament.depID'), nullable=False)
    correspondences = db.relationship('Correspondence', backref='employee', lazy=True)

class Correspondence(db.Model):
    __tablename__ = 'correspondence'
    corID = db.Column(db.Integer, primary_key=True)
    corSubject = db.Column(db.String(100), nullable=False, unique=False)
    corContent = db.Column(db.String(255), nullable=False, unique=False)
    corDate = db.Column(db.Date, nullable=False)
    corType = db.Column(db.Integer, nullable=False)
    corSenderName = db.Column(db.String(100), nullable=False)
    corSenderAddress = db.Column(db.String(255), nullable=False)
    corRecipientName = db.Column(db.String(100), nullable=False)
    corRecipientAddress = db.Column(db.String(255), nullable=False)
    depID = db.Column(db.Integer, db.ForeignKey("departament.depID"), nullable=True)
    empID = db.Column(db.Integer, db.ForeignKey("employee.empID"), nullable=True)
    attachments = db.relationship("Attachment", backref="correspondence", lazy=True)

    def __repr__(self):
        return f'<Correspondence {self.corSubject}>'

class Attachment(db.Model):
    attID = db.Column(db.Integer, primary_key=True)
    corID = db.Column(db.Integer, db.ForeignKey("correspondence.corID"), nullable=True)
    fileName = db.Column(db.String(100), nullable=False, unique=True)
    filePath = db.Column(db.String(200), nullable=False, unique=True)
