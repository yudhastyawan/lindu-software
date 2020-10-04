import numpy as np
# from scipy.linalg import inv
from numpy.linalg import inv
import module.Tomography.subroutine.parameterization as pr
import module.Tomography.subroutine.basic as bs
import module.Tomography.subroutine.ray_tracing as ray

def iterbending(niter,cacah,x,y,z,vxyz,xs,ys,zs,xr,yr,dvx,dvy,dvz):

    xi = [xr, xs]
    yi = [yr, ys]
    zi = [0, zs]

    xi = np.linspace(xi[0], xi[1], cacah + 1)
    yi = np.linspace(yi[0], yi[1], cacah + 1)
    zi = np.linspace(zi[0], zi[1], cacah + 1)

    xb = np.zeros(len(xi))
    yb = np.zeros(len(xi))
    zb = np.zeros(len(xi))

    for j in range(niter):
        for i in range(cacah - 1):
            x1 = xi[i]
            y1 = yi[i]
            z1 = zi[i]
            x2 = xi[i + 2]
            y2 = yi[i + 2]
            z2 = zi[i + 2]
            xmid = bs.mid(x1, x2)
            ymid = bs.mid(y1, y2)
            zmid = bs.mid(z1, z2)
            o, p, q = bs.index(x, y, z, x1, y1, z1)
            if o < len(dvx[:,0,0]) and p < len(dvx[0,:,0]) and q < len(dvx[0,0,:]):
                dvxi = dvx[o, p, q]
                dvyi = dvy[o, p, q]
                dvzi = dvz[o, p, q]
                V1 = vxyz[o, p, q]
            else:
                return xi, yi, zi
            o, p, q = bs.index(x, y, z, x2, y2, z2)
            if o < len(dvx[:,0,0]) and p < len(dvx[0,:,0]) and q < len(dvx[0,0,:]):
                V2 = vxyz[o, p, q]
            else:
                return xi, yi, zi
            o, p, q = bs.index(x, y, z, xmid, ymid, zmid)
            if o < len(dvx[:,0,0]) and p < len(dvx[0,:,0]) and q < len(dvx[0,0,:]):
                dvxm = dvx[o, p, q]
                dvym = dvy[o, p, q]
                dvzm = dvz[o, p, q]
                Vmid = vxyz[o, p, q]
            else:
                return xi, yi, zi
            xn, yn, zn = ray.ray_bending(x1, y1, z1, x2, y2, z2, dvxi, dvyi, dvzi, xmid, ymid, zmid, dvxm, dvym, dvzm,
                                         Vmid,V1, V2)
            if np.isnan(xn) == False and np.isnan(yn) == False and np.isnan(zn) == False:
                o, p, q = bs.index(x, y, z, xn, yn, zn)
                if o < len(dvx[:,0,0]) and p < len(dvx[0,:,0]) and q < len(dvx[0,0,:]):
                    xb[i + 1] = xn
                    yb[i + 1] = yn
                    zb[i + 1] = zn
                else:
                    return xi, yi, zi
            else:
                return xi, yi, zi

        xb[0] = xi[0]
        yb[0] = yi[0]
        zb[0] = zi[0]
        xb[-1] = xi[-1]
        yb[-1] = yi[-1]
        zb[-1] = zi[-1]
        if min(zb) >= min(zi) and max(zb) <= max(zi):
            xi = xb
            yi = yb
            zi = zb
        else:
            return xi, yi, zi
    return xi,yi,zi

def inversion(evtfile,statfile,velfile,deg2km,nx,ny,nz,normd,gradd,iter,gr,biter,cacah,progress_callback):
    progress_callback.emit('load data')
    file = open(evtfile,'r')
    event = file.readlines()
    for i in range(len(event)):
        event[i] = event[i].split()
    file.close()

    file = open(statfile,'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
    file.close()

    file = open(velfile,'r')
    velocity = file.readlines()
    for i in range(len(velocity)):
        velocity[i] = velocity[i].split()
    file.close()

    progress_callback.emit('parameterization')
    x,y,z,vxyz = pr.param2(event,station,velocity,deg2km,nx,ny,nz)

    rms = np.zeros(iter)
    for niter in range(iter):
        dvx, dvy, dvz = bs.diff_cube(vxyz,x,y,z)

        # membuat kernel
        ntr = 0
        for i in range(len(event)):
            if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'P':
                ntr = ntr + 1

        k = np.zeros((ntr+vxyz.size+vxyz.size,vxyz.size))
        tcal = np.zeros((ntr+vxyz.size+vxyz.size,1))
        tobs = np.zeros((ntr+vxyz.size+vxyz.size,1))

        i = 0
        tri = 0
        evi = 0
        while i < len(event):
            if event[i] != []:
                if event[i][0] == '#':
                    progress_callback.emit('iteration i-th: ' + str(niter+1) + ', forward modelling -> ' +'event i-th: ' + str(evi+1) + ', event ID: ' + str(event[i][-1]))
                    lats = float(event[i][7])
                    lons = float(event[i][8])
                    zs = float(event[i][9])
                    colats, colons = pr.colatlon(lats, lons)
                    xs, ys = pr.colatlon2km(colats, colons, deg2km)
                    r = i + 1
                    if r < len(event):
                        while r <len(event) and event[r][0] != '#' and event[r][-1] == 'P':
                            # print(event[r])
                            tobs[tri,0] = float(event[r][1])
                            j = 0
                            while j < len(station):
                                if event[r][0] == station[j][0]:
                                    latr = float(station[j][1])
                                    lonr = float(station[j][2])
                                    colatr, colonr = pr.colatlon(latr, lonr)
                                    xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                    xi,yi,zi = iterbending(biter,cacah,x,y,z,vxyz,xs,ys,zs,xr,yr,dvx,dvy,dvz)
                                    #---------------------
                                    for g in range(len(xi)-1):
                                        o1, p1, q1 = bs.index(x, y, z, xi[g], yi[g], zi[g])
                                        o2, p2, q2 = bs.index(x, y, z, xi[g+1], yi[g+1], zi[g+1])
                                        ngr = np.abs(o2-o1)+np.abs(p2-p1)+np.abs(q2-q1)+1
                                        lgr = gr*ngr
                                        xsp = np.linspace(xi[g],xi[g+1],int(lgr))
                                        ysp = np.linspace(yi[g],yi[g+1],int(lgr))
                                        zsp = np.linspace(zi[g],zi[g+1],int(lgr))
                                        for ii in range(lgr-1):
                                            l = np.sqrt(
                                                pow(xsp[ii] - xsp[ii+1], 2) + pow(ysp[ii] - ysp[ii+1], 2) + pow(zsp[ii] - zsp[ii+1], 2))
                                            oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                            dtc = l/vxyz[oi,pi,qi]
                                            nb = bs.noblok(oi, pi, qi, nx, ny)
                                            k[tri, nb] = k[tri, nb] + l
                                            tcal[tri,0] = tcal[tri,0] + dtc
                                j = j + 1
                            tri = tri + 1
                            r = r + 1
                    evi = evi + 1
            i = i + 1

        progress_callback.emit('iteration i-th: ' + str(niter + 1) + ', inversion')
        dtco = tobs-tcal
        rms[niter] = np.sum(np.power(dtco,2))

        iden = np.eye(vxyz.size)
        k[ntr:ntr+vxyz.size,0::] = normd*iden

        gamma = np.zeros((vxyz.size,vxyz.size))
        n = 0
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    pem = 0
                    if i - 1 >= 0:
                        nb = bs.noblok(i-1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if i + 1 < nx:
                        nb = bs.noblok(i+1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j - 1 >= 0:
                        nb = bs.noblok(i, j-1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j + 1 < ny:
                        nb = bs.noblok(i, j+1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk - 1 >= 0:
                        nb = bs.noblok(i, j, kk-1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk + 1 < nz:
                        nb = bs.noblok(i, j, kk+1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    gamma[n,:] = gamma[n,:]/pem
                    nb = bs.noblok(i, j, kk, nx, ny)
                    gamma[n, nb] = 1
                    n = n + 1

        k[(ntr+vxyz.size)::,0::] = gradd*gamma


        # inversion
        ds = np.mat(inv(np.mat(k.transpose())*np.mat(k)))*np.mat(k.transpose())*np.mat(dtco)
        dv = np.zeros(vxyz.size)

        v0 = np.zeros(vxyz.size)
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    nb = bs.noblok(i, j, kk, nx, ny)
                    v0[nb] = vxyz[i,j,kk]

        for i in range(vxyz.size):
            dv[i] = (-1*ds[i]*(v0[i]**2))/(1+ds[i]*v0[i])

        v1 = np.zeros(vxyz.size)
        for jj in range(len(v1)):
            v1[jj] = v0[jj] + dv[jj]

        vxyzn = np.zeros(vxyz.shape)

        for ii in range(len(v1)):
            for i in range(nx):
                for j in range(ny):
                    for kk in range(nz):
                        nb = bs.noblok(i, j, kk, nx, ny)
                        if ii == nb:
                            vxyzn[i, j, kk] = v1[ii]
        if vxyzn.min() >= 0:
            vxyz = vxyzn
        else:
            break

    return x,y,z,vxyz,rms

def inversionS(evtfile,statfile,velfile,deg2km,nx,ny,nz,normd,gradd,iter,gr,biter,cacah,progress_callback):
    progress_callback.emit('load data')
    file = open(evtfile,'r')
    event = file.readlines()
    for i in range(len(event)):
        event[i] = event[i].split()
    file.close()

    file = open(statfile,'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
    file.close()

    file = open(velfile,'r')
    velocity = file.readlines()
    for i in range(len(velocity)):
        velocity[i] = velocity[i].split()
    file.close()

    progress_callback.emit('parameterization')
    x,y,z,vxyz = pr.paramS(event,station,velocity,deg2km,nx,ny,nz)

    rms = np.zeros(iter)
    for niter in range(iter):
        dvx, dvy, dvz = bs.diff_cube(vxyz,x,y,z)

        # membuat kernel
        ntr = 0
        for i in range(len(event)):
            if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'S':
                ntr = ntr + 1

        k = np.zeros((ntr+vxyz.size+vxyz.size,vxyz.size))
        tcal = np.zeros((ntr+vxyz.size+vxyz.size,1))
        tobs = np.zeros((ntr+vxyz.size+vxyz.size,1))

        i = 0
        tri = 0
        evi = 0
        while i < len(event):
            if event[i] != []:
                if event[i][0] == '#':
                    progress_callback.emit(
                        'iteration i-th: ' + str(niter + 1) + ', forward modelling -> ' + 'event i-th: ' + str(
                            evi + 1) + ', event ID: ' + str(event[i][-1]))
                    lats = float(event[i][7])
                    lons = float(event[i][8])
                    zs = float(event[i][9])
                    colats, colons = pr.colatlon(lats, lons)
                    xs, ys = pr.colatlon2km(colats, colons, deg2km)
                    r = i + 1
                    if r < len(event):
                        while r <len(event) and event[r][0] != '#' and event[r][-1] == 'S':
                            tobs[tri,0] = float(event[r][1])
                            j = 0
                            while j < len(station):
                                if event[r][0] == station[j][0]:
                                    latr = float(station[j][1])
                                    lonr = float(station[j][2])
                                    colatr, colonr = pr.colatlon(latr, lonr)
                                    xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                    xi,yi,zi = iterbending(biter,cacah,x,y,z,vxyz,xs,ys,zs,xr,yr,dvx,dvy,dvz)
                                    #---------------------
                                    for g in range(len(xi)-1):
                                        o1, p1, q1 = bs.index(x, y, z, xi[g], yi[g], zi[g])
                                        o2, p2, q2 = bs.index(x, y, z, xi[g+1], yi[g+1], zi[g+1])
                                        ngr = np.abs(o2-o1)+np.abs(p2-p1)+np.abs(q2-q1)+1
                                        lgr = gr*ngr
                                        xsp = np.linspace(xi[g],xi[g+1],int(lgr))
                                        ysp = np.linspace(yi[g],yi[g+1],int(lgr))
                                        zsp = np.linspace(zi[g],zi[g+1],int(lgr))
                                        for ii in range(lgr-1):
                                            l = np.sqrt(
                                                pow(xsp[ii] - xsp[ii+1], 2) + pow(ysp[ii] - ysp[ii+1], 2) + pow(zsp[ii] - zsp[ii+1], 2))
                                            oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                            dtc = l/vxyz[oi,pi,qi]
                                            nb = bs.noblok(oi, pi, qi, nx, ny)
                                            k[tri, nb] = k[tri, nb] + l
                                            tcal[tri,0] = tcal[tri,0] + dtc
                                j = j + 1
                            tri = tri + 1
                            r = r + 1
                    evi = evi + 1
            i = i + 1

        progress_callback.emit('iteration i-th: ' + str(niter + 1) + ', inversion')
        dtco = tobs-tcal
        rms[niter] = np.sum(np.power(dtco,2))

        iden = np.eye(vxyz.size)
        k[ntr:ntr+vxyz.size,0::] = normd*iden

        gamma = np.zeros((vxyz.size,vxyz.size))
        n = 0
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    pem = 0
                    if i - 1 >= 0:
                        nb = bs.noblok(i-1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if i + 1 < nx:
                        nb = bs.noblok(i+1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j - 1 >= 0:
                        nb = bs.noblok(i, j-1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j + 1 < ny:
                        nb = bs.noblok(i, j+1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk - 1 >= 0:
                        nb = bs.noblok(i, j, kk-1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk + 1 < nz:
                        nb = bs.noblok(i, j, kk+1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    gamma[n,:] = gamma[n,:]/pem
                    nb = bs.noblok(i, j, kk, nx, ny)
                    gamma[n, nb] = 1
                    n = n + 1

        k[(ntr+vxyz.size)::,0::] = gradd*gamma


        # inversion
        ds = np.mat(inv(np.mat(k.transpose())*np.mat(k)))*np.mat(k.transpose())*np.mat(dtco)
        dv = np.zeros(vxyz.size)

        v0 = np.zeros(vxyz.size)
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    nb = bs.noblok(i, j, kk, nx, ny)
                    v0[nb] = vxyz[i,j,kk]

        for i in range(vxyz.size):
            dv[i] = (-1*ds[i]*(v0[i]**2))/(1+ds[i]*v0[i])

        v1 = np.zeros(vxyz.size)
        for jj in range(len(v1)):
            v1[jj] = v0[jj] + dv[jj]

        vxyzn = np.zeros(vxyz.shape)

        for ii in range(len(v1)):
            for i in range(nx):
                for j in range(ny):
                    for kk in range(nz):
                        nb = bs.noblok(i, j, kk, nx, ny)
                        if ii == nb:
                            vxyzn[i, j, kk] = v1[ii]
        if vxyzn.min() >= 0:
            vxyz = vxyzn
        else:
            break

    return x,y,z,vxyz,rms

def inversion_test(evtfile,statfile,velfile,deg2km,nx,ny,nz,normd,gradd,iter,gr,biter,cacah,pert,progress_callback):
    progress_callback.emit('load data')
    file = open(evtfile,'r')
    event = file.readlines()
    for i in range(len(event)):
        event[i] = event[i].split()
    file.close()

    file = open(statfile,'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
    file.close()

    file = open(velfile,'r')
    velocity = file.readlines()
    for i in range(len(velocity)):
        velocity[i] = velocity[i].split()
    file.close()

    progress_callback.emit('parameterization')
    x,y,z,vxyz = pr.param2(event,station,velocity,deg2km,nx,ny,nz)

    perturbation = pert
    vmean = np.ceil(np.mean(vxyz))
    vel = np.ones(vxyz.shape)*vmean
    vxyz = vel

    velr = np.zeros(vel.shape)
    for i in range(velr.shape[0]):
        for j in range(velr.shape[1]):
            for k in range(velr.shape[2]):
                nb = bs.noblok(i, j, k, nx, ny)
                if np.mod(nb,2) == 0:
                    velr[i,j,k] = vmean + vmean*perturbation
                else:
                    velr[i, j, k] = vmean - vmean * perturbation

    dvxr, dvyr, dvzr = bs.diff_cube(velr, x, y, z)
    # membuat kernel
    ntr = 0
    for i in range(len(event)):
        if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'P':
            ntr = ntr + 1

    k = np.zeros((ntr + vxyz.size + vxyz.size, vxyz.size))
    tobs = np.zeros((ntr + vxyz.size + vxyz.size, 1))

    i = 0
    tri = 0
    evi = 0
    while i < len(event):
        if event[i] != []:
            if event[i][0] == '#':
                progress_callback.emit(
                    'creating t obs -> ' + 'event i-th: ' + str(
                        evi + 1) + ', event ID: ' + str(event[i][-1]))
                lats = float(event[i][7])
                lons = float(event[i][8])
                zs = float(event[i][9])
                colats, colons = pr.colatlon(lats, lons)
                xs, ys = pr.colatlon2km(colats, colons, deg2km)
                r = i + 1
                if r < len(event):
                    while r < len(event) and event[r][0] != '#' and event[r][-1] == 'P':
                        j = 0
                        while j < len(station):
                            if event[r][0] == station[j][0]:
                                latr = float(station[j][1])
                                lonr = float(station[j][2])
                                colatr, colonr = pr.colatlon(latr, lonr)
                                xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                xir, yir, zir = iterbending(biter, cacah, x, y, z, velr, xs, ys, zs, xr, yr, dvxr, dvyr,
                                                            dvzr)
                                # ---------------------
                                for g in range(len(xir) - 1):
                                    o1, p1, q1 = bs.index(x, y, z, xir[g], yir[g], zir[g])
                                    o2, p2, q2 = bs.index(x, y, z, xir[g + 1], yir[g + 1], zir[g + 1])
                                    ngr = np.abs(o2 - o1) + np.abs(p2 - p1) + np.abs(q2 - q1) + 1
                                    lgr = gr * ngr
                                    xsp = np.linspace(xir[g], xir[g + 1], int(lgr))
                                    ysp = np.linspace(yir[g], yir[g + 1], int(lgr))
                                    zsp = np.linspace(zir[g], zir[g + 1], int(lgr))
                                    for ii in range(lgr - 1):
                                        l = np.sqrt(
                                            pow(xsp[ii] - xsp[ii + 1], 2) + pow(ysp[ii] - ysp[ii + 1], 2) + pow(
                                                zsp[ii] - zsp[ii + 1], 2))
                                        oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                        dtc = l / vxyz[oi, pi, qi]
                                        nb = bs.noblok(oi, pi, qi, nx, ny)
                                        k[tri, nb] = k[tri, nb] + l
                                        tobs[tri, 0] = tobs[tri, 0] + dtc
                            j = j + 1
                        tri = tri + 1
                        r = r + 1
                evi = evi + 1
        i = i + 1

    rms = np.zeros(iter)
    for niter in range(iter):
        print(niter)
        dvx, dvy, dvz = bs.diff_cube(vxyz,x,y,z)
        # dvxr, dvyr, dvzr = bs.diff_cube(velr, x, y, z)

        # membuat kernel
        ntr = 0
        for i in range(len(event)):
            if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'P':
                ntr = ntr + 1

        k = np.zeros((ntr+vxyz.size+vxyz.size,vxyz.size))
        tcal = np.zeros((ntr+vxyz.size+vxyz.size,1))
        # tobs = np.zeros((ntr+vxyz.size+vxyz.size,1))

        i = 0
        tri = 0
        evi = 0
        while i < len(event):
            if event[i] != []:
                if event[i][0] == '#':
                    progress_callback.emit(
                        'iteration i-th: ' + str(niter + 1) + ', forward modelling -> ' + 'event i-th: ' + str(
                            evi + 1) + ', event ID: ' + str(event[i][-1]))
                    lats = float(event[i][7])
                    lons = float(event[i][8])
                    zs = float(event[i][9])
                    colats, colons = pr.colatlon(lats, lons)
                    xs, ys = pr.colatlon2km(colats, colons, deg2km)
                    r = i + 1
                    if r < len(event):
                        while r <len(event) and event[r][0] != '#' and event[r][-1] == 'P':
                            # tobs[tri,0] = float(event[r][1])
                            j = 0
                            while j < len(station):
                                if event[r][0] == station[j][0]:
                                    latr = float(station[j][1])
                                    lonr = float(station[j][2])
                                    colatr, colonr = pr.colatlon(latr, lonr)
                                    xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                    xir, yir, zir = iterbending(biter, cacah, x, y, z, velr, xs, ys, zs, xr, yr, dvxr, dvyr,
                                                             dvzr)
                                    xi,yi,zi = iterbending(biter,cacah,x,y,z,vxyz,xs,ys,zs,xr,yr,dvx,dvy,dvz)
                                    #---------------------
                                    for g in range(len(xi)-1):
                                        o1, p1, q1 = bs.index(x, y, z, xi[g], yi[g], zi[g])
                                        o2, p2, q2 = bs.index(x, y, z, xi[g+1], yi[g+1], zi[g+1])
                                        ngr = np.abs(o2-o1)+np.abs(p2-p1)+np.abs(q2-q1)+1
                                        lgr = gr*ngr
                                        xsp = np.linspace(xi[g],xi[g+1],int(lgr))
                                        ysp = np.linspace(yi[g],yi[g+1],int(lgr))
                                        zsp = np.linspace(zi[g],zi[g+1],int(lgr))
                                        for ii in range(lgr-1):
                                            l = np.sqrt(
                                                pow(xsp[ii] - xsp[ii+1], 2) + pow(ysp[ii] - ysp[ii+1], 2) + pow(zsp[ii] - zsp[ii+1], 2))
                                            oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                            dtc = l/vxyz[oi,pi,qi]
                                            nb = bs.noblok(oi, pi, qi, nx, ny)
                                            k[tri, nb] = k[tri, nb] + l
                                            tcal[tri,0] = tcal[tri,0] + dtc
                                j = j + 1
                            tri = tri + 1
                            r = r + 1
                    evi = evi + 1
            i = i + 1

        progress_callback.emit('iteration i-th: ' + str(niter + 1) + ', inversion')
        dtco = tobs-tcal
        rms[niter] = np.sum(np.power(dtco,2))

        iden = np.eye(vxyz.size)
        k[ntr:ntr+vxyz.size,0::] = normd*iden

        gamma = np.zeros((vxyz.size,vxyz.size))
        n = 0
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    pem = 0
                    if i - 1 >= 0:
                        nb = bs.noblok(i-1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if i + 1 < nx:
                        nb = bs.noblok(i+1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j - 1 >= 0:
                        nb = bs.noblok(i, j-1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j + 1 < ny:
                        nb = bs.noblok(i, j+1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk - 1 >= 0:
                        nb = bs.noblok(i, j, kk-1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk + 1 < nz:
                        nb = bs.noblok(i, j, kk+1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    gamma[n,:] = gamma[n,:]/pem
                    nb = bs.noblok(i, j, kk, nx, ny)
                    gamma[n, nb] = 1
                    n = n + 1

        k[(ntr+vxyz.size)::,0::] = gradd*gamma


        # inversion
        ds = np.mat(inv(np.mat(k.transpose())*np.mat(k)))*np.mat(k.transpose())*np.mat(dtco)
        dv = np.zeros(vxyz.size)

        v0 = np.zeros(vxyz.size)
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    nb = bs.noblok(i, j, kk, nx, ny)
                    v0[nb] = vxyz[i,j,kk]

        for i in range(vxyz.size):
            dv[i] = (-1*ds[i]*(v0[i]**2))/(1+ds[i]*v0[i])

        v1 = np.zeros(vxyz.size)
        for jj in range(len(v1)):
            v1[jj] = v0[jj] + dv[jj]

        vxyzn = np.zeros(vxyz.shape)

        for ii in range(len(v1)):
            for i in range(nx):
                for j in range(ny):
                    for kk in range(nz):
                        nb = bs.noblok(i, j, kk, nx, ny)
                        if ii == nb:
                            vxyzn[i, j, kk] = v1[ii]
        if vxyzn.min() >= 0:
            vxyz = vxyzn
        else:
            break

    return x,y,z,vxyz,velr,rms

def inversion_testS(evtfile,statfile,velfile,deg2km,nx,ny,nz,normd,gradd,iter,gr,biter,cacah,pert,progress_callback):
    progress_callback.emit('load data')
    file = open(evtfile,'r')
    event = file.readlines()
    for i in range(len(event)):
        event[i] = event[i].split()
    file.close()

    file = open(statfile,'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
    file.close()

    file = open(velfile,'r')
    velocity = file.readlines()
    for i in range(len(velocity)):
        velocity[i] = velocity[i].split()
    file.close()

    progress_callback.emit('parameterization')
    x,y,z,vxyz = pr.paramS(event,station,velocity,deg2km,nx,ny,nz)

    perturbation = pert
    vmean = np.ceil(np.mean(vxyz))
    vel = np.ones(vxyz.shape)*vmean
    vxyz = vel

    velr = np.zeros(vel.shape)
    for i in range(velr.shape[0]):
        for j in range(velr.shape[1]):
            for k in range(velr.shape[2]):
                nb = bs.noblok(i, j, k, nx, ny)
                if np.mod(nb,2) == 0:
                    velr[i,j,k] = vmean + vmean*perturbation
                else:
                    velr[i, j, k] = vmean - vmean * perturbation

    dvxr, dvyr, dvzr = bs.diff_cube(velr, x, y, z)
    # membuat kernel
    ntr = 0
    for i in range(len(event)):
        if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'S':
            ntr = ntr + 1

    k = np.zeros((ntr + vxyz.size + vxyz.size, vxyz.size))
    tobs = np.zeros((ntr + vxyz.size + vxyz.size, 1))

    i = 0
    tri = 0
    evi = 0
    while i < len(event):
        if event[i] != []:
            if event[i][0] == '#':
                progress_callback.emit(
                    'creating t obs -> ' + 'event i-th: ' + str(
                        evi + 1) + ', event ID: ' + str(event[i][-1]))
                lats = float(event[i][7])
                lons = float(event[i][8])
                zs = float(event[i][9])
                colats, colons = pr.colatlon(lats, lons)
                xs, ys = pr.colatlon2km(colats, colons, deg2km)
                r = i + 1
                if r < len(event):
                    while r < len(event) and event[r][0] != '#' and event[r][-1] == 'S':
                        j = 0
                        while j < len(station):
                            if event[r][0] == station[j][0]:
                                latr = float(station[j][1])
                                lonr = float(station[j][2])
                                colatr, colonr = pr.colatlon(latr, lonr)
                                xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                xir, yir, zir = iterbending(biter, cacah, x, y, z, velr, xs, ys, zs, xr, yr, dvxr, dvyr,
                                                            dvzr)
                                # ---------------------
                                for g in range(len(xir) - 1):
                                    o1, p1, q1 = bs.index(x, y, z, xir[g], yir[g], zir[g])
                                    o2, p2, q2 = bs.index(x, y, z, xir[g + 1], yir[g + 1], zir[g + 1])
                                    ngr = np.abs(o2 - o1) + np.abs(p2 - p1) + np.abs(q2 - q1) + 1
                                    lgr = gr * ngr
                                    xsp = np.linspace(xir[g], xir[g + 1], int(lgr))
                                    ysp = np.linspace(yir[g], yir[g + 1], int(lgr))
                                    zsp = np.linspace(zir[g], zir[g + 1], int(lgr))
                                    for ii in range(lgr - 1):
                                        l = np.sqrt(
                                            pow(xsp[ii] - xsp[ii + 1], 2) + pow(ysp[ii] - ysp[ii + 1], 2) + pow(
                                                zsp[ii] - zsp[ii + 1], 2))
                                        oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                        dtc = l / vxyz[oi, pi, qi]
                                        nb = bs.noblok(oi, pi, qi, nx, ny)
                                        k[tri, nb] = k[tri, nb] + l
                                        tobs[tri, 0] = tobs[tri, 0] + dtc
                            j = j + 1
                        tri = tri + 1
                        r = r + 1
                evi = evi + 1
        i = i + 1

    rms = np.zeros(iter)
    for niter in range(iter):
        print(niter)
        dvx, dvy, dvz = bs.diff_cube(vxyz,x,y,z)
        # dvxr, dvyr, dvzr = bs.diff_cube(velr, x, y, z)

        # membuat kernel
        ntr = 0
        for i in range(len(event)):
            if event[i] != [] and event[i][0] != '#' and event[i][-1] == 'S':
                ntr = ntr + 1

        k = np.zeros((ntr+vxyz.size+vxyz.size,vxyz.size))
        tcal = np.zeros((ntr+vxyz.size+vxyz.size,1))
        # tobs = np.zeros((ntr+vxyz.size+vxyz.size,1))

        i = 0
        tri = 0
        evi = 0
        while i < len(event):
            if event[i] != []:
                if event[i][0] == '#':
                    progress_callback.emit(
                        'iteration i-th: ' + str(niter + 1) + ', forward modelling -> ' + 'event i-th: ' + str(
                            evi + 1) + ', event ID: ' + str(event[i][-1]))
                    lats = float(event[i][7])
                    lons = float(event[i][8])
                    zs = float(event[i][9])
                    colats, colons = pr.colatlon(lats, lons)
                    xs, ys = pr.colatlon2km(colats, colons, deg2km)
                    r = i + 1
                    if r < len(event):
                        while r <len(event) and event[r][0] != '#' and event[r][-1] == 'S':
                            # tobs[tri,0] = float(event[r][1])
                            j = 0
                            while j < len(station):
                                if event[r][0] == station[j][0]:
                                    latr = float(station[j][1])
                                    lonr = float(station[j][2])
                                    colatr, colonr = pr.colatlon(latr, lonr)
                                    xr, yr = pr.colatlon2km(colatr, colonr, deg2km)
                                    xir, yir, zir = iterbending(biter, cacah, x, y, z, velr, xs, ys, zs, xr, yr, dvxr, dvyr,
                                                             dvzr)
                                    xi,yi,zi = iterbending(biter,cacah,x,y,z,vxyz,xs,ys,zs,xr,yr,dvx,dvy,dvz)
                                    #---------------------
                                    for g in range(len(xi)-1):
                                        o1, p1, q1 = bs.index(x, y, z, xi[g], yi[g], zi[g])
                                        o2, p2, q2 = bs.index(x, y, z, xi[g+1], yi[g+1], zi[g+1])
                                        ngr = np.abs(o2-o1)+np.abs(p2-p1)+np.abs(q2-q1)+1
                                        lgr = gr*ngr
                                        xsp = np.linspace(xi[g],xi[g+1],int(lgr))
                                        ysp = np.linspace(yi[g],yi[g+1],int(lgr))
                                        zsp = np.linspace(zi[g],zi[g+1],int(lgr))
                                        for ii in range(lgr-1):
                                            l = np.sqrt(
                                                pow(xsp[ii] - xsp[ii+1], 2) + pow(ysp[ii] - ysp[ii+1], 2) + pow(zsp[ii] - zsp[ii+1], 2))
                                            oi, pi, qi = bs.index(x, y, z, xsp[ii], ysp[ii], zsp[ii])
                                            dtc = l/vxyz[oi,pi,qi]
                                            nb = bs.noblok(oi, pi, qi, nx, ny)
                                            k[tri, nb] = k[tri, nb] + l
                                            tcal[tri,0] = tcal[tri,0] + dtc
                                j = j + 1
                            tri = tri + 1
                            r = r + 1
                    evi = evi + 1
            i = i + 1

        progress_callback.emit('iteration i-th: ' + str(niter + 1) + ', inversion')
        dtco = tobs-tcal
        rms[niter] = np.sum(np.power(dtco,2))

        iden = np.eye(vxyz.size)
        k[ntr:ntr+vxyz.size,0::] = normd*iden

        gamma = np.zeros((vxyz.size,vxyz.size))
        n = 0
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    pem = 0
                    if i - 1 >= 0:
                        nb = bs.noblok(i-1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if i + 1 < nx:
                        nb = bs.noblok(i+1, j, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j - 1 >= 0:
                        nb = bs.noblok(i, j-1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if j + 1 < ny:
                        nb = bs.noblok(i, j+1, kk, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk - 1 >= 0:
                        nb = bs.noblok(i, j, kk-1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    if kk + 1 < nz:
                        nb = bs.noblok(i, j, kk+1, nx, ny)
                        gamma[n, nb] = -1
                        pem = pem + 1
                    gamma[n,:] = gamma[n,:]/pem
                    nb = bs.noblok(i, j, kk, nx, ny)
                    gamma[n, nb] = 1
                    n = n + 1

        k[(ntr+vxyz.size)::,0::] = gradd*gamma


        # inversion
        ds = np.mat(inv(np.mat(k.transpose())*np.mat(k)))*np.mat(k.transpose())*np.mat(dtco)
        dv = np.zeros(vxyz.size)

        v0 = np.zeros(vxyz.size)
        for i in range(nx):
            for j in range(ny):
                for kk in range(nz):
                    nb = bs.noblok(i, j, kk, nx, ny)
                    v0[nb] = vxyz[i,j,kk]

        for i in range(vxyz.size):
            dv[i] = (-1*ds[i]*(v0[i]**2))/(1+ds[i]*v0[i])

        v1 = np.zeros(vxyz.size)
        for jj in range(len(v1)):
            v1[jj] = v0[jj] + dv[jj]

        vxyzn = np.zeros(vxyz.shape)

        for ii in range(len(v1)):
            for i in range(nx):
                for j in range(ny):
                    for kk in range(nz):
                        nb = bs.noblok(i, j, kk, nx, ny)
                        if ii == nb:
                            vxyzn[i, j, kk] = v1[ii]
        if vxyzn.min() >= 0:
            vxyz = vxyzn
        else:
            break

    return x,y,z,vxyz,velr,rms
