from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'project_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-transparent border-light text-light',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-transparent border-light text-light',
                'placeholder': 'your@email.com'
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select bg-transparent border-light text-light'
            }, choices=[
                ('', 'Select a project type'),
                ('portrait', 'Portrait Session'),
                ('event', 'Event Photography'),
                ('commercial', 'Commercial Work'),
                ('other', 'Other')
            ]),
            'message': forms.Textarea(attrs={
                'class': 'form-control bg-transparent border-light text-light',
                'rows': 5,
                'placeholder': 'Tell me about your project...'
            })
        }


class ClientLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class GalleryPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter gallery password'
        }),
        label='Gallery Password'
    )