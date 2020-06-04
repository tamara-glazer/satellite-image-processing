######################################
#    Parallelized Data Processing    #
######################################

'''
Background: The data consist of seven .tif files, two from Guatemala, two from
Colombia, and three from St. Lucia. Each .tif file, ranging from 1.65 to 9.96
GB in size, contains a 4cm resolution satellite image of an area spanning
several miles. Originally, all data access, pre-processing, and feature
creation was conducted serially and took 12+ hours to complete. This script
attempts to perform the following operations in parallel to reduce the speed
of data processing: load geojson, extract relevant data for each individual
building from geojson, perform an affine transformation each each set of
coordinates, extract pixel matrix for each segemented building from tif file,
perform necessary image transformations, and compute metrics to be used as
features for unsupervised machine learning.
'''

import numpy as np
import pandas as pd
import pywren
import argparse
import file_names as f
import json
import boto3


BUCKET = 'mapping-disaster-risk'

TIFS = ['borde_rural_ortho-cog.tif', 'borde_soacha_ortho-cog.tif',
        'castries_ortho-cog.tif', 'dennery_ortho-cog.tif',
        'gros_islet_ortho-cog.tif', 'mixco_1_and_ebenezer_ortho-cog.tif',
        'mixco_3_ortho-cog.tif']
GEOJSONS = ['train-borde_rural.geojson', 'train-borde_soacha.geojson',
            'train-castries.geojson', 'train-dennery.geojson',
            'train-gros_islet.geojson', 'train-mixco_1_and_ebenezer.geojson',
            'train-mixco_3.geojson']

# Note that all geojsonn names are the object names as well, so to access 
# call: https://mapping-disaster-risk.s3.amazonaws.com/train-borde_rural.geojson

pwex = pywren.default_executor()


# Get all JSONS
def get_geojsons(geojsons=GEOJSONS):
    '''
    Load geojson, extract relevant information, return as a dictionary.
    '''
    s3 = boto3.client('s3')
    results = []
    for item in geojsons:
        obj = s3.get_object(Bucket=BUCKET, Key=item)
        geo_json = json.load(obj.get()['Body'])
        results.append(geo_json)

    return results


def get_geojsons_paralell():
    '''
    '''
    futures = pwex.map(get_geojsons, GEOJSONS)
    geojsons = pywren.get_all_results(futures)

    return geojsons


### FUNCTION TO BE PARALLELIZED: Create new, relevant jsons
def make_polygons(geo_json):
    '''
    Extract the necessary features from the geojsons.
    '''
    polygons = []

    for feature in geojson['features']:
        polygon = {}
        polygon['type'] = feature['geometry']['type']
        polygon['bid'] = feature['id']
        polygon['roof_material'] = feature['properties']['roof_material']
        polygon['coordinates'] = feature['geometry']['coordinates']
        polygons.append(polygon)

    return polygons


### PARALLELIZE ABOVE FUNCTION: Create new, relevant jsons ---> Can't get this to work
def make_polygons_parallel():
    '''
    Parallelized obtaining of geojsons.
    '''
    results = get_geojsons()
    futures = pwex.map(make_polygons, results)
    got_futures = pywren.get_all_results(futures)

    return got_futures


### PARALLEL: For each polygon, transform coordinates
def transform_coordinates(polygon):

    pass

### SERIAL/PARALLEL?: Access the TIF files
def get_tif():

    pass

### PARALLEL: Obtain each individual rooftop array
def get_rooftop_array_after_mask():

    pass

### PARALLEL: Convert to graysacle
def convert_grayscale():

    pass


### PARALLEL: Crop center
def crop_center():

    pass


### PARALLEL: Calculate zonal statistics
def calculate_zonal_stats():

    pass


### Bring everything together, time the process, and return the final dataframe of zonal stats
def build_df():

    pass


if __name__ == '__main__':
    pass
