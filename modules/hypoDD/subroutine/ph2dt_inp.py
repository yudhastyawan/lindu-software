class ph2t_inp(object):
    def __init__(self,output,station,phase,minwght,maxdist,maxsep,maxngh,minlnk,minobs,maxobs):
        file = open(output,'w')
        file.write(
            '* ph2dt.inp'+'\n'+
            '*--- I/O FILES:'+'\n'+
            '* filename of station input:'+'\n'+
            'station.dat'+'\n'+
            '* filename of phase data input:'+'\n'+
            'phase.pha'+'\n'+
            '*--- DATA SELECTION PARAMETERS:'+'\n'+
            '* MINWGHT MAXDIST MAXSEP MAXNGH MINLNK MINOBS MAXOBS'+'\n'+'\t'+
            minwght+'\t'+maxdist+'\t'+maxsep+'\t'+maxngh+'\t'+minlnk+'\t'+minobs+'\t'+maxobs+'\n'+''
        )
        file.close()