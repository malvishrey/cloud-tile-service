import rasterio
import numpy as np
import os
import subprocess
import shutil
def generate_tiles(basemap_path,out_path_new):

    out_dir = 'processed_planet_maps'
    os.makedirs(out_dir, exist_ok=True)
    for files in os.listdir(basemap_path):
        if files[-3:] =='tif':
            item_path = os.path.join(basemap_path, files)
            out_path = os.path.join(out_dir, files)
            in_name = item_path
            # print(in_name)
            out_name = 'temp.tif'
            out_name1 = 'temp1.tif'
            subprocess.run(f"gdal_translate {in_name} {out_name} -b 3 -b 2 -b 1 -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB", shell=True, capture_output=False, text=True)
            img = rasterio.open(out_name)
            temp = img.read(1)
            minval = np.min(temp[temp!=0])
            maxval = np.max(temp[temp!=0])
            subprocess.run(f"gdal_translate {out_name} {out_name1} -scale {minval} {maxval} 0 65535 -exponent 0.5 -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB", shell=True, capture_output=False, text=True)
            subprocess.run(f"gdal_translate -ot Byte -scale 0 65535 0 255 {out_name1} {out_path}", shell=True, capture_output=False, text=True)


    output_vrt = "planet_merged.vrt"  # Output VRT file name
    tif_files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith('.tif')]

    if not tif_files:
        print("No TIFF files found in the specified folder.")
    else:
        command = ["gdalbuildvrt", output_vrt] + tif_files
        try:
            subprocess.run(command, check=True)
            print(f"VRT file created successfully: {output_vrt}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while creating VRT file: {e}")

    command = [
        "gdal2tiles",               # The command to run
        "-z", "8-15",              # Options
        "--processes=6",
        output_vrt,                  # Input file
        out_path_new                 # Output directory
    ]

    subprocess.run(command, check=True, text=True, shell=True)

    os.remove('temp.tif')
    os.remove('temp1.tif')
    os.remove('planet_merged.tif')
    shutil.rmtree(out_dir)

        