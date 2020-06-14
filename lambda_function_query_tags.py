import boto3
import json
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tag-url')

def lambda_handler(event, context):
    # TODO implement
    if event['httpMethod'] == 'GET':
        tags = []
        for i in event['queryStringParameters']:
            tags.append(event['queryStringParameters'][i])
    
    elif event['httpMethod'] == 'POST':
        tags=[]
        tags=list(json.loads(event['body'])['tags'])
        #se=bo['tags']
       
    scans = table.scan()
    urls = []
    for line in scans['Items']:
        if all(ele in line['tag'] for ele in tags):
            urls.append(line['url'])
          
    return {
        'statusCode': 200,
        'headers' : {
       'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,'
     },
      'body': json.dumps({"Links":urls})
        
    }


