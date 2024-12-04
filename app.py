from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Departament, Employee, Correspondence, Attachment
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corespondetion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    departaments = Departament.query.all()
    return render_template("index.html", departaments=departaments)

@app.route("/departaments")
def departament_list():
    departaments = Departament.query.all()
    return render_template("departaments.html", departaments=departaments)

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

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        empName = request.form.get('empName')
        empEmail = request.form.get('empEmail')
        depID = request.form.get('depID')  # depID jako liczba
        empIsManager = 'empIsManager' in request.form  # True jeśli zaznaczono

        # Dodanie nowego pracownika
        new_employee = Employee(
            empName=empName,
            empEmail=empEmail,
            depID=depID,  # Zapisywanie depID w bazie
            empIsManager=empIsManager
        )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('employee_list'))  # Przekierowanie na listę pracowników

    # Dla metody GET: renderowanie formularza
    departaments = Departament.query.all()
    return render_template('add_employee.html', departaments=departaments)

@app.route("/employees")
def employee_list():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)

@app.route("/add-correspondence", methods=["GET", "POST"])
def add_correspondence():
    departaments = Departament.query.all()

    if request.method == 'POST':
        # Pobieramy dane z formularza
        corSubject = request.form.get('corSubject')
        corContent = request.form.get('corContent')
        corDate = request.form.get('corDate')
        corType = request.form.get('corType')
        corSenderName = request.form.get('corSenderName')
        corSenderAddress = request.form.get('corSenderAddress')
        corRecipientName = request.form.get('corRecipientName')
        corRecipientAddress = request.form.get('corRecipientAddress')
        depID = request.form.get('depID')
        corStatus = request.form.get('corStatus')

        # Konwersja corDate na datetime.date
        corDate_obj = datetime.strptime(corDate, '%Y-%m-%d').date()

        # Walidacja danych
        if not corSubject or not corDate or not corType or not corSenderName or not depID:
            return "All fields (Tytuł pisma, Data, Typ, Nadawca, Departament) are required.", 400

        try:
            # Dodajemy nową korespondencję
            new_correspondence = Correspondence(
                corSubject=corSubject,
                corContent=corContent,
                corDate=corDate_obj,
                corType=corType,
                corSenderName=corSenderName,
                corSenderAddress=corSenderAddress,
                corRecipientName=corRecipientName,
                corRecipientAddress=corRecipientAddress,
                depID=depID,
                corStatus=corStatus

            )
            db.session.add(new_correspondence)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

        return redirect(url_for('cor_records'))

    return render_template("add_correspondence.html", departaments=departaments)

@app.route('/cor_records')
def cor_records():
    try:
        # Pobranie listy departamentów
        departaments = Departament.query.all()

        # Pobranie parametrów filtrowania
        filter_subject = request.args.get('filterSubject', '').strip()
        filter_sender = request.args.get('filterSender', '').strip()
        filter_status = request.args.get('filterStatus', '').strip()
        filter_department = request.args.get('filterDepartment', '').strip()

        # Tworzenie podstawowego zapytania
        query = Correspondence.query

        # Dodawanie filtrów dynamicznie
        if filter_subject:
            query = query.filter(Correspondence.corSubject.ilike(f"%{filter_subject}%"))
        if filter_sender:
            query = query.filter(Correspondence.corSenderName.ilike(f"%{filter_sender}%"))
        if filter_status:
            query = query.filter(Correspondence.corStatus == filter_status)
        if filter_department:
            query = query.filter(Correspondence.depID == int(filter_department))

        # Pobranie przefiltrowanych rekordów
        records = query.all()

        return render_template('cor_records.html', records=records, departaments=departaments)
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/cor_update_record/<int:corID>', methods=['GET', 'POST'])
def cor_update_record(corID):
    record = Correspondence.query.get_or_404(corID)
    departaments = Departament.query.all()

    # Wybrany departament z formularza (domyślnie aktualny w rekordzie)
    selected_depID = request.args.get('depID', record.depID)  # Jeśli GET, to z URL, jeśli POST to z formularza

    # Pobranie pracowników na podstawie wybranego departamentu
    employees = Employee.query.filter_by(depID=selected_depID).all() if selected_depID else []

    if request.method == 'POST':
        if 'save' in request.form:
            # Zapisywanie zmian
            record.depID = request.form.get('depID')
            record.empID = request.form.get('empID')
            db.session.commit()
            return redirect(url_for('cor_records'))

    return render_template(
        'cor_update_record.html',
        record=record,
        departaments=departaments,
        employees=employees,
        selected_depID=selected_depID
    )

@app.route('/edit_correspondence/<int:corID>', methods=['GET', 'POST'])
def edit_correspondence(corID):
    record = Correspondence.query.get_or_404(corID)

    if request.method == 'POST':
        # Pobierz zmienione dane z formularza
        record.corStatus = request.form.get('corStatus')
        record.corDeadline = request.form.get('corDeadline')
        record.corComplited = request.form.get('corComplited')

        # Walidacja dat
        record.corDeadline = datetime.strptime(record.corDeadline, '%Y-%m-%d').date() if record.corDeadline else None
        record.corComplited = datetime.strptime(record.corComplited, '%Y-%m-%d').date() if record.corComplited else None

        # Zapis zmian
        try:
            db.session.commit()
            return redirect(url_for('cor_records'))  # Przekierowanie do listy rekordów
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

    return render_template('edit_correspondence.html', record=record)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
