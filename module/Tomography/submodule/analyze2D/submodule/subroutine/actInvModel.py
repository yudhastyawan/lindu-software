import numpy as np
import shutil
import os
import module.Tomography.submodule.analyze2D.submodule.subroutine.basic as bs
import module.Tomography.submodule.analyze2D.submodule.subroutine.actRay as ray
from tempfile import mkdtemp
from scipy.linalg import inv


def iterbending(niter,cacah,x,y,vxyz,xs,ys,xr,yr,dvx,dvy):

    xi = [xr, xs]
    yi = [yr, ys]

    if xr != xs:
        xi = np.linspace(xi[0], xi[1], cacah + 1)
    else:
        xi = np.ones(cacah+1)*xr
    if yr != ys:
        yi = np.linspace(yi[0], yi[1], cacah + 1)
    else:
        yi = np.ones(cacah+1)*yr

    xb = np.zeros(len(xi))
    yb = np.zeros(len(xi))

    for j in range(niter):
        for i in range(cacah - 1):
            x1 = xi[i]
            y1 = yi[i]
            x2 = xi[i + 2]
            y2 = yi[i + 2]
            xmid = bs.mid(x1, x2)
            ymid = bs.mid(y1, y2)
            o, p = bs.index(x, y, x1, y1)
            if p < len(dvx[:,0]) and o < len(dvx[0,:]):
                dvxi = dvx[p, o]
                dvyi = dvy[p, o]
                V1 = vxyz[p, o]
            else:
                return xi, yi
            o, p = bs.index(x, y, x2, y2)
            if p < len(dvx[:,0]) and o < len(dvx[0,:]):
                V2 = vxyz[p, o]
            else:
                return xi, yi
            o, p = bs.index(x, y, xmid, ymid)
            if p < len(dvx[:,0]) and o < len(dvx[0,:]):
                dvxm = dvx[p, o]
                dvym = dvy[p, o]
                Vmid = vxyz[p, o]
            else:
                return xi, yi
            xn, yn = ray.rayBending(x1, y1, x2, y2, dvxi, dvyi, xmid, ymid, dvxm, dvym,
                                         Vmid,V1, V2)
            if np.isnan(xn) == False and np.isnan(yn) == False:
                o, p = bs.index(x, y, xn, yn)
                if p < len(dvx[:,0]) and o < len(dvx[0,:]):
                    xb[i + 1] = xn
                    yb[i + 1] = yn
                else:
                    return xi, yi
            else:
                return xi, yi

        xb[0] = xi[0]
        yb[0] = yi[0]
        xb[-1] = xi[-1]
        yb[-1] = yi[-1]
        if min(yb) >= min(yi) and max(yb) <= max(yi):
            xi = xb
            yi = yb
        else:
            return xi, yi
    return xi,yi

def inversion(evtfile,statfile,velfile,rayfile,veloutfile,normd,gradd,iter,gr,biter,cacah,noise,progress_callback):
# def inversion(evtfile, statfile, velfile, rayfile, veloutfile, normd, gradd, iter, gr, biter, cacah, noise):
    progress_callback.emit('load data')
    tempdir = mkdtemp()
    file = open(evtfile, 'r')
    event = file.readlines()
    for i in range(len(event)):
        event[i] = event[i].split()
    file.close()

    file = open(statfile, 'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
    file.close()

    tempvel = os.path.join(tempdir, 'vel.npz')
    shutil.copyfile(velfile, tempvel)
    vel2d = np.load(tempvel)
    vel = vel2d['vel']
    x = vel2d['x']
    y = vel2d['y']

    vinit = vel

    nx = len(x)
    ny = len(y)

    ray2d = np.array([])
    raypath = np.array([])

    rms = np.zeros(iter)
    for niter in range(iter):
        dvx, dvy = bs.velDiff(vel, x, y)
        ray2d = np.zeros(vel.shape)

        # membuat kernel
        ntr = 0
        for i in range(len(event)):
            if event[i] != [] and event[i][0] != '#':
                ntr = ntr + 1

        raypath = np.zeros((ntr, 2, cacah + 1))
        k = np.zeros((ntr + vel.size + vel.size, vel.size))
        tcal = np.zeros((ntr + vel.size + vel.size, 1))
        tobs = np.zeros((ntr + vel.size + vel.size, 1))

        i = 0
        tri = 0
        evi = 0
        while i < len(event):
            if event[i] != []:
                if event[i][0] == '#':
                    progress_callback.emit(
                    # print(
                        'iteration i-th: ' + str(niter + 1) + ', forward modelling -> ' + 'event i-th: ' + str(
                            evi + 1) + ', event ID: ' + str(event[i][1]))
                    xs = float(event[i][2])
                    ys = float(event[i][3])
                    r = i + 1
                    if r < len(event):
                        while r < len(event) and event[r][0] != '#':
                            # print(event[r])
                            tobs[tri, 0] = float(event[r][1])
                            j = 0
                            while j < len(station):
                                if event[r][0] == station[j][0]:
                                    temp2d = np.zeros(ray2d.shape)
                                    xr = float(station[j][1])
                                    yr = float(station[j][2])
                                    xi, yi = iterbending(biter, cacah, x, y, vel, xs, ys, xr, yr, dvx, dvy)
                                    raypath[tri, :, :] = np.array([xi, yi])
                                    for g in range(len(xi) - 1):
                                        o1, p1 = bs.index(x, y, xi[g], yi[g])
                                        o2, p2 = bs.index(x, y, xi[g + 1], yi[g + 1])
                                        ngr = np.abs(o2 - o1) + np.abs(p2 - p1) + 1
                                        lgr = gr * ngr
                                        xsp = np.linspace(xi[g], xi[g + 1], int(lgr))
                                        ysp = np.linspace(yi[g], yi[g + 1], int(lgr))
                                        for ii in range(lgr - 1):
                                            l = np.sqrt(
                                                pow(xsp[ii] - xsp[ii + 1], 2) + pow(ysp[ii] - ysp[ii + 1], 2))
                                            oi, pi = bs.index(x, y, xsp[ii], ysp[ii])
                                            temp2d[pi, oi] = 1
                                            dtc = l / vel[pi, oi]
                                            nb = bs.noblok(oi, pi, nx)
                                            k[tri, nb] = k[tri, nb] + l
                                            tcal[tri, 0] = tcal[tri, 0] + dtc
                                    ray2d = ray2d + temp2d
                                j = j + 1
                            tri = tri + 1
                            r = r + 1
                    evi = evi + 1
            i = i + 1

        progress_callback.emit('iteration i-th: ' + str(niter + 1) + ', inversion')

        # adding noise
        alen = np.abs(tobs.min()-tobs.max())

        am = -1*alen*noise
        ax = alen*noise
        a = np.random.normal(0, 1, ntr)
        amm = a.min()
        axx = a.max()
        for i in range(ntr):
            tobs[i] = tobs[i] + (((ax - am) / (axx - amm)) * (a[i] - amm)) + am

        dtco = tobs - tcal
        rms[niter] = np.sum(np.power(dtco, 2))

        iden = np.eye(vel.size)
        k[ntr:ntr + vel.size, 0::] = normd * iden

        gamma = np.zeros((vel.size, vel.size))
        n = 0
        for i in range(nx):
            for j in range(ny):
                pem = 0
                if i - 1 >= 0:
                    nb = bs.noblok(i - 1, j, nx)
                    gamma[n, nb] = -1
                    pem = pem + 1
                if i + 1 < nx:
                    nb = bs.noblok(i + 1, j, nx)
                    gamma[n, nb] = -1
                    pem = pem + 1
                if j - 1 >= 0:
                    nb = bs.noblok(i, j - 1, nx)
                    gamma[n, nb] = -1
                    pem = pem + 1
                if j + 1 < ny:
                    nb = bs.noblok(i, j + 1, nx)
                    gamma[n, nb] = -1
                    pem = pem + 1
                gamma[n, :] = gamma[n, :] / pem
                nb = bs.noblok(i, j, nx)
                gamma[n, nb] = 1
                n = n + 1

        k[(ntr + vel.size)::, 0::] = gradd * gamma

        # inversion
        ds = np.mat(inv(np.mat(k.transpose()) * np.mat(k))) * np.mat(k.transpose()) * np.mat(dtco)
        dv = np.zeros(vel.size)

        v0 = np.zeros(vel.size)
        for i in range(nx):
            for j in range(ny):
                nb = bs.noblok(i, j, nx)
                v0[nb] = vel[j, i]

        for i in range(vel.size):
            dv[i] = (-1 * ds[i] * (v0[i] ** 2)) / (1 + ds[i] * v0[i])

        v1 = np.zeros(vel.size)
        for jj in range(len(v1)):
            v1[jj] = v0[jj] + dv[jj]

        veln = np.zeros(vel.shape)

        for ii in range(len(v1)):
            for i in range(nx):
                for j in range(ny):
                    nb = bs.noblok(i, j, nx)
                    if ii == nb:
                        veln[j, i] = v1[ii]
        if veln.min() >= 0:
            vel = veln
        else:
            break

    perV = ((vel - vinit)/vinit)*100

    tempray = os.path.join(tempdir, 'ray.npz')
    np.savez(tempray, grid=ray2d, path=raypath, x=x, y=y)
    shutil.copyfile(tempray, rayfile)

    tempfile = os.path.join(mkdtemp(), 'file.npz')
    np.savez(tempfile, vel=vel, x=x, y=y, per = perV, rms=rms)
    shutil.copyfile(tempfile, veloutfile)

if __name__ == '__main__':
    evtfile = 'D:/Testing/Anlyze2D/fwd/crt1.evt'
    statfile = 'D:/Testing/Anlyze2D/Create Model/stat6.stat'
    velfile = 'D:/Testing/Anlyze2D/Create Model/vin6.vel2d'
    rayfile = 'D:/Testing/Anlyze2D/Inverse/crt1.ray2d'
    veloutfile = 'D:/Testing/Anlyze2D/Inverse/crt1.vel2d'
    normd = 20
    gradd = 20
    iter = 10
    gr = 100
    biter = 100
    cacah = 1
    noise = 0
    # main = inversion(evtfile,statfile,velfile,rayfile,veloutfile,normd,gradd,iter,gr,biter,cacah, noise)
