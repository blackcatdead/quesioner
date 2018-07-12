from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from jurica.models import Responden
from django.forms import ModelForm, Textarea, TextInput, NumberInput, EmailInput, Select
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
class RegisterForm(ModelForm):
    class Meta:
        model = Responden
        fields = ['nama', 'email', 'nomor_hp', 'jenis_kelamin', 'usia', 'pendidikan', 'program', 'semester', 'masa_kerja']
        widgets = {
            'nama': TextInput(attrs={'class': 'form-control', 'placeholder': '*Nama'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': '*Email'}),
            'nomor_hp': TextInput(attrs={'class': 'form-control text_type_number', 'placeholder': '*Nomor Hp',}),
            'jenis_kelamin': Select(attrs={'class': 'form-control', 'placeholder': '*Jenis Kelamin'}),
            'usia': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Usia', 'min': 0}),
            'pendidikan': Select(attrs={'class': 'form-control', 'placeholder': '*Pendidikan'}),
            'program': Select(attrs={'class': 'form-control', 'placeholder': '*Program'}),
            'semester': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Semester', 'min': 1}),
            'masa_kerja': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Masa Kerja', 'min': 0}),
        }

	

class LoginForm(forms.Form):
	email = forms.EmailField(label='envelope', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'blank': True}))

class LoginAdminForm(forms.Form):
    username = forms.CharField(label='user', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'blank': True}))
    password = forms.CharField(label='lock', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'blank': True}))

class EditForm(ModelForm):
    class Meta:
        model = Responden
        fields = ['nama', 'nomor_hp', 'jenis_kelamin', 'usia', 'pendidikan', 'program', 'semester', 'masa_kerja', 'status']
        widgets = {
            'nama': TextInput(attrs={'class': 'form-control', 'placeholder': '*Nama'}),
            'nomor_hp': TextInput(attrs={'class': 'form-control text_type_number', 'placeholder': '*Nomor Hp'}),
            'jenis_kelamin': Select(attrs={'class': 'form-control', 'placeholder': '*Jenis Kelamin'}),
            'usia': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Usia', 'min': 0}),
            'pendidikan': Select(attrs={'class': 'form-control', 'placeholder': '*Pendidikan'}),
            'program': Select(attrs={'class': 'form-control', 'placeholder': '*Program'}),
            'semester': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Semester', 'min': 1}),
            'masa_kerja': NumberInput(attrs={'class': 'form-control', 'placeholder': '*Masa Kerja', 'min': 0}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }