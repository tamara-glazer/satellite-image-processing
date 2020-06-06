######################################
#  Upload Image Files to s3 Buckets  #
######################################

import numpy as np
import pandas as pd
import pywren
import boto3
import os
import sys
import threading
from multiprocessing.pool import ThreadPool
from boto3.s3.transfer import TransferConfig


AWS_KEY = ""
AWS_SECRET = ""
AWS_TOKEN = ""

TIFS = ['borde_rural_ortho-cog.tif', 'borde_soacha_ortho-cog.tif',
        'castries_ortho-cog.tif', 'dennery_ortho-cog.tif',
        'gros_islet_ortho-cog.tif', 'mixco_1_and_ebenezer_ortho-cog.tif',
        'mixco_3_ortho-cog.tif']
GEOJSONS = ['train-borde_rural.geojson', 'train-borde_soacha.geojson',
            'train-castries.geojson', 'train-dennery.geojson',
            'train-gros_islet.geojson', 'train-mixco_1_and_ebenezer.geojson',
            'train-mixco_3.geojson']

BUCKET = 'mapping-disaster-risk'


def create_client(aws_key_id, aws_secret, aws_token):
    '''
    Create S3 client.
    '''
    s3 = boto3.client('s3',
                      region_name='us-east-1',
                      aws_access_key_id=aws_key_id,
                      aws_secret_access_key=aws_secret,
                      aws_session_token=aws_token)

    return s3


def create_bucket(client, unique_bucket_name):
    '''
    Create a new s3 bucket in an existing client.
    '''
    client.create_bucket(Bucket=unique_bucket_name)


def upload_file(file_name):
    '''
    Upload a geojson or tif file to a specified S3 bucket.
    Note that the key will be the original filename.
    '''
    s3 = create_client(AWS_KEY, AWS_SECRET, AWS_TOKEN)
    s3.upload_file(Filename=file_name,
                   Bucket=BUCKET,
                   Key=file_name)


def list_bucket_objects(client, bucket, max_keys=1000):
    '''
    List all objects in a bucket.
    '''
    response = client.list_objects(Bucket=bucket,
                                   MaxKeys=max_keys)

    print(response)


def download_file(client, bucket, object_name, new_file_name):
    '''
    Download an object from s3 locally.
    Note: can access through https://{bucket}.s3.amazonaws.com/{key}
    '''
    client.download_file(Filename=new_file_name,
                         Bucket=bucket,
                         Key=object_name)


def upload_geojsons(bucket_name=BUCKET, files=GEOJSONS):
    '''
    Use Python's multi-processing module, which offers remote and local
    concurrency, to load all .geojson files to an s3 bucket using threading.

    Citation: http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/
    '''
    s3 = create_client(AWS_KEY, AWS_SECRET, AWS_TOKEN)
    create_bucket(s3, bucket_name)
    pool = ThreadPool(processes=10)
    pool.map(upload_file, files)


def upload_tifs(files=TIFS):
    '''
    Use TransferConfig to configure a multi-part upload and use threading in
    Python to load large .tif files to an s3 bucket. Multipart transfers occur
    when the file size exceeds the value of the multipart_threshold
    attribute.

    Citation: https://medium.com/@niyazi_erd/aws-s3-multipart-upload-with-python-and-boto3-9d2a0ef9b085
    '''
    for file_name in files:
        s3 = boto3.resource('s3')
        config = TransferConfig(multipart_threshold=1024 * 25,
                                max_concurrency=10,
                                multipart_chunksize=1024 * 25, 
                                use_threads=True)

        s3.meta.client.upload_file(Filename=file_name,
                                   Bucket=BUCKET,
                                   Key=file_name,
                                   Config=config)


def main(tifs=TIFS, geojsons=GEOJSONS):
    '''
    Complete full data uploading process prior to data processing.
    '''
    upload_tifs(tifs)
    upload_geojsons(BUCKET, GEOJSONS)


if __name__ == '__main__':
    main()

