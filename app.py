from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Departament, Employee, Correspondence, Attachment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corespondetion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def index():
    departaments = Departament.query.all()
    return render_template("index.html", departaments=departaments)

@app.route("/add-departament", methods=['GET', 'POST'])
def add_departament():
    if request.method == 'POST':
    # Pobieramy dane z formularza
        depName = request.form.get('depName')

        # Walidacja danych
        if not depName:
            return "All fields (depName) are required.", 400
        try:
            new_departament = Departament(depName=depName)
            db.session.add(new_departament)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500
        return redirect(url_for('index'))
    else:
        # Dla żądania GET renderujemy formularz
        return render_template("add_departament.html")
@app.route("/add-employee", methods=['GET', 'POST'])
def add_employee():
    departaments = Departament.query.all()

    if request.method == 'POST':
        # Pobieramy dane z formularza
        empName = request.form.get('empName')
        empEmail = request.form.get('empEmail')
        depID = request.form.get('depID')
        empIsManager = request.form.get('empIsManager', 'off') == 'on'

        # Walidacja danych
        if not empName or not empEmail or not depID:
            return "All fields (empName, empEmail, depID) are required.", 400

        try:
            # Dodajemy nowego pracownika
            new_employee = Employee(
                empName=empName,
                empEmail=empEmail,
                depID=depID,
                empIsManager=empIsManager
            )
            db.session.add(new_employee)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

        return redirect(url_for('employee_list'))
    # else:
    #     # Dla żądania GET renderujemy formularz
    return render_template("add_employee.html", departaments=departaments)

@app.route("/employees")
def employee_list():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)

if __name__ == "__main__":
    app.run(debug=True)
