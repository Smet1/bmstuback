from django.db import models
from django.utils import timezone


class Floor(models.Model):
    class Meta:
        ordering = ['number', ]
        verbose_name = "этаж"
        verbose_name_plural = "этажи"
        db_table = 'floor'

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="номер")

    def __str__(self):
        return "Этаж № {}".format(self.number)


class Cabinet(models.Model):
    class Meta:
        ordering = ['name', ]
        verbose_name = "кабинет"
        verbose_name_plural = "кабинеты"
        db_table = 'cabinet'

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="название"
    )
    auditoria = models.BooleanField(default=True, verbose_name="аудитория")
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        verbose_name="этаж"
    )
    longitude = models.IntegerField(
        verbose_name="широта"
    )
    latitude = models.IntegerField(
        verbose_name="долгота"
    )

    node = models.ForeignKey(
        'main.Cabinet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="выход"
    )

    def __str__(self):
        return self.name


class Degree(models.Model):
    class Meta:
        verbose_name = "ученая степень"
        verbose_name_plural = "ученые степени"
        db_table = 'degree'
        
    name = models.CharField(
        max_length=50,
        verbose_name="название"
    )


class Employee(models.Model):
    class Meta:
        ordering = ['last_name', ]
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"
        db_table = 'employee'

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия"
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name="Отчество"
    )

    degree = models.ForeignKey(
        Degree,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="ученая степень"
    )

    def __str__(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)


class Position(models.Model):
    class Meta:
        verbose_name = "должность"
        verbose_name_plural = "должности"
        db_table = 'position'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def get_current_time():
    return timezone.now().time()


class Schedule(models.Model):
    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "расписание"
        db_table = 'schedule'

    WEEKDAY_CHOICE = (
        (0, 'Пн'),
        (1, 'Вт'),
        (2, 'Ср'),
        (3, 'Чт'),
        (4, 'Пт'),
        (5, 'Сб'),
        (6, 'Вс'),
    )

    WEEK_CHOICE = (
        (0, 'Все'),
        (1, 'Чс'),
        (2, 'Зн'),
    )

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)

    time_from = models.TimeField(
        default=get_current_time,
        verbose_name="от"
    )
    time_to = models.TimeField(
        default=get_current_time,
        verbose_name="до"
    )
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICE,
        verbose_name="день недели"
    )
    week_type = models.IntegerField(
        default=WEEK_CHOICE[0][0],
        choices=WEEK_CHOICE,
        verbose_name="тип недели"
    )


class PosHeld(models.Model):
    class Meta:
        verbose_name = "занимаемая должность"
        verbose_name_plural = "занимаемые должности"
        db_table = 'posheld'

    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="сотрудник"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name="сотрудники"
    )
