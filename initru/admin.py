from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


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


admin.site.register(CustomUser)

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
    list_display = ['user', 'instruction', 'quiz','date_instruction', 'result', 'mark']

# тесты
@admin.register(test)
class test(admin.ModelAdmin):
    list_display = ['instruction', 'name_test', 'type_user','file']

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
# Register your models here.
