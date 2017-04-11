from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField( max_length = 20)
    password = forms.CharField( max_length = 20, widget = forms.PasswordInput() )

class CreateUserForm(forms.ModelForm):
    username = forms.CharField( max_length = 20,
        error_messages = {
            'required': 'El username es obligatorio',
            'unique': 'El username ya se encuentra registrado',
            'invalid': 'El username es incorrecto'})
    password = forms.CharField( max_length = 20, widget = forms.PasswordInput(), error_messages = {'required': 'El password es obligatorio'} )
    first_name = forms.CharField( max_length = 60, error_messages = {'required': 'El first name es obligatorio'} )
    last_name = forms.CharField( max_length = 60, error_messages = {'required': 'El last name es obligatorio'} )
    email = forms.CharField( max_length = 150, error_messages = {'required': 'El email es obligatorio','invalid': 'Ingrese un correo valido'})
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','email')
