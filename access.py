import boto3
BUCKET = 'mapping-disaster-risk'
KEY = 'train-mixco_3.geojson'

s3client = boto3.client('s3', region_name = 'us-east-1')
objects = s3client.list_objects(Bucket=BUCKET)
obj = s3client.get_object(Bucket=BUCKET, Key=KEY)