class tomo_log(object):
    def __init__(self, path, evtdat, statdat, veldat, xout, yout, zout, velog, velobsout, velcalout, velpout, velsout,
                 velpsout, type, deg2km, nx, ny, nz, normd, gradd, iter, cacah, biter, split, pert):
        file = open(path, 'w')
        file.write(
            'Path of Input Data ->' + '\n' +
            'Event File:' + '\t' + evtdat + '\n' +
            'Station File:' + '\t' + statdat + '\n' +
            '1D Velocity File:' + '\t' + veldat + '\n' +
            '\n' +
            'Path of Coordinate Log Output ->' + '\n' +
            'x file:' + '\t' + xout + '\n' +
            'y file:' + '\t' + yout + '\n' +
            'z file:' + '\t' + zout + '\n' +
            'log file:' + '\t' + velog + '\n' +
            '\n' +
            'Path of Test Resolution Output ->' + '\n' +
            'Obs Velocity File:' + '\t' + velobsout + '\n' +
            'Cal Velocity File:' + '\t' + velcalout + '\n' +
            '\n' +
            'Path of Velocity Inversion Output ->' + '\n' +
            'P Velocity Output:' + '\t' + velpout + '\n' +
            'S Velocity Output:' + '\t' + velsout + '\n' +
            'P/S Velocity Output:' + '\t' + velpsout + '\n' +
            '\n' +
            'Settings of Parameters ->' + '\n' +
            'Type of Tomography:' + '\t' + type + '\n' +
            'degree to km:' + '\t' + deg2km + '\n' +
            'Number of X:' + '\t' + nx + '\n' +
            'Number of Y:' + '\t' + ny + '\n' +
            'Number of Z:' + '\t' + nz + '\n' +
            'Norm Value:' + '\t' + normd + '\n' +
            'Gradient Value:' + '\t' + gradd + '\n' +
            'Number of Tomography Iteration:' + '\t' + iter + '\n' +
            'Number of Part of Ray Bending:' + '\t' + cacah + '\n' +
            'Number of Ray Iteration:' + '\t' + biter + '\n' +
            'Number of Splitting Ray Resolution:' + '\t' + split + '\n' +
            'Value of Perturbation Test:' + '\t' + pert + '\n'
        )
        file.close()

def read_log(path):
    file = open(path,'r')
    data = file.readlines()
    for i in range(len(data)):
        data[i] = data[i].split()
    file.close()

    if data[1][-1] != 'File:':
        evtdat = data[1][-1]
    else:
        evtdat = ''
    if data[2][-1] != 'File:':
        statdat = data[2][-1]
    else:
        statdat = ''
    if data[3][-1] != 'File:':
        veldat = data[3][-1]
    else:
        veldat = ''

    if data[6][-1] != 'file:':
        xout = data[6][-1]
    else:
        xout = ''
    if data[7][-1] != 'file:':
        yout = data[7][-1]
    else:
        yout = ''
    if data[8][-1] != 'file:':
        zout = data[8][-1]
    else:
        zout = ''
    if data[9][-1] != 'file:':
        velog = data[9][-1]
    else:
        velog = ''

    if data[12][-1] != 'File:':
        velobsout = data[12][-1]
    else:
        velobsout = ''
    if data[13][-1] != 'File:':
        velcalout = data[13][-1]
    else:
        velcalout = ''

    if data[16][-1] != 'Output:':
        velpout = data[16][-1]
    else:
        velpout = ''
    if data[17][-1] != 'Output:':
        velsout = data[17][-1]
    else:
        velsout = ''
    if data[18][-1] != 'Output:':
        velpsout = data[18][-1]
    else:
        velpsout = ''

    type = data[21][-1]
    deg2km = data[22][-1]
    nx = data[23][-1]
    ny = data[24][-1]
    nz = data[25][-1]
    normd = data[26][-1]
    gradd = data[27][-1]
    iter = data[28][-1]
    cacah = data[29][-1]
    biter = data[30][-1]
    split = data[31][-1]
    pert = data[32][-1]

    return evtdat, statdat, veldat, xout, yout, zout, velog, velobsout, velcalout, velpout, velsout, velpsout, type, deg2km, nx, ny, nz, normd, gradd, iter, cacah, biter, split, pert