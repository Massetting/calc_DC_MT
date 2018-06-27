
# DataCube MultiTemporal calculator

At this stage there is only one class: calculator(*location*) present in *calculator.py*.

Given a list of tiff files specified at the *location* the script saves three tiff in the folder ../output

The final file includes only data geographically present on the first tiff of the list. This means that if there are areas in other files not overlapping the first file, those will be excluded from the calculation.

The three files result are 
* the number of pixels (to control whether too many areas where removed), 
* the quadratic residuals sum((x-mean)**2) and 
* the variance as ratio of quadratic residuals and pixel number

The average in not computed here, but it is relatively easy to implement splitting the workload in two passes over all the data.


Note. Any additive operation can be implemented simply modifing the calculator.do_operation() method.

1. Retrieve the map and real coordinates from first tiff and save them as dictionary
1. Create a zeros numpy array **F**
1. Create a zeros numpy array **C**
1. Iterate over each pixel **P** present in the dictionary of point 1 
    1. Iterate over all rasters **R** and collect pixel value **PR** (and count **N**)
    1. do **z=(PR-average)^2**
    1. add **z** to **PF** 
    1. assign N to **PC**
1. **L= F/C** 
1. Save F, C and L


This structure is very light in memory usage, but heavy in disk reading. Perhaps, all could be speeded up reading pixels in blocks.
