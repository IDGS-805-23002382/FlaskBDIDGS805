from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos
from maestros.routes import maestros_bp
from flask_migrate import Migrate

import forms


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros_bp)
db.init_app(app)
migrate=Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm()
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        # Se agregan apellidos y telefono al objeto Alumnos
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("alumnos.html", form=create_form)


@app.route("/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        id=request.args.get('id')
        #slect*from alumnos where id=id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first() 
        nombre=alum1.nombre
        apellidos=alum1.apellidos
        email=alum1.email
        return render_template("detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            # Llenamos el formulario con los nuevos campos
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        return render_template("modificar.html", form=create_form)

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum1:
            # Actualizamos todos los datos en la DB
            alum1.nombre = create_form.nombre.data
            alum1.apellidos = create_form.apellidos.data
            alum1.email = create_form.email.data
            alum1.telefono = create_form.telefono.data
            db.session.commit()
        
        return redirect(url_for('index'))

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        return render_template("eliminar.html", form=create_form)

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum1:
            db.session.delete(alum1)
            db.session.commit()
            
        return redirect(url_for('index'))

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
 

