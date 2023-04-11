from django import forms  
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):
    
    password1= forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    
    password2= forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repita contraseña'
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombre',
            'apellidos',
            'genero',
        )
        
    def clean_password2(self):   
        
        if len(self.cleaned_data['password1']) < 5:
            self.add_error('password1', 'La contraseña debe de tener al menos 5 dígitos')
        elif self.cleaned_data['password2'] != self.cleaned_data["password1"]:
            self.add_error('password2', 'Las contraseñas no coinciden')
            
class LoginForm(forms.Form):  
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'usuario'
            }
        )
    )   
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'contraseña'
            }
        )
    )
    
    def clean(self):         
        cleaned_data = super(LoginForm, self).clean()  
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    
    password1= forms.CharField(
        label='Contraseña      ',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña actual'
            }
        )
    )
    
    password2= forms.CharField(
        label='Nueva Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña nueva'
            }
        )
    )
    
class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)