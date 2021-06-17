from django.test import TestCase, Client, RequestFactory
from datetime import datetime
from tickets.models import City, Airport, Flight
from tickets.forms import CityManagerForm
from tickets.views import SearchListView

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.city_url = ('/')
        self.flight_url = ('/flights')
        self.city1 = City.objects.create(
            id=1,
            name='Печора',
            en_name='Pechora'
        )
        self.city2 = City.objects.create(
            id=2,
            name='Псков',
            en_name='Pskov'
        )
        self.airport1 = Airport.objects.create(
            id=1,
            iata_code='PCH',
            air_name='Печора',
            city_id=1,
        )
        self.airport2 = Airport.objects.create(
            id=2,
            iata_code='PSV',
            air_name='Псков',
            city_id=1,
        )
        self.flight = Flight.objects.create(
            plane=None,
            takeoff_place_id=1,
            arrival_place_id=2,
            takeoff_time=datetime.now(),
            arrival_time=datetime.now(),
            seats_number=50,
        )   

    def test_city_list_view_get(self):
        response = self.client.get(self.city_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homePage.html')
        print('Запрос GET для CityListView прошел успешно!')
    
    def test_city_list_view_search(self):
        response = self.client.post(self.city_url)

        self.assertEquals(response.status_code, 200)
        print('Запрос POST для CityListView прошел успешно!')

    def test_get_queryset(self):
        request = RequestFactory().get(self.flight_url)
        view = SearchListView()
        view.request = request

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Flight.objects.all())

