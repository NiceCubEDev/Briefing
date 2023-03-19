from django.shortcuts import render, redirect
from .forms import contactForm, CreateUserForm, ChangeNumberUser, ChangeEmailUser, ChangeAvatarUser, ChangePasswordUser
from django.contrib import messages
from django.db.models import Q
from .models import inst, complex, CustomUser, test, question, answers, res, downloadInstructionsForTests, typeuser, Groups
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from deeppavlov import build_model


#чат-бот
def chatbot_responseView(request):

    page_name = 'bot.html' # страница

    if request.method == 'POST':
        data={}
        query = request.POST
        user_text = query['message']
        model = build_model('kbqa_cq_ru', download=True)
        bot_response = model([user_text])
        data['status'] = 'ok'
        return JsonResponse({'data':data,'response':bot_response[0]})
  

    return render(request, page_name)


# главная
def mainView(request):

    page_name = 'main.html'
    
    users = CustomUser.get_count_users() # количество пользователей
    passed_brief = res.objects.filter(mark='Сдан').count() or 0 # количество пройденных инструктажей
    count_brief = test.objects.all().count() or 0 # количество инструктажей

    getInstr = inst.get_all_names()
    getComplex = complex.get_all_names()
    users = CustomUser.get_count_users()
    contact = contactForm()

    if request.method == 'POST':
        data = {}
        print(request.POST)
        form = contactForm(request.POST)
        if form.is_valid():
            form.save()
            data['message'] = 'Вы успешно отправили!'
            data['status'] = 'ok'
            return JsonResponse(data)
        else:
            data['message'] = 'Введите правильные данные!'
            data['status'] = 'error'
            return JsonResponse(data)
        
        
    values = {
        'contact':contact,
        'instr':getInstr, 
        'complex':getComplex,
        'countUser':users,
        'pb':passed_brief,
        'cb':count_brief,
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


@login_required(login_url='account/login/')
def journalView(request):
    
    page_name = 'forOss/journal.html'
    obj_res = None # Для результатов
    obj_briefs = inst.objects.all()
    obj_type_users = typeuser.objects.all()
    obj_groups = Groups.objects.all()
    obj_quizes = test.objects.all()
    obj_results_user = res.objects.all()


    if request.method == "POST":


        obj_result = res.objects.filter(
                user__type_user = request.POST['id_type_user'], 
                instruction = request.POST['id_brief'], 
                user__groupStud_id=request.POST['id_group'],
                quiz__id = request.POST['id_quiz'],
                date_instruction__range=(request.POST['id_date_start'] or None, 
                                        timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)),  
            )
        
        if len(obj_result) > 0:
            data_list=[] # лист для данных после фильтра
            for row in obj_result:
            
                data_list.append( 
                        {
                        'surname':row.user.last_name, 
                        'name':row.user.first_name,
                        'patro':row.user.patronymic, 
                        'group':row.user.groupStud, # группа
                        'type_user':row.user.type_user, # тип пользователя
                        'type_user_test':row.quiz.type_user, # тип пользователя (параметр в тестах)
                        'brief':row.instruction.name_instruction, # название инструктажа
                        'quiz_name':row.quiz.name_test, 
                        'date_start':row.date_instruction,
                        'date_end':row.date_instruction_end,
                        'score':row.result,
                        'mark':row.mark,
                        }
                )

            obj_res = data_list
            message = 'Успешно!'
            status = 'ok'
        else:    
            obj_result = 'Нет данных'
            message = 'Выберите правильные параметры.'
            status = 'error'

        return JsonResponse({'result':obj_res, 'status':status,'message':message})

    values = {
        'type_brief': obj_briefs,
        'type_users': obj_type_users,
        'groups': obj_groups,
        'quiz':obj_quizes,
        'users':obj_results_user,
    }

    return render(request, page_name, values)

# это профиль
@login_required  # обязательная авторизация
def profileView(request):
    page_name = 'profile.html'

    if request.method == 'POST': 
        data = {} # for messages
        user = request.user


        # if request.POST.get('download'):
        #     document = Document()
            
        #     items = (
        #         ('салават', '19012004', 'плюшевые котята')
        #     ) 

        #     table = document.add_table(1, len(items[0]))
        #     table.style = 'Light Shading  Accent 1'
        #     head_cells = table.rows[0].cells

        #     for i, item in enumerate(['имя ', 'дата рождения', 'описание']):
        #         p = head_cells[i].paragraphs[0]
        #         p.add_run(item).bold = True
            
        #     for row in items:
        #         cells = table.add_row().cells
        #         for i,item in enumerate(row):
        #             cells[i].text = str(item)
        #             if i == 2:
        #                 cells[i].paragraphs[0].runs[0].font.name = 'Arial'
                        
        #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        #     response['Content-Disposition'] = 'attachment; filename=download.docx'
        #     document.save(response)

        #     return response

        if user.check_password(request.POST['password']):

            # проверка на наличие номера телефона в запросе
            if request.POST.get('phone_number'): # если отправили номер телефона
                if user.phone_number != request.POST['phone_number']: 
                    form = ChangeNumberUser(request.POST)
                    if form.is_valid():
                        user.phone_number = request.POST['phone_number']
                        user.save()
                        data['message'] = f'{user.first_name}, Вы успешно сменили номер телефона!'
                        data['status'] = 'ok'
                        return JsonResponse(data)
                    else: 
                        data['message'] = 'Введите правильный номер телефона!'
                        data['status'] = 'error'
                else: 
                    data['message'] = 'Вы ввели настоящий номер телефона!'
                    data['status'] = 'error'


            # проверка на почты в запросе
            if request.POST.get('email'): # если отправили почту
                if user.email != request.POST['email']:
                    form = ChangeEmailUser(request.POST)
                    if form.is_valid():
                        user.email = request.POST['email']
                        user.save()
                        data['message'] = f'{user.first_name}, Вы успешно электронную почту!'
                        data['status'] = 'ok'
                        return JsonResponse(data)
                    else:
                        data['message'] = 'Введите корректную электронную почту!'
                        data['status'] = 'error'


                else: 
                    data['message'] = 'Одинаковая электронная почта, введите правильную!'
                    data['status'] = 'error'


            # смена пароля
            if request.POST.get('password2'):
                if request.POST['password'] != request.POST['password2']:
                    form = ChangePasswordUser(request.POST)
                    if form.is_valid():
                        user.set_password(request.POST['password2'])
                        user.save()
                        data['message'] = f'{user.first_name}, Вы успешно сменили пароль!'
                        data['status'] = 'ok'
                        data['reload'] = 'go'
                        return JsonResponse(data)
                    else:
                        data['message'] = 'Новый пароль не соответствует по требованиям! '
                        data['status'] = 'error'


                else:
                    data['message'] = 'Старый пароль соответствует новому'
                    data['status'] = 'error'


            # проверка на почты в запросе
            if request.FILES: # если отправили почту
                form = ChangeAvatarUser(request.FILES)
                if form.is_valid():
                    user.avatar.delete()
                    user.avatar = request.FILES['avatar']
                    user.save()
                    data['message'] = f'{user.first_name}, Вы успешно сменили фотографию!'
                    data['status'] = 'ok'
                    return JsonResponse(data)
                else:
                    data['message'] = 'Выберите корректную фотографию!'
                    data['status'] = 'error'
                
        else: 
            data['message'] = 'Введите корректный пароль!'
            data['status'] = 'error'


    


        return JsonResponse(data)
    
    return render(request, page_name)


# элемент  с пройденными инструктажами
@login_required
def passedView(request):
    page_name = 'passed_inst.html'

    obj_res = res.objects.filter(user= request.user).order_by("-date_instruction")

    values = {
        'obj':obj_res
    }

    return render(request, page_name, values)


# проверка о наличии файла
@login_required
def checkFileDownloadedView(request, id):
    data = {}
    if request.method == 'POST':
        obj_query = downloadInstructionsForTests.objects.filter(user=request.user, test = request.POST['quiz-pk']).count()
        if obj_query == 0:
            downloadInstructionsForTests.objects.create(
                user = request.user,
                test_id = request.POST['quiz-pk']
            )
            data['status'] = 'ok'
        else:
            data['status'] = 'warning'
        return JsonResponse(data)
    else: 
        return HttpResponseBadRequest()


#Проверка о прохождении теста
@login_required
def checkPassedView(request, id):
    data = {}
    if request.method == 'POST':
        obj_query_file = downloadInstructionsForTests.objects.filter(user = request.user, test=request.POST['quiz']).count()
        if obj_query_file != 0:
            passed_brief = res.objects.filter(instruction = id, quiz = request.POST['quiz'], mark = 'Сдан', user=request.user).count()
            if passed_brief == 0:
                data['status'] = True
            else: 
                data['message'] = 'Вы уже прошли данный инструктаж'
                data['status'] = False
        else: 
            data['message'] = 'Вы не изучили теорию!'
            data['status'] = False
    else:
        return HttpResponseBadRequest()
    return JsonResponse(data)

# элемент мои данные
@login_required  # обязательная авторизация
def getDetailProfile(request):
    page_name = 'profiile_detail_remaster.html'
    return render(request, page_name)


#мои возможности
@login_required  # обязательная авторизация
def actionUserView(request):

    page_name = 'action.html'
 
    return render(request, page_name)


#редактирование профиля
@login_required  # обязательная авторизация
def getEditProfile(request): 
    page_name = 'profile_edit.html'
    return render(request, page_name)

    
# страница с инструктажами
@login_required  # обязательная авторизация
def briefPageView(request):
    page_name = "user_tests/user_themes_tests_list.html"
    themesInstructions = inst.objects.all().order_by("-name_instruction")

    values = {
        'themes':themesInstructions,
    }
    return render(request, page_name, values)


# страница с тестами инструктажами
@login_required  # обязательная авторизация
def testsPageView(request, id):
    page_name = 'user_tests/user_tests_list.html'
    themesInstructions = inst.objects.get(id = id) # model inst
    tests = test.get_need_instr(request, id) # model test
    values = {
        'test' : tests,
        'themes': themesInstructions,
    }
    return render(request, page_name, values)


# получение страницы теста
@login_required  # обязательная авторизация
def testView(request, num, id): 
    page_name = 'user_tests/user_tests_test.html'
    quiz = test.objects.get(instruction = id, type_user=request.user.type_user, pk = num)
    passed_brief = res.objects.filter(instruction = id, quiz = quiz, mark = 'Сдан', user=request.user).count()
    if passed_brief == 0:
        values = {
        'test':quiz,
        }
        return render(request, page_name, values)
    else:
        return HttpResponseBadRequest()
   
# создание пользователя
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

# получение вопросов
@login_required
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


# проверка теста
@login_required
def testDataSaveView(request, num, id): # id - инструктаж # num - номер теста
    if request.method == 'POST':
        
        user = request.user # пользователь 
        quiz = test.objects.get(pk=num, instruction = id, type_user=request.user.type_user) # получение нужного теста


        questions = [] # list с в вопросами
        data = request.POST
        data_ = dict(data.lists()) # в хороший список
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys(): # прогонка по вопросам 
            quest = question.objects.get(name=k)
            questions.append(quest) # Добавляем в список вопросов
        

        score = 0 # балл
        multiper = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.name) # выбранные ответы

            if a_selected !="": # если ответ не пустой, то 
                question_answers = answers.objects.filter(question=q) # получаем ответы по вопросу
                for a in question_answers: 
                    if a_selected == a.text: # если выбранный ответ совпадает с ответов настоящим
                        if a.correct:
                            score += 1 # плюс отвеченный вопрос
                            correct_answer = a.text # сохраняем правильный ответ
                    else:
                        if a.correct: 
                            correct_answer = a.text
                results.append({str(q):{'correct_answer':correct_answer, 'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})
        
        countAnswers = score
        score_ = score * multiper

        if score_ >= quiz.required_score_to_pass: # если человек набрал больше баллов, чем в условии теста, то сохраняем его и отправляем успешно 
            res.objects.create(
                user = user,
                instruction_id = quiz.instruction.id,
                quiz = quiz,
                date_instruction = timezone.now(),
                result = score_,
                mark = 'Сдан',
            )
            return JsonResponse({'passed':True, 'score':score_, 'results':results, 'countAnswers':countAnswers})
        else:
            res.objects.create(
                user = user,
                instruction_id = quiz.instruction.id,
                quiz = quiz,
                date_instruction = timezone.now(),
                result = score_,
                mark = 'Не сдан',
            )
            return JsonResponse({'passed':False, 'score':score_, 'results':results, 'countAnswers':countAnswers})





                

