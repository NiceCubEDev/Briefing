from django.shortcuts import render, redirect
from .forms import contactForm, CreateUserForm
from django.contrib import messages
from .models import inst, complex, CustomUser, test, question, answers, res
from django.http import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def mainView(request):

    page_name = 'main.html'
    
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
    return render(request, page_name, values)


#get_about_us
def aboutPageView(request):
    page_name = 'about.html'
    return render(request, page_name)

#get_contact
def contactPageView(request):
    page_name = 'contact.html'
    return render(request, page_name)

# get profile 
@login_required  # обязательная авторизация
def profileView(request):
    page_name = 'profile.html'
    return render(request, page_name)

@login_required  # обязательная авторизация
def getDetailProfile(request):
    page_name = 'profiile_detail_remaster.html'
    return render(request, page_name)


@login_required  # обязательная авторизация
def getEditProfile(request): 
    page_name = 'profile_edit.html'

    if request.method == 'POST': 
        print(request.POST)

    return render(request, page_name)

    

@login_required  # обязательная авторизация
def briefPageView(request):

    page_name = "user_tests/user_themes_tests_list.html"
    themesInstructions = inst.objects.all()

    values = {
        'themes':themesInstructions,
    }

    return render(request, page_name, values)


@login_required  # обязательная авторизация
def testsPageView(request, id):

    template_name = 'user_tests/user_tests_list.html'
    themesInstructions = inst.objects.get(id = id) # model inst

    tests = test.get_need_instr(request, id) # model test

    values = {
        'test' : tests,
        'themes': themesInstructions,
    }

    return render(request, template_name, values)


@login_required  # обязательная авторизация
def testView(request, num, id): 

    page_name = 'user_tests/user_tests_test.html'
    quiz = test.objects.get(instruction = id, type_user=request.user.type_user, pk = num)
    values = {
        'test':quiz,
    }

    return render(request, page_name, values)
        

@login_required
def createUserAdmin(request):
    page_name = 'admin/createUser.html'
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
        return render(request, page_name, values)
    else:
        return render(request, "error.html")


def testDataView(request, num, id):
    quiz = test.objects.get(instruction = id, type_user=request.user.type_user, pk = num)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data':questions,
        'time':quiz.time
    })


def testDataSaveView(request, num, id): # id - инструктаж # num - номер теста
    if request.method == 'POST':
        questions = [] # list с в вопросами
        data = request.POST
        data_ = dict(data.lists()) # в хороший список
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        for k in data_.keys(): # прогонка по вопросам 
            # print('Вопрос ключ:', k)
            quest = question.objects.get(name=k)
            questions.append(quest) # Добавляем в список вопросов
        
        user = request.user
        quiz = test.objects.get(pk=num) # получение нужного теста

        score = 0 # балл
        multiper = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.name) # выбранные ответы

            if a_selected !="":
                question_answers = answers.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct: 
                            correct_answer = a.text
                results.append({str(q):{'correct_answer':correct_answer, 'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})
        
        countAnswers = score
        score_ = score * multiper
        res.objects.create(
            user = user,
            instruction_id = quiz.instruction.id,
            quiz = quiz,
            date_instruction = timezone.now(),
            result = score_,
            mark = '123',
        )

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed':True, 'score':score_, 'results':results, 'countAnswers':countAnswers})
        else:
            return JsonResponse({'passed':False, 'score':score_, 'results':results, 'countAnswers':countAnswers})


                

