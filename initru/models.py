from django.db import models
from django.contrib.auth.models import AbstractUser
from smart_selects.db_fields import ChainedForeignKey


# Регионы
class Region(models.Model):
    name_region = models.CharField(
        'Название Региона',
        max_length=64
    )

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return f'{self.name_region}'

# улицы
class Street(models.Model):
    name_street = models.CharField(
        'Название улицы',
        max_length=64
    )

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'

    def __str__(self):
        return f'ул. {self.name_street}'

# города
class City(models.Model):
    name_city = models.CharField(
        'Название города',
        max_length=50
    )
    postal_code = models.IntegerField(
        'Почтовый индекс'
    )
    region  = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        null=False,
        verbose_name='Регион'
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name_city


# инструктажи
class inst(models.Model):
    name_instruction = models.CharField(
        'Название инструктажа',
        max_length=64
    )
    date_period = models.IntegerField(
        'Период инструктажа'
    )

    def __str__(self):
        return self.name_instruction

    class Meta:
        verbose_name = 'Инструктаж'
        verbose_name_plural = 'Инструктажи'

    @staticmethod  # возвращение названий
    def get_all_names():
        return inst.objects.all()[:5]

# специальности
class Spec(models.Model):
    name_special = models.CharField(
        'Название специальности',
        max_length=255
    )
    encryption_special = models.CharField(
        'Шифр специальности',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return "%s - %s " % (self.name_special, self.encryption_special)

# роли
class role(models.Model):
    name_role = models.CharField(
        'Название роли',
        max_length=25
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name_role

# группы
class Groups(models.Model):
    name_group = models.CharField(
        'Название группы',
        max_length=8
    )
    special  = models.ForeignKey(
        Spec, on_delete=models.CASCADE,
        null=False, verbose_name='Специальность'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name_group

# типы пользователей
class typeuser(models.Model):
    name_type_user = models.CharField(
        "Название типа пользователя",
        max_length=15
    )

    class Meta:
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Тип пользователей'

    def __str__(self):
        return self.name_type_user

# тест
class test(models.Model):
    instruction = models.ForeignKey( inst, on_delete=models.CASCADE, verbose_name='Инструктаж' )
    name_test = models.CharField( 'Название теста инструктажа', max_length=125 )
    number_of_questions = models.IntegerField('Количество вопросов') ##
    time = models.IntegerField('Ограничение по времени') ##
    required_score_to_pass = models.IntegerField('Рекомендуемый балл в %', help_text='Рекомендуемый балл в %')
    type_user  = models.ForeignKey(typeuser, on_delete=models.CASCADE, verbose_name='Тип пользователя')
    file = models.FileField( 'Файл к тесту', upload_to='instr/', null=True, blank=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'{self.instruction} - {self.name_test}'

    @staticmethod
    def get_need_instr(request, id):
        return test.objects.all().filter(
            instruction = id
            ).filter(type_user = request.user.type_user)
    
    def get_questions(self):
        pass 

# вопросы
class question(models.Model):
    test  = models.ForeignKey(
        test, on_delete=models.CASCADE,
        verbose_name='Номер теста'
    )
    question = models.CharField(
        'Вопрос',
        max_length=255
    )
    answer = models.CharField(
        'Ответы',
        max_length=64
    )
    score = models.FloatField(
        'балл'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.test } - {self.question}'

# обратная связь
class contact_us(models.Model):
    name_contact = models.CharField(
        "Имя пользователя",
        max_length=125
    )
    email_contact = models.EmailField(
        "Электронная почта пользователя",
    )
    text_contact = models.TextField(
        "Сообщение пользователя",
        max_length=350
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

# комплекс
class complex(models.Model):
    name_complex = models.CharField(
        'Название',
        max_length=255
    )
    image_complex = models.ImageField(
        'Изображение',
        upload_to='images/startPage/complex/'
    )

    def __str__(self) -> str:
        return self.name_complex

    class Meta:
        verbose_name = 'Программный комлекс'
        verbose_name_plural = 'Программные комлексы'

    @staticmethod
    def get_all_names():
        return complex.objects.all()

# кустом юзер
class CustomUser(AbstractUser):  # custom user for Users with django
    gen = (
        ('m', 'Мужской'),
        ('j', 'Женский')
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=250,
    )
    gender = models.CharField(
        'Пол', choices=gen, 
        max_length=3, null=True,
    )
    birthday_date = models.DateField(
        'Дата рождения', null=True,
    )
    region  = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        null=True, verbose_name='Регион',
    )
    city  = ChainedForeignKey(
        City,
        chained_field='region',
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        null=True,
        sort=True)
    
    street  = models.ForeignKey(
        Street, on_delete=models.CASCADE,
        null=True, verbose_name='Улица',
    )
    house = models.IntegerField(
        "Номер дома", null=True,
    )
    flat = models.IntegerField(
        'Этаж', null=True,
    )
    avatar = models.ImageField(
        upload_to='images/users/',
        null=True,
        blank=True,
    )
    
    phone_number = models.TextField(
        'Номер телефона', max_length=15,unique=True, 
        blank=False, null=True,
    )
    
    type_user  = models.ForeignKey(
        typeuser, on_delete=models.CASCADE,
        verbose_name='Тип пользователя', null=True,
    )
    groupStud  = models.ForeignKey(
        Groups, on_delete=models.CASCADE,
        verbose_name='Группа', null=True, 
        blank=True
    )
    role  = models.ForeignKey(
        role, on_delete=models.CASCADE,
        null=True, verbose_name='Роль',
    )
    date_end = models.DateField(
        'Дата завершения зачисления',
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'


    @staticmethod
    def get_count_users():
        return CustomUser.objects.count()

    @staticmethod #получение нужного профиля
    def get_user(request):
        return CustomUser.objects.get(
                pk=request.user.id
                )
    


# результаты
class res(models.Model):
    user  = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    instruction  = models.ForeignKey(
        inst, on_delete=models.CASCADE,
        verbose_name='Инструктаж'
    )
    date_instruction = models.DateTimeField(
        'Дата начала инструктажа'
    )
    result = models.IntegerField(
        'Результат'
    )
    cause = models.CharField(
        'Причина',
        max_length=255
    )

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

# ответы на вопросы
class answers(models.Model):
    question  = models.ForeignKey(
        question, on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    result  = models.ForeignKey(
        res,
        on_delete=models.CASCADE,
        verbose_name='Результат'
    )
    score = models.IntegerField(
        'Балл'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
