from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.urls import (
    reverse_lazy,
    reverse
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    authenticate,
    login, 
    logout
)

from django.http import HttpResponseRedirect

from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)
from .models import User
#
from .functions import code_generator

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        #generamos el código
        codigo = code_generator()
        
        usuario = User.objects.create_user(
            #Los datos que necesitamos que están en el formulario los vamos a recuperar directamente del formulario
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombre=form.cleaned_data['nombre'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        ) 
        # enviar el codigo al email del usuario
        asunto = 'Confirmación de mail'
        mensaje = 'Código de verificación: ' + codigo
        email_remitente = 'fjgonzalez25691@gmail.com'
        
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],] )
        #redirigir a pantalla de validación 
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk':usuario.id}
            )
        )
    
class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')
    
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self). form_valid(form)
    
class LogoutView(View):
    
    def get(self, request, *arg, **kwords):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
        
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        #para recuperar el usuario activo
        usuario = self.request.user
        # para hacer la autentificación
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            
        logout(self.request)
        return super(UpdatePasswordView, self). form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')
    
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)