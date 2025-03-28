from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User
from .services import FormClean


class ProfileForm(FormClean, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте ваш Никнейм.',
            'help_text': "!@@@@@"
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'help_text': "!@@@@@"
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите страну'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите город'
        })

    class Meta:
        model = User
        fields = ('username', 'name', 'country', 'avatar', 'city',)
        exclude = ('password1', 'password2')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_user = User.objects.get(password=password)
        return password_user.password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким username уже существует.")

        return username

    def clean(self):
        """Валидация на проверку полей (чтобы не было запрещенных слов)"""
        super().clean()


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })


class CustomUserCreationForm(FormClean, UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш никнейм.'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    def clean(self):
        """Валидация на проверку полей (чтобы не было запрещенных слов)"""
        super().clean()
