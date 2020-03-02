from math import radians

from rest_framework import status
from rest_framework.views import APIView

from django.conf import settings
from django.http import JsonResponse
from django.db.models import F, Q, Value, FloatField
from django.db.models.functions import Sin, ASin, Cos, Sqrt
from django.contrib.postgres.search import SearchVector, SearchQuery

from find_bnb.models import BnBListing
from find_bnb.serializers import SearchResultsSerializer, SearchQuerySerializer


EARTH_RADIUS_M = 6371000


# Create your views here.
class SearchListingsView(APIView):

    def post(self, request, *args, **kwargs):
        # validate post params
        query_serializer = SearchQuerySerializer(data=request.POST)
        if not query_serializer.is_valid():
            return JsonResponse(data={'error': 'bad request'},
                                status=status.HTTP_400_BAD_REQUEST)

        latitude = query_serializer.validated_data.get('latitude')
        search_lat_rads = radians(latitude) if latitude else None

        longitude = query_serializer.validated_data.get('longitude')
        search_long_rads = radians(longitude) if longitude else None

        distance = query_serializer.validated_data.get('distance')

        query = query_serializer.validated_data.get('query', '').strip()

        qset = BnBListing.objects.all()

        if all([latitude, longitude, distance]):
            # Haversine formula
            # Reference: # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
            dlon = F('longitude_radians') - search_long_rads
            dlat = F('latitude_radians') - search_lat_rads
            a = Sin(dlat / 2) ** 2 + Cos(search_lat_rads) * Cos(F('latitude_radians')) * Sin(dlon / 2) ** 2
            c = 2 * ASin(Sqrt(a))
            distance_func = c * EARTH_RADIUS_M

            # efficiency improvement: use a square first to limit the amount of data to annotate
            qset = qset.annotate(distance=distance_func)
            qset = qset.filter(distance__lte=distance)
        else:
            qset = qset.annotate(distance=Value(None, FloatField()))

        if query:
            if settings.USING_POSTGRES:
                # use text search in Postgres
                qset = qset.annotate(search=SearchVector('name',
                                                         'neighborhood_group',
                                                         'neighborhood',
                                                         'room_type'))
                qset = qset.filter(search=SearchQuery(query))
            else:
                # use regular __icontains: very basic search in SQLite
                qset = qset.filter(Q(name__icontains=query) |
                                   Q(neighborhood_group__icontains=query) |
                                   Q(neighborhood__icontains=query) |
                                   Q(room_type__icontains=query))

        serializer = SearchResultsSerializer(qset.order_by('distance', 'price'),
                                             many=True)

        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK,
                            safe=False)
