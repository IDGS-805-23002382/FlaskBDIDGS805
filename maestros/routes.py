from . import maestros_bp
from flask import render_template, request, redirect, url_for
import forms
from models import Maestros
from models import db


@maestros_bp.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"


@maestros_bp.route("/", methods=['GET','POST'])
@maestros_bp.route("/maestros")
def maestros():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
    return render_template(
        "maestros/listadoMes.html",
        form=create_form,
        maestros=maestros
    )

@maestros_bp.route('/registrar', methods=['GET', 'POST'])
def registrarMaestro():
    form = forms.UserForm2()

    if form.validate_on_submit():
        nuevo_maestro = Maestros(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )

        db.session.add(nuevo_maestro)
        db.session.commit()

        return redirect(url_for('maestros.maestros'))

    return render_template(
        'maestros/maestros.html',
        form=form
    )
    
# DETALLE
@maestros_bp.route('/detalle/<int:id>')
def detallesMaes(id):
    maestro = Maestros.query.get_or_404(id)
    return render_template('maestros/detallesMaes.html', maestro=maestro, nombre=maestro.nombre,
    apellidos=maestro.apellidos,
    email=maestro.email,
    especialidad=maestro.especialidad)



@maestros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def modificarMaes(id):
    maestro = Maestros.query.get_or_404(id)
    form = forms.UserForm2(obj=maestro)

    if form.validate_on_submit():
        maestro.nombre = form.nombre.data
        maestro.apellidos = form.apellidos.data
        maestro.especialidad = form.especialidad.data
        maestro.email = form.email.data

        db.session.commit()
        return redirect(url_for('maestros.maestros'))

    return render_template(
        'maestros/modificarMaes.html',
        form=form,
        maestro=maestro
    )

@maestros_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarMaes(id):
    maestro = Maestros.query.get_or_404(id)
    form = forms.UserForm2(obj=maestro)

    if form.validate_on_submit():
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('maestros.maestros'))

    return render_template(
        'maestros/eliminarMaes.html',
        form=form,
        maestro=maestro
    )
