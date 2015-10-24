import subprocess
from itertools import permutations
import sys
import gdal

def generate_rgb_images(image_path, band_1, band_2, band_3):
    '''
    This method will create a jpg representation of the given multiband tif
    using the specified bands.
    '''
    command = 'gdal_translate -b %s -b %s -b %s %s rgb-%s%s%s.tif' % (band_3, band_2, band_1, image_path, band_3, band_2, band_1)
    print command
    subprocess.call(command, shell=True)

    name = '%d%d%d' % (band_3, band_2, band_1)


    create_copy('rgb-%s.tif' % name, 'rgb-%s.jpg' % name)


    print name



    remove = 'rm rgb-%s.tif' % name

    subprocess.call(remove, shell=True)

def create_copy(image_path, name):
    dataset = gdal.Open(image_path)      
    
    saveOptions = []
    saveOptions.append("QUALITY=75")
    
    # Obtains a JPEG GDAL driver
    jpegDriver = gdal.GetDriverByName("JPEG")   
    
    # Create the .JPG file
    jpegDriver.CreateCopy(name, dataset, 0, saveOptions) 


if __name__ == '__main__':

    for c in permutations([1, 2, 3, 4, 5], 3):
    		print c
    		generate_rgb_images(sys.argv[1], c[0],c[1],c[2])


