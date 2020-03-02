import json
import pandas

from math import radians

from django.core.management.base import BaseCommand

from find_bnb.models import BnBListing
from find_bnb.serializers import BnBListingSerializer


COLUMNS_TO_FIELDS = [
    'import_id',
    'name',
    'host_id',
    'host_name',
    'neighborhood_group',
    'neighborhood',
    'latitude',
    'longitude',
    'room_type',
    'price',
    'minimum_nights',
    'number_of_reviews',
    'last_review',
    'reviews_per_month',
    'calculated_host_listings_count',
    'availability_365',
]
EXPECTED_COLUMNS = len(COLUMNS_TO_FIELDS)
DEFAULT_BATCH_SIZE = 1000


class Command(BaseCommand):
    help = 'Clean and load data for BnB listings'

    def add_arguments(self, parser):
        parser.add_argument('data_path', type=str,
                            help='path to datafile for loading (csv)')
        parser.add_argument('error_path', type=str,
                            help='output file path for problem records (txt)')
        parser.add_argument('--batch_size', type=int,
                            help=f'batch size for bulk create, default is '
                                 f'{DEFAULT_BATCH_SIZE}')

    def handle(self, data_path, error_path, *args, **options):
        good_records = 0
        bad_records = 0

        batch_size = options.get('batch_size') or DEFAULT_BATCH_SIZE
        data_iter = pandas.read_csv(data_path, error_bad_lines=False,
                                    warn_bad_lines=True, chunksize=batch_size)
        with open(error_path, 'w') as error_file:
            for chunk in data_iter:
                batch = []
                for line_num, row in chunk.where(chunk.notnull(), None).iterrows():
                    ser = BnBListingSerializer(data={k: v for k, v in zip(COLUMNS_TO_FIELDS, row.to_list())})
                    if ser.is_valid():
                        # calculate and cache lat and long in radians, will need this to calc distances later
                        ser.validated_data['longitude_radians'] = radians(ser.validated_data['longitude'])
                        ser.validated_data['latitude_radians'] = radians(ser.validated_data['latitude'])

                        batch.append(BnBListing(**ser.validated_data))
                        good_records += 1
                    else:
                        # output lines with bad formatting for inspection and possible later inclusion
                        error_file.write(f'{json.dumps(row.to_dict())}\n')
                        bad_records += 1

                BnBListing.objects.bulk_create(batch)

        print(f'Good: {good_records}, Bad: {bad_records}')
