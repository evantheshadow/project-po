from django.db import models

# Create your models here.

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
        on_delete=models.PROTECT,
    )

    class Meta:
        managed = False
        # db_table = 'airports_table'

    def __str__(self):
        return air_name