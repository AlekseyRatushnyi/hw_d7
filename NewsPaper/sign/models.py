from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )



def send_greeting(user_email):
    msg = EmailMultiAlternatives(
        subject="Приветствуем",
        body='Вы зарегестировались на новостном портале!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user_email
        )

    msg.send()

class BasicSignupForm(SignupForm):


    def save(self, request):
        user_email = []
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        user_email.append(user.email)
        send_greeting(user_email)
        return user


