from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from models import Alumnos

import forms


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_foud(e):
    return render_template("404.html"), 404


@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    alumno = Alumnos.query.all() 
    return render_template("index.html", form=create_form, alumno=alumno)


@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.correo.data  
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template("alumnos.html", form=create_form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
 

