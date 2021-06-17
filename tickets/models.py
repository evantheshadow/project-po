from django.db import models
import datetime
from django.utils import timezone
from .functions import *
# Create your models here.

TICKET_CLASS_CHOICES = (
    ('Первый класс', 'Первый класс'),
    ('Бизнес-класс', 'Бизнес-класс'),
    ('Эконом', 'Эконом')
)


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    name = models.CharField(
        max_length=100, verbose_name='Город', 
        null=True
    )
    en_name = models.CharField(
        max_length=100, verbose_name='Международное название города',
        null=True
    )

    def __str__(self):
        return self.name


class Airport(models.Model):
    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'

    iata_code = models.CharField(
        max_length=3,
        verbose_name='Код аэропорта',
        unique=True
    )
    air_name = models.CharField(
        max_length=100,
        verbose_name='Имя аэропорта'
    )
    city = models.ForeignKey(
        City, verbose_name='Город',
        on_delete=models.CASCADE,
    )

    class Meta:
        managed = False

    def __str__(self):
        return self.air_name


class PlaneType(models.Model):
    class Meta:
        verbose_name = 'Тип самолета'
        verbose_name_plural = 'Типы самолетов'

    name = models.CharField(
        max_length=35, verbose_name="Название типа самолета"
    )

    def __str__(self):
        return self.name


class Plane(models.Model):
    class Meta:
        verbose_name = 'Самолет'
        verbose_name_plural = 'Самолеты'

    name = models.CharField(
        max_length=35, verbose_name='Имя самолета', null=True,
    )
    pl_type = models.ForeignKey(
        PlaneType, verbose_name="Тип самолета",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Flight(models.Model):
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    plane = models.ForeignKey(
      Plane, verbose_name='Самолет',
      on_delete=models.SET_NULL,
      null=True
    )
    takeoff_place = models.ForeignKey(
        Airport, verbose_name='Откуда',
        on_delete=models.SET_NULL,
        related_name="place_from",
        null=True
    )
    arrival_place = models.ForeignKey(
        Airport, verbose_name='Куда',
        on_delete=models.SET_NULL,
        related_name="place_to",
        null=True
    )
    takeoff_time = models.DateTimeField(
        null=True, verbose_name='Время отправления',
    )
    arrival_time = models.DateTimeField(
        null=True, verbose_name='Время прибытия',
    )
    seats_number = models.IntegerField(
        default=0, verbose_name='Количество билетов',
    )

    def __str__(self):
        return 'Маршрут: {} ({}) - {} ({}) || {} - {}'.format(
            self.takeoff_place.city.name, 
            self.takeoff_place.iata_code, 
            self.arrival_place.city.name,
            self.arrival_place.iata_code,
            self.takeoff_time.strftime('%d.%m.%Y %H:%M'),
            self.arrival_time.strftime('%d.%m.%Y %H:%M'),
        )
        

class Ticket(models.Model):
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    flight = models.ForeignKey(
        Flight, verbose_name="Номер рейса",
        on_delete=models.CASCADE,
    )
    is_bought = models.BooleanField(
        verbose_name='Куплен ли билет',
    )
    tickets_num = models.IntegerField(
        verbose_name='Количество билетов',
        default=0,
    )
    t_class = models.CharField(
        max_length=35, verbose_name='Класс билета',
        default=TICKET_CLASS_CHOICES[0][1], choices=TICKET_CLASS_CHOICES
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{}: {} || Рейс: ({} ({}) - {} ({}))'.format(
            self.t_class,
            how_price_is_it(self.price),
            self.flight.takeoff_place.city.name, 
            self.flight.takeoff_place.iata_code, 
            self.flight.arrival_place.city.name,
            self.flight.arrival_place.iata_code
        )


class Position(models.Model):
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.CharField(
        max_length=55, null=True,
        verbose_name='Название должности'
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    last_name = models.CharField(max_length=50, null=False, default='Петров', verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, null=False, default='Григорий', verbose_name="Имя")
    patro = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    position = models.ForeignKey(Position, null=True, verbose_name="Должность", on_delete=models.SET_NULL)
    xp = models.IntegerField(default=0, null=False, verbose_name="Стаж")

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
        if self.patro == None:
            self.patro = ' '

    def __str__(self):
        return '{} {} {} - {} (Стаж: {} {})'.format(self.last_name, self.first_name, self.patro, self.position, self.xp, xp_years(self.xp))


class AirlineTeam(models.Model):
    class Meta:
        verbose_name = 'Экипаж'
        verbose_name_plural = 'Экипажи'

    flight = models.ForeignKey(
        Flight, verbose_name="Назначенный вылет",
        on_delete=models.CASCADE,
    )
    worker = models.ForeignKey(
        Employee, verbose_name="Рабочий",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.worker.patro == None:
            self.worker.patro = ' '
        return '{}: {} {} {} ({} ({}) - {} ({}))'.format(
            self.worker.position,
            self.worker.last_name,
            self.worker.first_name,
            self.worker.patro,
            self.flight.takeoff_place.city.name, 
            self.flight.takeoff_place.iata_code, 
            self.flight.arrival_place.city.name,
            self.flight.arrival_place.iata_code
        )