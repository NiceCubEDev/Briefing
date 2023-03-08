from django.shortcuts import render, redirect
from .forms import contactForm, EditProfileForm, CreateUserForm
from django.contrib import messages
from .models import inst, complex, CustomUser, test
from django.http import *
from django.contrib.auth.decorators import login_required

def mainView(request):

    template_path = 'main.html'
    
    getInstr = inst.get_all_names()
    getComplex = complex.get_all_names()
    users = CustomUser.get_count_users()

    if request.method == 'POST':
        contact = contactForm(request.POST or None)
        if contact.is_valid():
            contact.save()
            messages.success(request,'Успешно отправлено!')
            return HttpResponseRedirect('/#link')
        else:
            messages.error(request, 'Введите корректные данные')
            return HttpResponseRedirect('/#link')
    else:
        contact = contactForm()
    values = {
        'contact':contact,
        'instr':getInstr, 
        'complex':getComplex,
        'countUser':users,
    }
    return render(request, template_path, values)


#get_about_us
def aboutPageView(request):
    template_path = 'about.html'
    return render(request, template_path)

#get_contact
def contactPageView(request):
    template_path = 'contact.html'
    return render(request, template_path)

# get profile 
@login_required(login_url='/account/login/') # обязательная авторизация
def profileView(request):
    template_path = 'profile.html'
    return render(request, template_path)

@login_required(login_url='/account/login/') # обязательная авторизация
def getDetailProfile(request):
    template_path = 'profiile_detail_remaster.html'
    return render(request,template_path)


@login_required(login_url='account/login/') # обязательная авторизация
def getEditProfile(request): 
    template_path = 'profile_edit.html'
    get_user = CustomUser.get_user(request)
    if request.method == "GET": 
        try:
            edit_form = EditProfileForm
        except:
            get_user = None
    if request.method == "POST":
        edit_form = EditProfileForm()
        get_user.username = request.POST.get("username")
        get_user.phone_number = request.POST.get("phone_number")
        get_user.email = request.POST.get("email")
        if request.FILES:
            get_user.avatar = request.FILES['avatar']
        get_user.save()
        messages.success(request, "Прошло успешно!")
    values = {
        'form':edit_form,
        'DataUser':get_user,
    }

    return render(request, template_path, values)
    

@login_required(login_url='account/login/') # обязательная авторизация
def briefPageView(request):

    template_path = "user_tests/user_themes_tests_list.html"
    themesInstructions = inst.objects.all()

    values = {
        'themes':themesInstructions,
    }

    return render(request, template_path, values)


@login_required(login_url='account/login/') # обязательная авторизация
def testsPageView(request, id):

    template_name = 'user_tests/user_tests_list.html'
    themesInstructions = inst.objects.get(id = id) # model inst

    tests = test.get_need_instr(request, id) # model test

    values = {
        'test' : tests,
        'themes': themesInstructions,
    }

    return render(request, template_name, values)


@login_required(login_url='account/login/') # обязательная авторизация
def testView(request, num, id): 

    template_path = 'user_tests/user_tests_intro.html'
    tests = test.objects.filter(instruction = num, type_user=request.user.type_user, pk = id)
    
    values = {
        'test':tests,
    }

    return render(request, template_path, values)
        

@login_required
def createUserAdmin(request):
    template_path = 'admin/createUser.html'
    if request.user.is_superuser:
        if request.method == 'POST':
            newUser = CreateUserForm(request.POST, request.FILES)
            if newUser.is_valid():
                newUser.save()
                messages.success(request, 'Успешно создан!')
                return redirect('user_create')
            else:
                messages.error(request,'Введите корректные данные!')
                userForm = CreateUserForm()
        else: 
            userForm = CreateUserForm()
        values = {
            'form':userForm,
        }
        return render(request, template_path, values)
    else:
        return render(request, "error.html")


# этап разработки теста для пользователя
# создать форму для вопросов в forms.py
# получать список вопросов, на которые он не ответил.
# спсок вопросов, список ответов и можно сравнить (вариант) 
# можно сделать на JS либо на DJANGO . 
