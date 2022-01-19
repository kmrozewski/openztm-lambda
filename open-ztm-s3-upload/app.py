import requests
import json
import pickle
import boto3

path = 'https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json'
s3 = boto3.resource('s3')

def handler(event, context):
    response = requests.get(path).json()
    first = list(response.keys())[0]
    stops = response[first]['stops']
    
    save_to_s3(stops)
    # TODO implement
    return {
        'statusCode': 200,
        'body': stops[0]
    }

def save_to_s3(json_data):
    print("Saving to s3")
    s3object = s3.Object('open-ztm-files', 'stops.json')
    s3object.put(Body=(bytes(json.dumps(json_data).encode('UTF-8'))))