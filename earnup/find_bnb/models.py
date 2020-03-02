from django.db import models


class BnBListing(models.Model):
    import_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    host_id = models.PositiveIntegerField(blank=True, null=True)
    host_name = models.TextField(blank=True, null=True)
    neighborhood_group = models.TextField(blank=True, null=True)
    neighborhood = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    latitude_radians = models.FloatField()
    longitude = models.FloatField()
    longitude_radians = models.FloatField()
    room_type = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)  # money, so should have decimals allowed
    minimum_nights = models.PositiveIntegerField(blank=True, null=True)
    number_of_reviews = models.PositiveIntegerField(blank=True, null=True)
    last_review = models.DateField(blank=True, null=True)
    reviews_per_month = models.FloatField(blank=True, null=True)
    calculated_host_listings_count = models.PositiveIntegerField(blank=True, null=True)
    availability_365 = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude_radians', 'longitude_radians']),
            models.Index(fields=['name', 'neighborhood', 'neighborhood_group', 'room_type']),
        ]
