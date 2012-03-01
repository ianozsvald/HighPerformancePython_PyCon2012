# Mandelbrot calculate using GPU, Serial numpy and faster numpy
# Use to show the speed difference between CPU and GPU calculations
# ian@ianozsvald.com March 2010

# Based on vegaseat's TKinter/numpy example code from 2006
# http://www.daniweb.com/code/snippet216851.html#
# with minor changes to move to numpy from the obsolete Numeric

import datetime
import sys
import numpy as np
import Image

# You can choose a calculation routine below (calculate_z), uncomment
# one of the three lines to test the three variations
# Speed notes are listed in the same place

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


def show(output):
    """Convert list to numpy array, show using PIL"""
    try:
        import Image
        # convert our output to PIL-compatible input
        #import array
        #output = ((o + (256*o) + (256**2)*o) * 8 for o in output)
        #output = array.array('I', output)
        # display with PIL
        output = (output + (256*output) + (256**2)*output) * 8
        im = Image.new("RGB", (w/2, h/2))
        im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
        im.show()
    except ImportError as err:
        # Bail gracefully if we don't have PIL
        print "Couldn't import Image or numpy:", str(err)


def calculate_z(q, maxiter, z):
    """Pure python with complex datatype, iterating over list of q and z"""
    output = np.array([0] * len(q), dtype=np.int32)
    for i in range(len(q)):
        zi = z[i]
        qi = q[i]
        if i % 1000 == 0:
            # print out some progress info since it is so slow...
            print "%0.2f%% complete" % (1.0/len(q) * i * 100)
        for iteration in range(maxiter):
            zi = zi * zi + qi
            if abs(zi) > 2.0:
                output[i] = iteration
                break
    return output


def calculate_z_mathexpanded(q, maxiter, z):
    """ Generate a mandelbrot set """
    output = np.array([0] * len(q), dtype=np.int32)
    for i in range(len(q)):
        zx = z[i].real # need to extract items using dot notation
        zy = z[i].imag
        qx = q[i].real
        qy = q[i].imag
        if i % 100 == 0:
            print i, len(q)

        for iteration in range(maxiter):
            zx_new = (zx * zx - zy * zy) + qx
            zy_new = (zx * zy + zy * zx) + qy
            # must assign after else we're using the new zx/zy in the fla
            zx = zx_new
            zy = zy_new
            if (zx*zx + zy*zy) > 4.0:
                output[i] = iteration
                break
    return output


def calculate(show_output):
    # make a list of x and y values which will represent q
    # xx and yy are the co-ordinates, for the default configuration they'll look like:
    # if we have a 1000x1000 plot
    # xx = [-2.13, -2.1242, -2.1184000000000003, ..., 0.7526000000000064, 0.7584000000000064, 0.7642000000000064]
    # yy = [1.3, 1.2948, 1.2895999999999999, ..., -1.2844000000000058, -1.2896000000000059, -1.294800000000006]
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x=[]
    y=[]
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    q = []
    for ycoord in y:
        for xcoord in x:
            q.append(complex(xcoord, ycoord))
    z = [0+0j] * len(q)

    print "Total elements:", len(y)*len(x)
    # convert Python lists into numpy arrays
    q_np = np.array(q)
    z_np = np.array(z)

    start_time = datetime.datetime.now()
    output = calculate_z(q_np, maxiter, z_np)
    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print "Main took", secs

    validation_sum = np.sum(output)
    print "Total sum of elements (for validation):", validation_sum

    if show_output:
        show(output)

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    # 'python mandelbrot_pypy.py 1000 1000'
    if len(sys.argv) == 1:
        w = h = 1000
        maxiter = 1000
    else:
        w = int(sys.argv[1])
        h = int(sys.argv[1])
        maxiter = int(sys.argv[2])

    # we can show_output for Python, not for PyPy
    validation_sum = calculate(True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 1148485 # if False then we have a bug

