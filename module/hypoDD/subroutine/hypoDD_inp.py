class hypoDD_inp(object):
    def __init__(self,output,dtcc,dtct,eventdatsel,stationdat,hypoDDloc,hypoDDreloc,hypoDDsta,hypoDDres,hypoDDsrc,idat,ipha,dist,obscc,obsct,istart,isolv,nset,cid,weight,vpvs,vel):
        file = open(output,'w')
        file.write(
            '* hypoDD.inp:' + '\n' +
            '*--- INPUT FILE SELECTION' + '\n' +
            '* filename of cross-corr diff. time input(blank if not available):' + '\n' +
            dtcc + '\n' +
            '* filename of catalog travel time input(blank if not available):' + '\n' +
            dtct + '\n' +
            '* filename of initial hypocenter input:' + '\n' +
            eventdatsel + '\n' +
            '* filename of station input:' + '\n' +
            stationdat + '\n' +
            '*' + '\n' +
            '*--- OUTPUT FILE SELECTION' + '\n' +
            '* filename of initial hypocenter output (if blank: output to hypoDD.loc):' + '\n' +
            hypoDDloc + '\n' +
            '* filename of relocated hypocenter output (if blank: output to hypoDD.reloc):' + '\n' +
            hypoDDreloc + '\n' +
            '* filename of station residual output (if blank: no output written):' + '\n' +
            hypoDDsta + '\n' +
            '* filename of data residual output (if blank: no output written):' + '\n' +
            hypoDDres + '\n' +
            '* filename of takeoff angle output (if blank: no output written):' + '\n' +
            hypoDDsrc + '\n' +
            '*' + '\n' +
            '*--- DATA SELECTION:' + '\n' +
            '* IDAT IPHA DIST' + '\n' +
            idat + '\t' + ipha + '\t'+ dist + '\n' +
            '*' + '\n' +
            '*--- EVENT CLUSTERING:' + '\n' +
            '* OBSCC OBSCT' + '\n' +
            obscc + '\t' + obsct + '\n' +
            '*' + '\n' +
            '*--- SOLUTION CONTROL:' + '\n' +
            '* ISTART ISOLV NSET' + '\n' +
            istart + '\t' + isolv + '\t' + nset + '\n' +
            '*' + '\n' +
            '*--- DATA WEIGHTING AND REWEIGHTING:' + '\n' +
            '* NITER WTCCP WTCCS WRCC WDCC WTCTP WTCTS WRCT WDCT DAMP' + '\n'
        )
        for i in range(weight.shape[0]):
            for j in range(weight.shape[1]):
                if j == 0:
                    file.write(
                        str(int(weight[i, j])) + '\t'
                    )
                elif int(weight[i,j]) == -9:
                    file.write(
                        str(int(weight[i,j])) + '\t'
                    )
                else:
                    file.write(
                        str(weight[i, j]) + '\t'
                    )
            file.write('\n')
        file.write(
            '*' + '\n' +
            '*--- MODEL SPECIFICATIONS:' + '\n' +
            '* NLAY RATIO' + '\n' +
            str(len(vel)) + '\t' + vpvs + '\n' +
            '* TOP:' + '\n'
        )
        for i in range(len(vel)):
            file.write(
                str(vel[i][0]) + '\t'
            )
        file.write('\n')
        file.write(
            '* VEL:' + '\n'
        )
        for i in range(len(vel)):
            file.write(
                str(vel[i][1]) + '\t'
            )
        file.write('\n')
        file.write(
            '*' + '\n' +
            '*--- CLUSTER/EVENT SELECTION:' + '\n' +
            '* CID' + '\n' +
            cid + '\n' +
            '* ID' + '\n' +
            ''
        )
        file.close()