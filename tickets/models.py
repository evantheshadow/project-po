from django.db import models

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
        unique=True
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
        # db_table = 'airports_table'

    def __str__(self):
        return air_name


class Flight(models.Model):
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
    date = models.DateField(
        null=False, blank=True, verbose_name='Дата отправления'
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
    cost = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)