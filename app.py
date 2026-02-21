from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Alumnos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
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

@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    create_form = forms.UserForm()
    if request.method == "POST":
        if create_form.validate_on_submit():
            nuevo = Alumnos(
                nombre=create_form.nombre.data,
                apaterno=create_form.apaterno.data,
                email=create_form.correo.data   # aquí mapeamos correo → email
            )
            
            db.session.add(nuevo)
            db.session.commit()
            flash("Alumno registrado correctamente")
            return redirect(url_for("index"))
        else:
            flash("Error al registrar alumno")
    return render_template("alumnos.html", form=create_form)


@app.route("/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        id=request.args.get('id')
        #slect*from alumnos where id=id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first() 
        nombre=alum1.nombre
        apaterno=alum1.apaterno
        email=alum1.email
        return render_template("detalles.html", id=id, nombre=nombre, apaterno=apaterno, email=email)
         
           
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
 

