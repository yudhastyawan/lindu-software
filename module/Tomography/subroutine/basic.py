import numpy as np


# def diff(x, y):
#     yb2 = []
#     for i in range(len(y)):
#         if (i <= (len(y) - 3)):
#             yb2.append((-y[i + 2] + 4 * y[i + 1] - 3 * y[i]) / (2 * (x[i + 1] - x[i])))
#         else:
#             yb2.append((3 * y[i] - 4 * y[i - 1] + y[i - 2]) / (2 * (x[i] - x[i - 1])))
#     return yb2

def diff(x, y):
    yb2 = []
    for i in range(len(y)):
        if (i <= (len(y) - 2)):
            yb2.append((y[i + 1] - y[i]) / ((x[i + 1] - x[i])))
        else:
            yb2.append((y[i] - y[i - 1]) / ((x[i] - x[i - 1])))
    return yb2


def find(z, a, dvzi):
    for i in range(len(z)):
        if (z[i] <= a):
            x = dvzi[i]
        else:
            break
    return x


def mid(x1, x2):
    xmid = 0.5 * (x1 + x2)
    return xmid


def diff_cube(vxyz, x, y, z):
    dvx = np.zeros(vxyz.shape)
    for i in range(vxyz.shape[2]):
        for j in range(vxyz.shape[1]):
            dvx[:, j, i] = diff(x, vxyz[:, j, i])
    dvy = np.zeros(vxyz.shape)
    for i in range(vxyz.shape[2]):
        for j in range(vxyz.shape[0]):
            dvy[j, :, i] = diff(y, vxyz[j, :, i])
    dvz = np.zeros(vxyz.shape)
    for i in range(vxyz.shape[0]):
        for j in range(vxyz.shape[1]):
            dvz[i, j, :] = diff(z, vxyz[i, j, :])
    return dvx, dvy, dvz


def index(x, y, z, xi, yi, zi):
    i = np.abs(np.fix((xi - x[0]) / (x[1] - x[0])))
    j = np.abs(np.fix((yi - y[0]) / (y[1] - y[0])))
    k = np.abs(np.fix((zi - z[0]) / (z[1] - z[0])))
    return int(i), int(j), int(k)

def colatlon(lat,lon):
    colat = 90 - lat
    if lon >= 0 and lon <= 180:
        colon = lon
    else:
        colon = 360 + lon
    return colat, colon

def colatlon2km(colat,colon,deg2km):
    x = colon*deg2km
    y = colat*deg2km
    return x,y

def noblok(i,j,k,nx,ny):
    nblok = (k)*nx*ny+(j)*nx+i
    return nblok