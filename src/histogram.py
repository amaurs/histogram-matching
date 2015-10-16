import numpy
import sys
import matplotlib.pyplot as plt

def main(image_path, reference_image_path): 
    get_histogram(image_path, reference_image_path)

def get_histogram(image_path, reference_image_path):    
    import gdal
    final = numpy.zeros((5,5000,5000))
    for band in range(1,2):
        print 'Processing band %s.' % band
        interest_band = band
        print 'About to open file %s.' % image_path
        ds = gdal.Open(image_path)
        print 'Reading data as array from file.'
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
        final[interest_band - 1] = result.reshape((5000, 5000))
    show_histograms(cdf, reference_cdf)
    
def show_histograms(original_cumulative_distribution_function, reference_cumulative_distribution_function):
    plt.plot(original_cumulative_distribution_function, color='g')
    plt.plot(reference_cumulative_distribution_function, color='r')
    plt.title("Histogram Matching")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == '__main__':
    print sys.argv
    main(sys.argv[1], sys.argv[2])
