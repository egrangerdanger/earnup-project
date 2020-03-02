from rest_framework import serializers

from .models import BnBListing


class BnBListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BnBListing
        exclude = ['longitude_radians', 'latitude_radians']


class SearchQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90, required=False)
    longitude = serializers.FloatField(min_value=-180, max_value=180, required=False)
    distance = serializers.FloatField(min_value=0, required=False)
    query = serializers.CharField(min_length=1, required=False)


class SearchResultsSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(allow_null=True)

    class Meta:
        model = BnBListing
        fields = ['name',
                  'host_name',
                  'neighborhood_group',
                  'neighborhood',
                  'latitude',
                  'longitude',
                  'distance',
                  'price',
                  'minimum_nights',
                  'room_type']
