from wtforms import Form
from wtforms import IntegerField, StringField, PasswordField, RadioField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id = IntegerField("ID")
    
    nombre = StringField("Nombre", [
        validators.InputRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message="El nombre debe tener entre 4 y 10 caracteres")
    ])
    
    apaterno = StringField("Apaterno", [
        validators.InputRequired(message="El campo es requerido")
    ])
    
    correo = EmailField("Correo", [
        validators.InputRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un correo válido")
    ])
    