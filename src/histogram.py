import numpy
import osr
import sys
import gdal
import matplotlib.pyplot as plt

def main(image_path, reference_image_path, output_name): 
    get_histogram(image_path, reference_image_path, output_name)

def get_histogram(image_path, reference_image_path, output_name):    

    f, plots = plt.subplots(5, sharex=True, sharey=True)

    print 'About to open file %s.' % image_path
    ds = gdal.Open(image_path)

    bands = ds.RasterCount

    print "Bands: %d" % bands

    geo_transform = ds.GetGeoTransform()

    projection = osr.SpatialReference()
    projection.ImportFromWkt(ds.GetProjectionRef())

    output_file = output_name
    width = 5000
    height = 5000


    driver = gdal.GetDriverByName('GTiff')
    result_image = driver.Create(output_file, width, height, 5, gdal.GDT_Int16  )
    result_image.SetGeoTransform(geo_transform)
    result_image.SetProjection(projection.ExportToWkt())



    for band in range(1,6):
        print 'Processing band %s.' % band
        interest_band = band
        print 'Reading band as array from file.'
        array = numpy.array(ds.GetRasterBand(interest_band).ReadAsArray()) 
        ref_ds = gdal.Open(reference_image_path)
        reference_array = numpy.array(ref_ds.GetRasterBand(interest_band).ReadAsArray())
        flat = numpy.ravel(array)
        reference_flattened = numpy.ravel(reference_array)        
        gray_levels = 256*256
        hist, bin_edges = numpy.histogram(flat, bins=gray_levels)
        reference_histogram, reference_bin_edges = numpy.histogram(reference_flattened, bins=gray_levels)
        cdf = numpy.cumsum(hist)
        reference_cdf = numpy.cumsum(reference_histogram)
        result = numpy.zeros(len(flat))
        for i in range(len(flat)):
            index = numpy.searchsorted(reference_cdf,[cdf[flat[i]]])
            result[i] = index[0]

        result_image.GetRasterBand(interest_band).WriteArray(result.reshape((width, height)))
        result_image.FlushCache()

        current_plot = plots[band - 1]
        current_plot.plot(cdf, color='g')
        current_plot.plot(reference_cdf, color='r')
        #show_histograms(cdf, reference_cdf, 'band%d' % band)
    plt.savefig('bands.png')

def create_tiff(output_file, width, height, geo_transform, projection):


    result.GetRasterBand(1).WriteArray( Array )
        

    
def show_histograms(original_cumulative_distribution_function, reference_cumulative_distribution_function, title):
    plt.plot(original_cumulative_distribution_function, color='g')
    plt.plot(reference_cumulative_distribution_function, color='r')
    plt.title("Histogram Matching")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig(title + '.png')

if __name__ == '__main__':
    print sys.argv
    main(sys.argv[1], sys.argv[2], sys.argv[3])
