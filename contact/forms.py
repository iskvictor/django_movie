from .models import Contact
from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """Форма подписки на email"""
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields =("email", "captcha")
        widgets = {
            "email": forms.TextInput(attrs={"class": "editContent", "placeholder": "Your email.....",
            })

        }
        labels = {
            "email": ""
        }