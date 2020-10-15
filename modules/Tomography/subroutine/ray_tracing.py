import numpy as np


def ray_bending(x1, y1, z1, x2, y2, z2, dvx, dvy, dvz, xmid, ymid, zmid, dvxm, dvym, dvzm, Vmid, V1, V2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    L2 = pow(dx, 2) + pow(dy, 2) + pow(dz, 2)
    nL = dx * dvx + dy * dvy + dz * dvz
    nx = dvx - nL * dx / L2
    ny = dvx - nL * dy / L2
    nz = dvz - nL * dz / L2

    nl = np.sqrt(pow(nx, 2) + pow(ny, 2) + pow(nz, 2))
    nx = nx / (nl+10**(-6))
    ny = ny / (nl+10**(-6))
    nz = nz / (nl+10**(-6))

    l = pow(x2 - xmid, 2) + pow(y2 - ymid, 2) + pow(z2 - zmid, 2)
    c = 0.5 / V1 + 0.5 / V2
    ra = pow(0.25 * (c * Vmid + 1) / (c * (nx * dvxm + ny * dvym + nz * dvzm)+10**(-6)), 2)
    rb = 0.5 * l / (c * Vmid)
    Rc = -0.25 * (c * Vmid + 1) / (c * (nx * dvxm + ny * dvym + nz * dvzm)+10**(-6)) + np.sqrt(ra + rb)
    xnew = xmid + nx * Rc
    ynew = ymid + ny * Rc
    znew = zmid + nz * Rc
    return xnew, ynew, znew