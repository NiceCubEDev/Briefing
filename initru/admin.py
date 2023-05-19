from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
from django import forms 

#Регионы
@admin.register(Region)
class Region(admin.ModelAdmin):
    list_display = ['name_region']

#Города
@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ['name_city', 'postal_code', 'region']

#Улицы
@admin.register(Street)
class Street(admin.ModelAdmin):
    list_display = ['name_street']


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
  
    add_form = UserCreationForm
    list_display = ("first_name",'last_name', 'patronymic')
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'patronymic', 'email','username', 'password', 'gender','birthday_date','phone_number','region','city','street','house','flat','avatar','type_user','groupStud','role','date_end','groups','is_active','is_staff','is_superuser',)}),
        )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'patronymic', 'email','username', 'password', 'gender','birthday_date','phone_number','region','city','street','house','flat','avatar','type_user','groupStud','role','date_end','groups','is_active','is_staff','is_superuser',)}
            ),
        )


admin.site.register(CustomUser, CustomUserAdmin)


#Специальности
@admin.register(Spec)
class Spec(admin.ModelAdmin):
    list_display = ['name_special', 'encryption_special']


# группы студентов
@admin.register(Groups)
class Groups(admin.ModelAdmin):
    list_display = ['name_group', 'special']


#роли
@admin.register(role)
class role(admin.ModelAdmin):
    list_display = ['name_role']


#тип пользователя
@admin.register(typeuser)
class typeuser(admin.ModelAdmin):
    list_display = ['name_type_user']


# инструктажи
@admin.register(inst)
class inst(admin.ModelAdmin):
    list_display = ['name_instruction', 'date_period']


# Результаты
@admin.register(res)
class res(admin.ModelAdmin):
    list_display = ['user', 'instruction', 'quiz','date_instruction','date_instruction_end', 'result', 'mark', 'attempt']


# тесты
@admin.register(test)
class test(admin.ModelAdmin):
    list_display = ['instruction', 'name_test', 'type_user','file', 'stud_groups','date_target']
    list_filter = ['name_test']

# вопросы и ответы
class AnswerInline(admin.TabularInline):
    model = answers


@admin.register(question)
class question(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['test', 'name', 'created']


# Ответы
@admin.register(answers)
class answer(admin.ModelAdmin):
    list_display = ['question', 'text', 'correct', 'created']


# связь с нами
@admin.register(contact_us)
class contact_us(admin.ModelAdmin):
    list_display = ['name_contact', 'email_contact', 'text_contact']


# Комлексы для главной страницы
@admin.register(complex)
class complex(admin.ModelAdmin):
    list_display = ['name_complex', 'image_complex']


# model for files brief
@admin.register(downloadInstructionsForTests)
class downloadInstructionsForTestsAdmin(admin.ModelAdmin):
    list_display = ['user', 'test']


#назначенные инструктажи отдельным людям
@admin.register(briefsForPeoples)
class briefsForPeoplesAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'date_target']
    list_filter = ['date_target', ]

