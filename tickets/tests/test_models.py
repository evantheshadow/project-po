from django.test import TestCase
from django.template.defaultfilters import slugify
from tickets.models import *


class ModelsTestCase(TestCase):
    def setUp(self):
        self.city1 = City.objects.create(name='Печора')
        self.city2 = City.objects.create(name='Псков')

        self.airport1 = Airport.objects.create(city_id=1, air_name='Аэропорт Печоры', iata_code='PCH')
        self.airport2 = Airport.objects.create(city_id=2, air_name='Аэропорт Пскова', iata_code='PSK')

    def test_if_city_is_pechora(self):
        """
        Test if the given city is Pechora.
        """
        city = City.objects.get(id=1)

        self.assertEqual(city.name, 'Печора')
        print('test_models.py >>: Тест определения города Печора прошло успешно!')

    def test_if_city_is_pskov(self):
        """
        Test if the given city is Pskov.
        """
        city = City.objects.get(id=2)

        self.assertEqual(city.name, 'Псков')
        print('test_models.py >>: Тест определения города Псков прошло успешно!')

    def test_if_airport_1(self):
        airport = Airport.objects.get(id=1)
        self.assertEqual(airport.air_name, 'Аэропорт Печоры')

    def test_if_airport_2(self):
        airport = Airport.objects.get(id=2)
        self.assertEqual(airport.air_name, 'Аэропорт Пскова')
    
    

