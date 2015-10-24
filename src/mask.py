import numpy
import osr
import sys
import gdal

def use_mask(original_image, mask):
    original_dataset = gdal.Open(original_image)
    mask_dataset = gdal.Open(mask)
    bands = original_dataset.RasterCount
    geo_transform = original_dataset.GetGeoTransform()
    projection = osr.SpatialReference()
    projection.ImportFromWkt(original_dataset.GetProjectionRef())
    width = original_dataset.RasterXSize
    height = original_dataset.RasterYSize

    print width,height

    print bands
    output_file = "final_final_final_test.tif"
    driver = gdal.GetDriverByName('GTiff')
    result_image = driver.Create(output_file, width, height, bands, gdal.GDT_Int16  )
    result_image.SetGeoTransform(geo_transform)
    result_image.SetProjection(projection.ExportToWkt())


    original_array_red = numpy.ravel(numpy.array(original_dataset.GetRasterBand(1).ReadAsArray()))
    original_array_green = numpy.ravel(numpy.array(original_dataset.GetRasterBand(2).ReadAsArray()))
    original_array_blue = numpy.ravel(numpy.array(original_dataset.GetRasterBand(3).ReadAsArray()))

    mask_array_red = numpy.ravel(numpy.array(mask_dataset.GetRasterBand(1).ReadAsArray()))
    mask_array_green = numpy.ravel(numpy.array(mask_dataset.GetRasterBand(2).ReadAsArray()))
    mask_array_blue = numpy.ravel(numpy.array(mask_dataset.GetRasterBand(3).ReadAsArray()))

    size = len(original_array_red)
    print size
    final_array_red = numpy.ravel(numpy.array(original_dataset.GetRasterBand(1).ReadAsArray()))
    final_array_green = numpy.ravel(numpy.array(original_dataset.GetRasterBand(2).ReadAsArray()))  
    final_array_blue = numpy.ravel(numpy.array(original_dataset.GetRasterBand(3).ReadAsArray()))



    for i in range(size):
        if(i%100000 == 0):
            print i*1.0 / size

        if (mask_array_red[i] + mask_array_green[i] + mask_array_blue[i]) < 1:
            final_array_red[i] = 0.2126 * original_array_red[i] + 0.7152 * original_array_green[i] + 0.0722 * original_array_blue[i]
            final_array_green[i] = 0.2126 * original_array_red[i] + 0.7152 * original_array_green[i] + 0.0722 * original_array_blue[i]
            final_array_blue[i] = 0.2126 * original_array_red[i] + 0.7152 * original_array_green[i] + 0.0722 * original_array_blue[i]

    result_image.GetRasterBand(1).WriteArray(final_array_red.reshape((width, height)))
    result_image.GetRasterBand(2).WriteArray(final_array_green.reshape((width, height)))
    result_image.GetRasterBand(3).WriteArray(final_array_blue.reshape((width, height)))
    result_image.FlushCache()
if __name__ == '__main__':
    use_mask('/Users/agutierrez/Documents/python/histogram-matching/all/final/rgb-proj2.tif','/Users/agutierrez/Documents/python/histogram-matching/all/final/final2.tif')
