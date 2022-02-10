import requests
import json
import boto3


path = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json'
s3 = boto3.resource('s3')


def handler(event, context):
    response = requests.get(path).json()
    stops = parse_stops(response)

    print(f'Saving to S3 {len(stops)} stops')
    save_to_s3(stops)

    return {
        'statusCode': 200,
        'body': stops
    }


def save_to_s3(json_data):
    print("Saving to s3")
    s3object = s3.Object('open-ztm-files', 'stops.json')
    s3object.put(Body=(bytes(json.dumps(json_data).encode('UTF-8'))))


def parse_stops(response):
    return [get_stop(stop) for stop in get_current_stops(response)]


def get_current_stops(response):
    keys = list(response.keys())
    today = keys[0]
    print(f'Getting stops from {today}')

    return response[today]['stops']


def get_stop(stop):
    stop_copy = dict(stop)
    pop_key(stop_copy, 'subName')
    pop_key(stop_copy, 'date')
    pop_key(stop_copy, 'zoneId')
    pop_key(stop_copy, 'stopUrl')
    pop_key(stop_copy, 'locationType')
    pop_key(stop_copy, 'parentStation')
    pop_key(stop_copy, 'stopTimezone')
    pop_key(stop_copy, 'wheelchairBoarding')
    pop_key(stop_copy, 'depot')
    pop_key(stop_copy, 'ticketZoneBorder')
    pop_key(stop_copy, 'activationDate')

    return stop_copy


def pop_key(stop, key):
    try:
        del stop[key]
    except KeyError:
        print(f'No such key: {key}')
