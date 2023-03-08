from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *



@admin.register(Region)
class Region(admin.ModelAdmin):
    list_display = ['name_region']

@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ['name_city', 'postal_code', 'region']

@admin.register(Street)
class Street(admin.ModelAdmin):
    list_display = ['name_street']


admin.site.register(CustomUser)

@admin.register(Spec)
class Spec(admin.ModelAdmin):
    list_display = ['name_special', 'encryption_special']


@admin.register(Groups)
class Groups(admin.ModelAdmin):
    list_display = ['name_group', 'special']

@admin.register(role)
class role(admin.ModelAdmin):
    list_display = ['name_role']

@admin.register(typeuser)
class typeuser(admin.ModelAdmin):
    list_display = ['name_type_user']


@admin.register(inst)
class inst(admin.ModelAdmin):
    list_display = ['name_instruction', 'date_period']

@admin.register(res)
class res(admin.ModelAdmin):
    list_display = ['user', 'instruction', 'quiz','date_instruction', 'result', 'mark']


@admin.register(test)
class test(admin.ModelAdmin):
    list_display = ['instruction', 'name_test', 'type_user','file']

class AnswerInline(admin.TabularInline):
    model = answers

@admin.register(question)
class question(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['test', 'name', 'created']


@admin.register(answers)
class answer(admin.ModelAdmin):
    list_display = ['question', 'text', 'correct', 'created']


@admin.register(contact_us)
class contact_us(admin.ModelAdmin):
    list_display = ['name_contact', 'email_contact', 'text_contact']


@admin.register(complex)
class complex(admin.ModelAdmin):
    list_display = ['name_complex', 'image_complex']


# Register your models here.
