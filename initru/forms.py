import phonenumbers
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, contact_us


class contactForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = "__all__"
        widgets = {
            "name_contact": forms.TextInput(
                attrs={
                    "placeholder": "Имя",
                    "class": "form-control",
                }
            ),
            "email_contact": forms.EmailInput(
                attrs={
                    "placeholder": "Электронная почта",
                    "class": "form-control",
                }
            ),
            "text_contact": forms.Textarea(
                attrs={"placeholder": "Сообщение", "class": "form-control", "style": "resize:none;"}
            ),
        }


class ChangeNumberUser(forms.ModelForm):
    phone_number = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["phone_number"]

    def clean_phone_number(self):  # валидация номера телефона
        phone_number = self.cleaned_data.get("phone_number")  # записываем в переменную
        z = phonenumbers.parse(phone_number, region="RU")  # проверка
        if not phonenumbers.is_valid_number(z):  # Если не валидный
            raise forms.ValidationError("У номера телефона неправильный формат!")
        return phone_number


class ChangeEmailUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]


class ChangeAvatarUser(forms.ModelForm):
    avatar = forms.ImageField(
        label="Выберите аватарку",
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ["avatar"]


class ChangePasswordUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["password1", "password2"]
