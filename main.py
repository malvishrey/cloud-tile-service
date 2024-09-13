from google.cloud import storage
import pandas as pd
from datetime import datetime
import logging
import json
import os
from planet_basemaps import find_base_maps, download_and_extract_base_maps
from tile_generation import generate_tiles
import geopandas as gpd
import subprocess
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#env tile-service-gcp
def generate_tile_service(date, confidence, geojson, asu_snow):

    client = storage.Client()
    bucket_name = 'shrey-snowviz-platform'
    bucket = client.get_bucket(bucket_name)
    blob_date = bucket.blob('data/ps_daily.txt')
    ps_dates = blob_date.download_as_text()
    logger.info(f"reached_here after bucket {ps_dates}")
    current_date = datetime.today().strftime('%Y-%m-%d')
    print(current_date)
    if (current_date in ps_dates):
        logger.info(f"The date {current_date} exists already.")
        return 'Skipped - date already exists'
    
    if geojson == "":
        geojson = 'data/svr_quad_13.geojson'

    blob = bucket.blob(geojson)
    temp = blob.download_as_text()
    temp_geojson_path = 'temp.geojson'
    with open(temp_geojson_path, 'w', encoding='utf-8') as file:
        file.write(temp)
    gdf = gpd.read_file('temp.geojson')
    
    order_ids = find_base_maps(current_date,confidence="75",temp_path=temp_geojson_path)
    logger.info(f"order list {order_ids}")
    if(len(order_ids)<len(gdf)//2):
        logger.info(f"Skipping due to less coverage.")
        return 'Skipped - less coverage'
    
    download_path = 'raw_planet_maps/'
    result = subprocess.run("pip install planet -U", check=True, text=True, shell=True)
    download_and_extract_base_maps(order_ids,download_path)
    result = subprocess.run("pip install planet==1.5.2", check=True, text=True, shell=True)

    out_path = "".join(current_date.split('-'))
    print('out_path',out_path)
    generate_tiles(download_path,out_path)
    if(os.path.exists(out_path)):
        command = [
            "gsutil",
            "-m", "cp",
            "-r",
            out_path,
            f"gs://{bucket_name}/data/planet_daily"
        ]
        result = subprocess.run(command, check=True, text=True)
        updated_content = ps_dates + f"\n{current_date}"
        blob_date.upload_from_string(updated_content)
    else:
        return 'Skipped - problem with tile generation'

    os.remove(temp_geojson_path)
    shutil.rmtree(download_path)
    shutil.rmtree(out_path)

    return 'Tiles generated successfully'
if __name__ == "__main__":
    generate_tile_service("", "", "", "")

