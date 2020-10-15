import numpy as np
import shutil
import os
import modules.Tomography.submodule.analyze2D.submodule.subroutine.basic as bs
import modules.Tomography.submodule.analyze2D.submodule.subroutine.actRay as ray
from tempfile import mkdtemp


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

    if niter == 0:
        return xi, yi
    else:
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

def fwdModel(srcfile,statfile,velfile,gr,biter,cacah):
    # progress_callback.emit('load data')
    tempdir = mkdtemp()
    nsrc = 0
    file = open(srcfile, 'r')
    source = file.readlines()
    for i in range(len(source)):
        source[i] = source[i].split()
        if source[i] != []:
            nsrc = nsrc + 1
    file.close()

    file = open(srcfile, 'r')
    source2 = file.readlines()
    file.close()

    nstat = 0
    file = open(statfile, 'r')
    station = file.readlines()
    for i in range(len(station)):
        station[i] = station[i].split()
        if station[i] != []:
            nstat = nstat + 1
    file.close()

    tempvel = os.path.join(tempdir,'vel.npz')
    shutil.copyfile(velfile,tempvel)
    vel2d = np.load(tempvel)
    vel = vel2d['vel']
    x = vel2d['x']
    y = vel2d['y']

    dvx, dvy = bs.velDiff(vel, x, y)

    ray2d = np.zeros(vel.shape)
    raypath = np.zeros((nsrc*nstat,2,cacah+1))
    # file = open(evtfile,'w')
    i = 0
    while i < len(source) and source[i] != []:
        # file.write('#'+'\t'+source2[i])
        xs = float(source[i][1])
        ys = float(source[i][2])
        j = 0
        while j < len(station) and station[j] != []:
            temp2d = np.zeros(ray2d.shape)
            tobs = 0
            print(
                'creating t obs -> ' + 'event i-th: ' + str(
                    i + 1) + ', event ID: ' + str(source[i][0])
                + ', station ID: ' + str(station[j][0]))
            xr = float(station[j][1])
            yr = float(station[j][2])
            xi, yi = iterbending(biter, cacah, x, y, vel, xs, ys, xr, yr, dvx, dvy)
            raypath[i*(nstat)+j,:,:] = np.array([xi,yi])
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
                    tobs = tobs + dtc
            ray2d = ray2d + temp2d
            # file.write(station[j][0]+'\t'+str(tobs)+'\n')
            j = j + 1
        i = i + 1

    # tempray = os.path.join(tempdir,'ray.npz')
    # np.savez(tempray,grid=ray2d,path=raypath,x=x,y=y)
    # shutil.copyfile(tempray,rayfile)

    return tobs

srcfile = 'D:/Testing/TA/Sintetik/2D/test result/tes6.src'
statfile = 'D:/Testing/TA/Sintetik/2D/test result/tes6.stat'
velfile = 'D:/Testing/TA/Sintetik/2D/test result/tes6.vel2d'
# evtfile = 'D:/Testing/Anlyze2D/fwd/evt4.evt'
# rayfile = 'D:/Testing/Anlyze2D/fwd/ray4.ray2d'
gr = 100
biter = 100
cacah = 20
tobs = []
for i in range(100):
    a = fwdModel(srcfile,statfile,velfile,gr,i,cacah)
    tobs.append(a)

import matplotlib.pyplot as plt
plt.plot(tobs)
plt.ylabel('t obs')
plt.xlabel('iteration i-th')
plt.title('T obs vs. Iteration')
plt.show()