import sys
from io import BytesIO
from json import dumps
from unittest import TestCase, main
from unittest.mock import Mock
from botocore.stub import Stubber
from botocore.session import get_session
from botocore.response import StreamingBody

# prepare mocks for boto3
stubbed_client = get_session().create_client('s3')
stubber = Stubber(stubbed_client)

# mock response from S3
body_encoded = dumps({'name': 'Hello World'}).encode()
stubber.add_response('get_object', {'Body': StreamingBody(BytesIO(body_encoded), len(body_encoded))})

stubber.activate()

# add mocks to the real module
sys.modules['boto3'] = Mock()
sys.modules['boto3'].resource = Mock(return_value=stubbed_client)

# import the module that will be tested
# boto3 should be mocked in the app.py
from functions.closeststops import get_distance_in_meters


class TestClosestStops(TestCase):

    def test_should_return_correct_distance(self):
        # given
        papiesz_lat = 41.90218803264449
        papiesz_lon = 12.454085406992665
        target_lat = 41.92136787215122
        target_lon = 12.45566640018914

        # when
        distance = get_distance_in_meters(papiesz_lat, papiesz_lon, target_lat, target_lon)

        # then
        self.assertEqual(2137, distance, msg='Correct distance between two coordinates')

    def test_when_received_identical_coords_then_distance_should_be_zero(self):
        # given
        papiesz_lat = 41.90218803264449
        papiesz_lon = 12.454085406992665
        # when
        distance = get_distance_in_meters(papiesz_lat, papiesz_lon, papiesz_lat, papiesz_lon)

        # then
        self.assertEqual(0, distance, msg='Correct distance between two coordinates')


if __name__ == '__main__':
    main()
