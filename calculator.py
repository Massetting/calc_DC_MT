# -*- coding: utf-8 -*-
"""

@author: Andrea Massetti

@mail: andrea.massetti@gmail.com


Structure should be: open reference tiff, determine coordinates of pixel 
centroids for each pixel. 
I can use a dict i.e. coordinates[(xmap, ymap)] = (get_pixel_coordinates(x_map, y_map))
iterate for each pixel
    for each raster
        open>readasarray>store>close
    update result
where to store?
I could store directly in a 2d arr, location [x_map, y_map]
"""
import gdal
import os
import numpy as np

class calculator:
    def __init__(self, location):
        self.location = location
        self.raster_location_list = [os.path.join(self.location, f) for f in os.listdir(self.location) if f.endswith(".tif")]
        self.reference_raster_location = self.raster_location_list[0]
        self.tiff_file, self.geotransform, self.projection, self.band, self.xsize, self.ysize, self.nodata = self.import_tiff(self.reference_raster_location)
        self.__delattr__("tiff_file")
        self.__delattr__("band")
        self.coordinates = self.create_coo_dict(self.reference_raster_location)
        self.result = np.zeros((self.xsize, self.ysize), dtype=np.float64)
        self.counts = np.zeros((self.xsize, self.ysize), dtype=np.int32)
        self.mu = -60
    #    self.counter = 0
        self.total_counts = {}


    
    def do_all(self):
        for map_coordinates, coordinates in self.coordinates.items():
            count = 0
            for raster in self.raster_location_list:
                value = self.get_pixel_value(raster, coordinates[0], coordinates[1])
                self.update_value(self.result, value, map_coordinates[0], map_coordinates[1], self.mu, count)
            self.total_counts[map_coordinates] = count
        for map_coordinates, counts in self.total_counts():
            self.counts[map_coordinates[0],map_coordinates[1]] = counts
        final_result = self.result/self.counts
            
        self.save_result(self.result, "quadratic_sum")
        self.save_result(final_result, "variance")
        self.save_result(self.counts, "number")
    def save_result(self, result, name):
        driver=gdal.GetDriverByName('GTiff')
        out_location = os.path.join(self.location,"output")
        if not os.path.isdir(out_location):
            os.makedirs(out_location)
        out_file = os.path.join(out_location, "{}.tif".format(name))
        counter=1    
        while os.path.exists(out_file):
            out_file = os.path.join(out_location, "{}__{}.tif").format(name, counter)
            counter+=1  
            
        new_tiff=driver.Create(out_file, self.sizex, self.sizey, 1, gdal.GDT_Float64)#datatype to be considered
        new_tiff.SetGeoTransform(self.geotransform)
        new_tiff.SetProjection(self.projection)
        new_tiff.GetRasterBand(1).WriteArray(result)
    #    new_tiff.GetRasterBand(1).SetNoDataValue(np.nan)
        new_tiff.FlushCache() 
        new_tiff=None    
        
        
        
    def update_value(self, result, value, x_map, y_map, mu, count):
        previous_value = result[x_map, y_map]
        new_value = self.do_operation(previous_value, value, mu)
        result[x_map, y_map] = new_value
        count += 1
    #link    
    def do_operation(self, previous_value, value, mu):
        (value - mu) **2    
    
    
    def get_pixel_value(self, raster_location:str, x_coo: float, y_coo: float):
        tiff_file, geotransform, projection, band, xsize, ysize, nodata = self.import_tiff(raster_location)
        local_x_map = int((x_coo - geotransform[0]) / geotransform[1])
        local_y_map = int((y_coo - geotransform[3]) / geotransform[5])
        pixel_value = band.ReadAsArray(local_x_map, local_y_map,1,1)
#        self.__delattr__("tiff_file")#, "geotransform", "projection", "band", "xsize", "ysize", "nodata")
#        self.__delattr__("band")
        return pixel_value
    
    def import_tiff(self, raster_location:str):
        tiff_file = gdal.Open(raster_location)
        geotransform = tiff_file.GetGeoTransform()
        projection = tiff_file.GetProjection()
        band = tiff_file.GetRasterBand(1)    
        xsize = band.XSize
        ysize = band.YSize
        nodata = band.GetNoDataValue()
        return tiff_file, geotransform, projection, band, xsize, ysize, nodata
    #link
#    def close(self,*args):#tiff_file, geotransform, projection, band, xsize, ysize, nodata):
#    #    tiff_file, geotransform, projection, band, xsize, ysize, nodata = None
#        for i in kargs.keys():
#            print("{}".format(i))
#            pass
##            self.__delete__(i)# = "aa"
##            print(self.__dict__[i], "{}".format(i))
##            i = None 
    
    #
    #
    #
    #
    def get_pixel_coordinates(self, x_map, y_map, geotransform):
        x_coo = (x_map * geotransform[1]) + geotransform[0]
        y_coo = (y_map * geotransform[5]) + geotransform[3]
        return x_coo, y_coo
    #link
    def create_coo_dict(self, reference_raster_location):
        coordinates = {}
        tiff_file, geotransform, projection, band, xsize, ysize, nodata = self.import_tiff(reference_raster_location)
        for xs in range(xsize):
            for ys in range(ysize):
                coordinates[(xs, ys)] = self.get_pixel_coordinates(xs, ys, geotransform)
#        self.__delattr__("tiff_file", "geotransform", "projection", "band", "nodata", xsize, ysize)
        return coordinates


        
if __name__=="__main__":
    a=calculator(r"E:\GOULD\Landsat\Dee_Vee\selected")
