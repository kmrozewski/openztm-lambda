import json
import boto3
import math

EARTH_MEAN_RADIUS_METRES = 6371e3
allowed_origins = [
    'https://ztmgdansk.com',
    'https://test.ztmgdansk.com',
    'http://localhost:3000'
]


def get_stops():
    s3 = boto3.resource('s3')
    response = s3.get_object(Bucket='open-ztm-files', Key='stops.json')
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)


stops = get_stops()


def handler(event, context):
    if 'origin' in event['headers']:
        print(f"Origin {event['headers']['origin']}")
        print(f"Allowed {get_allowed_origin(event['headers'])}")

    params = event["queryStringParameters"]
    latitude = float(params['latitude'])
    longitude = float(params['longitude'])
    radius = int(params['radius']) if 'radius' in event else 500

    closest = get_closest_stops(latitude, longitude, radius)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
            'Access-Control-Allow-Origin': get_allowed_origin(event['headers']),
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(closest)
    }


def get_closest_stops(latitude, longitude, radius):
    closest = []
    for stop in stops:
        distance = get_distance_in_meters(latitude, longitude, stop['stopLat'], stop['stopLon'])
        if distance <= radius:
            closest.append({'distance': distance, 'stop': stop})

    return closest


def deg_to_rad(deg):
    return deg * math.pi / 180.0


def distance_formula(c):
    return c * EARTH_MEAN_RADIUS_METRES


def sub_formula_c(a):
    return 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def sub_formula_a(phi1, phi2, delta_phi, delta_lambda):
    return (math.sin(delta_phi / 2)
        * math.sin(delta_phi / 2)
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2)
        * math.sin(delta_lambda / 2))


def get_params(latitude1, longitude1, latitude2, longitude2):
    return [
        deg_to_rad(latitude1),
        deg_to_rad(latitude2),
        deg_to_rad(latitude2 - latitude1),
        deg_to_rad(longitude2 - longitude1)
    ]


def get_distance_in_meters(latitude1, longitude1, latitude2, longitude2):
    params = get_params(latitude1, longitude1, latitude2, longitude2)
    return round(distance_formula(sub_formula_c(sub_formula_a(params[0], params[1], params[2], params[3]))))


def get_allowed_origin(headers):
    if 'origin' in headers:
        origin = headers['origin']
        return origin if origin in allowed_origins else allowed_origins[0]

    return allowed_origins[0]