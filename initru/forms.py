from django import forms
from .models import contact_us, CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class contactForm(forms.ModelForm):

    class Meta:
        model = contact_us
        fields = '__all__'
        widgets = {
            'name_contact': forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class':'form-control',
            }),
            'email_contact': forms.EmailInput(attrs={
                'placeholder': 'Электронная почта',
                'class':'form-control',
            }),
            'text_contact': forms.Textarea(attrs={
                'placeholder': 'Сообщение',
                'class':'form-control',
                'style':'resize:none;'
            })
        }



class ChangeNumberUser(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = ['phone_number']


class ChangeEmailUser(forms.ModelForm): 
    class Meta: 
        model = CustomUser
        fields = ['email']


class ChangeAvatarUser(forms.ModelForm):
    avatar = forms.ImageField(label='выберите аватарку')

    class Meta: 
        model = CustomUser
        fields = ['avatar']


class ChangePasswordUser(UserCreationForm):
    class Meta: 
        model = CustomUser
        fields = ['password1', 'password2']


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        kirillit = [RegexValidator('^[а-яА-Я -]*$', message = 'Разрешенные символы (кириллица, пробел и тире.)')]
        lang = [RegexValidator('^[a-zA-Z0-9-]*$', message= 'Разрешенные символы(латиница, цифры и тире).')]

        self.fields['username'].validators = lang
        self.fields['username'].label = 'Логин'
        self.fields['avatar'].label = 'Выберите аватарку'
        self.fields['first_name'].validators = kirillit
        self.fields['last_name'].validators = kirillit
        self.fields['patronymic'].validators = kirillit
        self.fields['region'].empty_label = 'Выберите регион'
        self.fields['street'].empty_label = 'Выберите улицу'
        self.fields['groupStud'].empty_label = 'Выберите группу'
        self.fields['city'].label = 'Выберите город'
        self.fields['role'].empty_label = 'Выберите роль'
        self.fields['gender'].empty_label = 'Выберите пол'
        self.fields['type_user'].label = 'Выберите тип пользователя (тесты зависят от поля)'

    gen = (
        ('m', 'Мужской'),
        ('j', 'Женский')
    )
    gender = forms.Select()

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'patronymic',
            'gender',
            'birthday_date',
            'region',
            'city',
            'email',
            'street',
            'house',
            'flat',
            'username',
            'avatar',
            'phone_number',
            'type_user',
            'groupStud',
            'role',
            'date_end',
            'password1',
            'password2',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Введите имя',
                'class': "form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-orange-500 focus:outline-none shadow mb-2",
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Введите фамилию',
                'class': " form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-orange-500 focus:outline-none shadow mb-2",
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Введите логин',
                'class': " form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-orange-500 focus:outline-none shadow mb-2",
                'style':'margin-top:32px;',
            }),
            'patronymic': forms.TextInput(attrs={
                'placeholder': 'Введите отчество',
                'class': " form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-orange-500 focus:outline-none shadow mb-2",
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введите почту',
                'class': " form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-orange-500 focus:outline-none shadow",
                'style':'margin-top:52px;'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;'
            }),
            'birthday_date': forms.DateInput(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow',
                'style':'height:38px;',
                'type':'date',
            }),
            'date_end': forms.DateInput(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2 mt-4',
                'style':'height:38px;',
                'type':'date',
            }),
            'region': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;',
            }),
            'street': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;',
            }),
            'groupStud': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;',
            }),
            'type_user': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;',
            }),
            'role': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow',
                'style':'height:38px;',
            }),
            'house': forms.NumberInput(attrs={
                'placeholder': 'Введите номер дома',
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2 mt-2',
                'style':'height:38px;',
            }),
            'flat': forms.NumberInput(attrs={
                'placeholder': 'Введите этаж',
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2',
                'style':'height:38px;',
            }),
            'phone_number': forms.NumberInput(attrs={
                'placeholder': 'Введите номер телефона',
                'class': 'form-select block w-full px-3 py-1.5 text-base text-gray-700 bg-white  border border-solid border-gray-300 rounded transition ease-in -out m-0 focus: text-gray-700 focus: bg-white focus:border-orange-600 focus: outline-none shadow mb-2 mt-3',
                'style':'height:38px;',
            }),
        }