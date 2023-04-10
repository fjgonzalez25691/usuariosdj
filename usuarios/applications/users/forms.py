from django import forms  

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
        
        
       
        
