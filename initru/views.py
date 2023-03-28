from django.shortcuts import render, redirect
# формы
from .forms import contactForm, CreateUserForm, ChangeNumberUser, ChangeEmailUser, ChangeAvatarUser, ChangePasswordUser
# from django.contrib import messages
# для условий
from django.db.models import Q
# модели 
from .models import inst, complex, CustomUser, test, question, answers, res, downloadInstructionsForTests, typeuser, Groups
# варианты ответов
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
# обязательная авторизация
from django.contrib.auth.decorators import login_required
# получение времени
from django.utils import timezone
# чат бот
from deeppavlov import build_model
# импорт ворд
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.section import WD_ORIENTATION


# чат-бот
def chatbot_responseView(request):

    page_name = 'bot.html'  # страница

    if request.method == 'POST':
        data = {}
        query = request.POST
        user_text = query['message']
        model = build_model('kbqa_cq_ru', download=True)
        bot_response = model([user_text])
        data['status'] = 'ok'
        return JsonResponse({'data': data, 'response': bot_response[0]})

    return render(request, page_name)


# главная
def mainView(request):

    page_name = 'main.html'

    users = CustomUser.get_count_users()  # количество пользователей
    # количество пройденных инструктажей
    passed_brief = res.objects.filter(mark='Сдан').count() or 0
    count_brief = test.objects.all().count() or 0  # количество инструктажей

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
        'contact': contact,
        'instr': getInstr,
        'complex': getComplex,
        'countUser': users,
        'pb': passed_brief,
        'cb': count_brief,
    }
    return render(request, page_name, values)


# get_about_us
def aboutPageView(request):
    page_name = 'about.html'
    return render(request, page_name)


# get_contact
def contactPageView(request):
    page_name = 'contact.html'
    return render(request, page_name)


@login_required(login_url='account/login/')
def journalView(request):

    page_name = 'forOss/journal.html'

    role = list(request.user.groups.values_list(
        'name', flat=True))  # получение поли

    if request.user.is_superuser or role[0] == 'Специалист по охране труда':

        obj_res = None  # Для результатов
        obj_briefs = inst.objects.all()  # получение инструктажей
        obj_type_users = typeuser.objects.all()  # получение тип пользователей
        obj_groups = Groups.objects.all()  # получение групп
        obj_quizes = test.objects.all()  # получение тестов
        obj_results_user = res.objects.filter(mark='Сдан')  # получение зачетов

        if 'import-doc' in request.POST:  # условие для скачивания
            print(request.POST)
            if request.POST['date_start'] != '' and request.POST['date_end'] != '': # Если есть даты
                try:
                    obj_result = res.objects.filter(
                        user__type_user=request.POST['type_user'],
                        instruction=request.POST['type_brief'],
                        user__groupStud_id=request.POST['group'],
                        quiz__id=request.POST['quiz'],
                        date_instruction__range=(request.POST['date_start'],
                                                    timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)),
                        
                        date_instruction_end__range=(request.POST['date_end'],
                                                    timezone.localtime(timezone.now()).replace(hour=23, minute=59, second=0, microsecond=0)),
                        
                        mark=request.POST['mark'],
                    )
                    
                except res.DoesNotExist:
                    obj_result = []

            # styles for docs
            alignment_dict = {
                'justify':WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                'center':WD_PARAGRAPH_ALIGNMENT.CENTER,
                'right':WD_PARAGRAPH_ALIGNMENT.RIGHT,
                'left':WD_PARAGRAPH_ALIGNMENT.LEFT,
            }

            orient_dict = {
                'portrait':WD_ORIENTATION.PORTRAIT,
                'landscape':WD_ORIENTATION.LANDSCAPE,
            }
            #####
            
            if len(obj_result) > 0: # если есть данные то
                # code for docx
                
                document = Document()

                document.add_heading('Привет')

                p = document.add_paragraph()
                p.add_run('Это болд предложение, а дальше простое - ').bold = True
                p.add_run('ДА')

                # document.add_paragraph(
                # 'first item in unordered list', style='ListBullet'
                # )
                # document.add_paragraph(
                # 'first item in ordered list', style='ListNumber'
                # )

                #document.add_picture('monty-truth.png', width=Inches(1.25))

                # table = document.add_table(rows=1, cols=3)
                # hdr_cells = table.rows[0].cells
                # hdr_cells[0].text = 'Qty'
                # hdr_cells[1].text = 'Id'
                # hdr_cells[2].text = 'Desc'

                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename=download.docx'

                document.save(response)
                return response
            else: 
                return HttpResponseBadRequest()


        if request.POST: # для аякс условие
            print('я здесь')
            if request.POST['id_date_start'] != '' and request.POST['id_date_end'] != '': # Если есть даты
            # if request.POST['id_date_start'] != '' and request.POST['id_date_end'] != '':
                try:
                    obj_result = res.objects.filter(
                        user__type_user=request.POST['id_type_user'],
                        instruction=request.POST['id_brief'],
                        user__groupStud_id=request.POST['id_group'],
                        quiz__id=request.POST['id_quiz'],
                        date_instruction__range=(request.POST['id_date_start'],
                                                    timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)),
                        
                        date_instruction_end__range=(request.POST['id_date_end'],
                                                    timezone.localtime(timezone.now()).replace(hour=23, minute=59, second=0, microsecond=0)),
                        
                        mark=request.POST['mark'],
                    )
                except res.DoesNotExist:
                    obj_result = []

            elif request.POST['id_date_start'] != '': # если есть начальная дата
                try:
                    obj_result = res.objects.filter(
                        user__type_user=request.POST['id_type_user'],
                        instruction=request.POST['id_brief'],
                        user__groupStud_id=request.POST['id_group'],
                        quiz__id=request.POST['id_quiz'],
                        date_instruction__range=(request.POST['id_date_start'],
                                                    timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)),
                        mark=request.POST['mark'],
                    )
                except res.DoesNotExist:
                    obj_result = []

            else: # иначе без дат 
                try:
                    obj_result = res.objects.filter(
                        user__type_user=request.POST['id_type_user'],
                        instruction=request.POST['id_brief'],
                        user__groupStud_id=request.POST['id_group'],
                        quiz__id=request.POST['id_quiz'],
                        mark=request.POST['mark'],
                    )
                except res.DoesNotExist:
                    obj_result = []


            if len(obj_result) > 0:

                data_list = []  # лист для данных после фильтра

                for row in obj_result:
                    data_list.append({
                        'surname': str(row.user.last_name),
                        'name': str(row.user.first_name),
                        'patro': str(row.user.patronymic),
                        'group': str(row.user.groupStud),  # группа
                        # тип пользователя
                        'type_user': str(row.user.type_user),
                        # тип пользователя (параметр в тестах)
                        'type_user_test': str(row.quiz.type_user),
                        # название инструктажа
                        'brief': str(row.instruction.name_instruction),
                        'quiz_name': str(row.quiz.name_test),
                        'date_start': row.date_instruction,
                        'date_end': row.date_instruction_end,
                        'score': str(row.result),
                        'mark': str(row.mark),
                    })

                obj_res = data_list
                message = 'Успешно!'
                status = 'ok'

            else:
                message = 'Данные не найдены.'
                status = 'error'

            return JsonResponse({'result': obj_res, 'status': status, 'message': message}, safe=False)
    else:
        return render(request, "error.html")

    values = {
        'type_brief': obj_briefs,
        'type_users': obj_type_users,
        'groups': obj_groups,
        'quiz': obj_quizes,
        'users': obj_results_user,
    }

    return render(request, page_name, values)


# это профиль
@login_required  # обязательная авторизация
def profileView(request):

    page_name = 'profile.html'

    if request.method == 'POST':
        data = {}  # for messages
        user = request.user


        if user.check_password(request.POST['password']):

            # проверка на наличие номера телефона в запросе
            if request.POST.get('phone_number'):  # если отправили номер телефона
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
            if request.POST.get('email'):  # если отправили почту
                if user.email != request.POST['email']:
                    form = ChangeEmailUser(request.POST)
                    if form.is_valid():
                        user.email = request.POST['email']
                        user.save()
                        data['message'] = f'{user.first_name}, Вы успешно сменили электронную почту!'
                        data['status'] = 'ok'
                        return JsonResponse(data)
                    else:
                        data['message'] = 'Введите корректную электронную почту!'
                        data['status'] = 'error'

                else:
                    data['message'] = 'Новая почта совпадает с старым'
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
            if request.FILES:  # если отправили почту
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

    obj_res = res.objects.filter(
        user=request.user).order_by("-date_instruction")

    values = {
        'obj': obj_res
    }

    return render(request, page_name, values)


@login_required
def passFilterView(request):
    obj_res = None # для результатов. 
    if request.method == 'POST': # Если метод пост
        if request.POST.get('filter'): # Если существует элемент фильтра
            print(request.POST['filter'])
            
            try:
                obj_res = res.objects.filter(user = request.user).order_by(request.POST['filter']) # получение данных
            except res.DoesNotExist:
                obj_res = [] # если не получилось, то 
            
            if len(obj_res) > 0: # длинна массива больше 0

                data_list = [] # переменная лист для фильтра

                for row in obj_res:
                    data_list.append(
                        {
                            'name_brief':str(row.instruction.name_instruction),
                            'quiz_name':str(row.quiz.name_test),
                            'date_start':row.date_instruction,
                            'result':row.result,
                            'mark':row.mark
                        }
                    )
                
                obj_res = data_list

                message = 'Успешно!'
                status = 'ok'
            else:
                message = 'Данные не найдены'
                status = 'error'
            
            return JsonResponse({'result':obj_res, 'status': status, 'message': message})
            
    return JsonResponse({'status':'good night'})

# проверка о наличии файла
@login_required
def checkFileDownloadedView(request, id):
    data = {}
    if request.method == 'POST':
        obj_query = downloadInstructionsForTests.objects.filter(
            user=request.user, test=request.POST['quiz-pk']).count()
        if obj_query == 0:
            downloadInstructionsForTests.objects.create(
                user=request.user,
                test_id=request.POST['quiz-pk']
            )
            data['status'] = 'ok'
        else:
            data['status'] = 'warning'
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest()


# Проверка о прохождении теста
@login_required
def checkPassedView(request, id):
    data = {}
    if request.method == 'POST':
        obj_query_file = downloadInstructionsForTests.objects.filter(
            user=request.user, test=request.POST['quiz']).count()
        if obj_query_file != 0:
            passed_brief = res.objects.filter(
                instruction=id, quiz=request.POST['quiz'], mark='Сдан', user=request.user).count()
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


# мои возможности
@login_required  # обязательная авторизация
def actionUserView(request):

    page_name = 'action.html'

    return render(request, page_name)


# редактирование профиля
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
        'themes': themesInstructions,
    }
    return render(request, page_name, values)


# страница с тестами инструктажами
@login_required  # обязательная авторизация
def testsPageView(request, id):
    page_name = 'user_tests/user_tests_list.html'
    themesInstructions = inst.objects.get(id=id)  # model inst
    tests = test.get_need_instr(request, id)  # model test
    values = {
        'test': tests,
        'themes': themesInstructions,
    }
    return render(request, page_name, values)


# получение страницы теста
@login_required  # обязательная авторизация
def testView(request, num, id):
    page_name = 'user_tests/user_tests_test.html'
    quiz = test.objects.get(
        instruction=id, type_user=request.user.type_user, pk=num)
    passed_brief = res.objects.filter(
        instruction=id, quiz=quiz, mark='Сдан', user=request.user).count()
    if passed_brief == 0:
        values = {
            'test': quiz,
        }
        return render(request, page_name, values)
    else:
        return HttpResponseBadRequest()


# получение вопросов
@login_required
def testDataView(request, num, id):

    quiz = test.objects.get(
        instruction=id, type_user=request.user.type_user, pk=num)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


# проверка теста
@login_required
def testDataSaveView(request, num, id):  # id - инструктаж # num - номер теста
    if request.method == 'POST':

        user = request.user  # пользователь
        # получение нужного теста
        quiz = test.objects.get(pk=num, instruction=id,
                                type_user=request.user.type_user)

        questions = []  # list с в вопросами
        data = request.POST
        data_ = dict(data.lists())  # в хороший список
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():  # прогонка по вопросам
            quest = question.objects.get(name=k)
            questions.append(quest)  # Добавляем в список вопросов

        score = 0  # балл
        multiper = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.name)  # выбранные ответы

            if a_selected != "":  # если ответ не пустой, то
                question_answers = answers.objects.filter(
                    question=q)  # получаем ответы по вопросу
                for a in question_answers:
                    if a_selected == a.text:  # если выбранный ответ совпадает с ответов настоящим
                        if a.correct:
                            score += 1  # плюс отвеченный вопрос
                            correct_answer = a.text  # сохраняем правильный ответ
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        countAnswers = score
        score_ = score * multiper

        # если человек набрал больше баллов, чем в условии теста, то сохраняем его и отправляем успешно
        if score_ >= quiz.required_score_to_pass:
            res.objects.create(
                user=user,
                instruction_id=quiz.instruction.id,
                quiz=quiz,
                date_instruction=timezone.now(),
                result=score_,
                mark='Сдан',
            )
            return JsonResponse({'passed': True, 'score': score_, 'results': results, 'countAnswers': countAnswers})
        else:
            res.objects.create(
                user=user,
                instruction_id=quiz.instruction.id,
                quiz=quiz,
                date_instruction=timezone.now(),
                result=score_,
                mark='Не сдан',
            )
            return JsonResponse({'passed': False, 'score': score_, 'results': results, 'countAnswers': countAnswers})
