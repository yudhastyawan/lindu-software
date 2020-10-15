import numpy as np

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

def param(event, station, velocity, deg2km, nx, ny, nz):
    # define lat min-max, lon min-max, and depth max
    lat = []
    lon = []
    depth = []
    i = 0
    while i < len(event):
        if event[i][0] == '#' and event[i] != []:
            lat.append(float(event[i][7]))
            lon.append(float(event[i][8]))
            depth.append(float(event[i][9]))
        if event[i][0] != '#' and event[i] != []:
            j = 0
            while j < len(station):
                if event[i][0] == station[j][0]:
                    lat.append(float(station[j][1]))
                    lon.append(float(station[j][2]))
                j = j+1
        i = i+1

    lat_min = min(lat)
    lat_max = max(lat)
    lon_min = min(lon)
    lon_max = max(lon)

    colat_min,colon_min = colatlon(lat_min,lon_min)
    colat_max,colon_max = colatlon(lat_max,lon_max)

    depth_max = max(depth)

    xmin,ymin = colatlon2km(colat_min,colon_min,deg2km)
    xmax,ymax = colatlon2km(colat_max,colon_max,deg2km)

    x = np.linspace(xmin,xmax,nx)
    y = np.linspace(ymin,ymax,ny)
    z = np.linspace(0,depth_max,nz)

    vz = np.zeros(len(z))
    for i in range(len(z)):
        for j in range(len(velocity)):
            if z[i]>=float(velocity[j][0]) and z[i]<float(velocity[j+1][0]) and j+1<len(velocity):
                vz[i]=(velocity[j][1])
            if z[i]>=float(velocity[j][0]) and j+1>=len(velocity):
                vz[i]=(velocity[j][1])

    v = np.zeros((x.__len__(),y.__len__(),z.__len__()))
    for i in range(x.__len__()):
        for j in range(y.__len__()):
            v[i,j,:] = vz[:]

    return x,y,z,v

def param2(event, station, velocity, deg2km, nx, ny, nz):
    # define lat min-max, lon min-max, and depth max
    colat = []
    colon = []
    depth = []
    i = 0
    while i < len(event):
        if event[i][0] == '#' and event[i] != []:
            colatx, colonx = colatlon(float(event[i][7]), float(event[i][8]))
            colat.append(colatx)
            colon.append(colonx)
            depth.append(float(event[i][9]))
        if event[i][0] != '#' and event[i] != []:
            j = 0
            while j < len(station):
                if event[i][0] == station[j][0]:
                    colatx, colonx = colatlon(float(station[j][1]), float(station[j][2]))
                    colat.append(colatx)
                    colon.append(colonx)
                j = j+1
        i = i+1

    colat_min = min(colat)
    colat_max = max(colat)
    colon_min = min(colon)
    colon_max = max(colon)

    depth_max = max(depth)

    xmin,ymin = colatlon2km(colat_min,colon_min,deg2km)
    xmax,ymax = colatlon2km(colat_max,colon_max,deg2km)

    x = np.linspace(xmin,xmax,nx)
    y = np.linspace(ymin,ymax,ny)
    z = np.linspace(0,depth_max,nz)

    vz = np.zeros(len(z))
    for i in range(len(z)):
        for j in range(len(velocity)):
            if z[i]>=float(velocity[j][0]) and z[i]<float(velocity[j+1][0]) and j+1<len(velocity):
                vz[i]=(velocity[j][1])
            if z[i]>=float(velocity[j][0]) and j+1>=len(velocity):
                vz[i]=(velocity[j][1])

    v = np.zeros((x.__len__(),y.__len__(),z.__len__()))
    for i in range(x.__len__()):
        for j in range(y.__len__()):
            v[i,j,:] = vz[:]

    return x,y,z,v

def paramS(event, station, velocity, deg2km, nx, ny, nz):
    # define lat min-max, lon min-max, and depth max
    colat = []
    colon = []
    depth = []
    i = 0
    while i < len(event):
        if event[i][0] == '#' and event[i] != []:
            colatx, colonx = colatlon(float(event[i][7]), float(event[i][8]))
            colat.append(colatx)
            colon.append(colonx)
            depth.append(float(event[i][9]))
        if event[i][0] != '#' and event[i] != []:
            j = 0
            while j < len(station):
                if event[i][0] == station[j][0]:
                    colatx, colonx = colatlon(float(station[j][1]), float(station[j][2]))
                    colat.append(colatx)
                    colon.append(colonx)
                j = j+1
        i = i+1

    colat_min = min(colat)
    colat_max = max(colat)
    colon_min = min(colon)
    colon_max = max(colon)

    depth_max = max(depth)

    xmin,ymin = colatlon2km(colat_min,colon_min,deg2km)
    xmax,ymax = colatlon2km(colat_max,colon_max,deg2km)

    x = np.linspace(xmin,xmax,nx)
    y = np.linspace(ymin,ymax,ny)
    z = np.linspace(0,depth_max,nz)

    vz = np.zeros(len(z))
    for i in range(len(z)):
        for j in range(len(velocity)):
            if z[i]>=float(velocity[j][0]) and z[i]<float(velocity[j+1][0]) and j+1<len(velocity):
                vz[i]=(velocity[j][2])
            if z[i]>=float(velocity[j][0]) and j+1>=len(velocity):
                vz[i]=(velocity[j][2])

    v = np.zeros((x.__len__(),y.__len__(),z.__len__()))
    for i in range(x.__len__()):
        for j in range(y.__len__()):
            v[i,j,:] = vz[:]

    return x,y,z,v

