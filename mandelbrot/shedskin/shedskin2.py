import sys
import datetime
import math

# Compilation note:
# shedskin shedskin1.py

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3

# Mark Darfour's version without complex numbers in critical loop


def calculate_z_serial_purepython(q, maxiter, z):
    output = [0] * len(q)
    for i in range(len(q)):
        zx, zy = z[i].real, z[i].imag
        qx, qy = q[i].real, q[i].imag
        for iteration in range(maxiter):
            # expand complex numbers to floats, do raw float arithmetic
            zx_new = (zx * zx - zy * zy) + qx
            zy_new = (2 * (zx * zy)) + qy # note that zx(old) is used so we make zx_new on previous line
            zx = zx_new
            zy = zy_new
            # remove need for abs and just square the numbers
            if zx*zx + zy*zy > 4.0:
                output[i] = iteration
                break
    return output


def calc_pure_python(show_output):
    # make a list of x and y values which will represent q
    # xx and yy are the co-ordinates, for the default configuration they'll look like:
    # if we have a 1000x1000 plot
    # xx = [-2.13, -2.1242, -2.1184000000000003, ..., 0.7526000000000064, 0.7584000000000064, 0.7642000000000064]
    # yy = [1.3, 1.2948, 1.2895999999999999, ..., -1.2844000000000058, -1.2896000000000059, -1.294800000000006]
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x = []
    y = []
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

    print "Total elements:", len(z)
    start_time = datetime.datetime.now()
    output = calculate_z_serial_purepython(q, maxiter, z)
    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print "Main took", secs

    validation_sum = sum(output)
    print "Total sum of elements (for validation):", validation_sum

    # uncomment this to verify image output, use Python only
    #if show_output:
    #    import Image
    #    # convert our output to PIL-compatible input
    #    import array
    #    output = ((o + (256*o) + (256**2)*o) * 8 for o in output)
    #    output = array.array('I', output)
    #    # display with PIL
    #    im = Image.new("RGB", (w/2, h/2))
    #    im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
    #    im.show()

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    if len(sys.argv) == 1:
        w = h = 1000
        maxiter = 1000
    else:
        w = int(sys.argv[1])
        h = int(sys.argv[1])
        maxiter = int(sys.argv[2])

    # we can show_output for Python, not for PyPy
    validation_sum = calc_pure_python(True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 1148485 # if False then we have a bug


