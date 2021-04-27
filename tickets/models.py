from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

TICKET_CLASS_CHOICES = (
    ('A', 'Первый класс'),
    ('C', 'Бизнес-класс'),
    ('X', 'Эконом')
)


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(
        max_length=100, verbose_name='Город', 
        null=True
    )
    en_name = models.CharField(
        max_length=100, verbose_name='Международное название города',
        null=True
    )


class Airport(models.Model):
    id = models.IntegerField(
        unique=True,
        primary_key=True,
    )
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
    name = models.CharField(
        max_length=35, verbose_name="Название типа"
    )


class Plane(models.Model):
    name = models.CharField(
        max_length=35, verbose_name='Имя самолета', null=True,
    )
    pl_type = models.ForeignKey(
        PlaneType, verbose_name="Тип самолета",
        on_delete=models.CASCADE
    )


class Flight(models.Model):
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
        null=False, blank=True, verbose_name='Время отправления',
        auto_now_add=True
    )
    arrival_time = models.DateTimeField(
        null=False, blank=True, verbose_name='Время прибытия',
        auto_now_add=True
    )
    seats_number = models.IntegerField(
        default=0,
    )


class Ticket(models.Model):
    flight = models.ForeignKey(
        Flight, verbose_name="Номер рейса",
        on_delete=models.CASCADE,
    )
    is_bought = models.BooleanField()
    t_class = models.CharField(
        max_length=35, verbose_name='Класс билета',
        default=TICKET_CLASS_CHOICES[0][0], choices=TICKET_CLASS_CHOICES
    )
    price = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


class Position(models.Model):
    name = models.CharField(
        max_length=55, null=True
    )


class Employee(models.Model):
    last_name = models.CharField(max_length=50, null=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, null=True, verbose_name="Имя")
    patro = models.CharField(max_length=50, null=True, verbose_name="Отчество")
    position = models.ForeignKey(Position, null=True, verbose_name="Должность", on_delete=models.SET_NULL)
    xp = models.IntegerField(default=0, verbose_name="Стаж")


class AirlineTeam(models.Model):
    flight = models.ForeignKey(
        Flight, verbose_name="Назначенный вылет",
        on_delete=models.CASCADE,
    )
    worker = models.ForeignKey(
        Employee, verbose_name="Рабочий",
        on_delete=models.CASCADE,
    )