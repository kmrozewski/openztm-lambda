import sys
import os
import json
from unittest import TestCase, main
from unittest.mock import Mock
from botocore.stub import Stubber
from botocore.session import get_session

# prepare mocks for boto3
stubbed_client = get_session().create_client('s3')
stubber = Stubber(stubbed_client)
stubber.activate()

# add mocks to the real module
sys.modules['boto3'] = Mock()
sys.modules['boto3'].resource = Mock(return_value=stubbed_client)

# import the module that will be tested
# boto3 should be mocked in the app.py
from functions.s3upload import parse_stops


class TestS3Upload(TestCase):
    @classmethod
    def setUpClass(cls):
        stops_path = './response.json' if 'test' in os.getcwd() else './tests/response.json'
        with open(stops_path, 'r') as file:
            response = json.load(file)
            cls.stops = parse_stops(response)

    def test_should_get_first_row(self):
        # expect
        self.assertEqual(5, len(self.stops), msg='Correct number of stops')

    def test_required_fields_should_be_present(self):
        stop = self.stops[0]
        
        # expect
        self.assertEqual(8227, stop['stopId'])
        self.assertEqual('04', stop['stopCode'])
        self.assertEqual('Dąbrowa Centrum', stop['stopName'])
        self.assertEqual('8227', stop['stopShortName'])
        self.assertEqual('Gdynia Dąbrowa Centrum', stop['stopDesc'])
        self.assertEqual('Gdynia', stop['zoneName'])
        self.assertEqual(0, stop['virtual'])
        self.assertEqual(0, stop['nonpassenger'])
        self.assertEqual(0, stop['onDemand'])
        self.assertEqual(54.47317, stop['stopLat'])
        self.assertEqual(18.46509, stop['stopLon'])

    def test_not_required_fields_should_be_removed(self):
        stop = self.stops[0]
        
        # expect
        self.assertFalse('subName' in stop)
        self.assertFalse('date' in stop)
        self.assertFalse('zoneId' in stop)
        self.assertFalse('stopUrl' in stop)
        self.assertFalse('locationType' in stop)
        self.assertFalse('parentStation' in stop)
        self.assertFalse('stopTimezone' in stop)
        self.assertFalse('wheelchairBoarding' in stop)
        self.assertFalse('depot' in stop)
        self.assertFalse('activationDate' in stop)
        self.assertFalse('ticketZoneBorder' in stop)


if __name__ == '__main__':
    main()
