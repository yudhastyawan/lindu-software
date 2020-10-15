# relocfile = "D:\Aplikasi\output\hypoDD.reloc"
# phasefile = "D:\Aplikasi\HypoDD\HYPODD\examples\example1\El16.pha"
# evtfile = "D:\Aplikasi\output\event.evt"

def dd2tomo(relocfile, phasefile, evtfile):
    file = open(phasefile,'r')
    phase = file.readlines()
    for i in range(len(phase)):
        phase[i] = phase[i].split()
    file.close()

    file = open(relocfile,'r')
    reloc = file.readlines()
    for i in range(len(reloc)):
        reloc[i] = reloc[i].split()
    file.close()

    for i in range(len(phase)):
        if phase[i] != []:
            if phase[i][0] == '#':
                for j in range(len(reloc)):
                    if phase[i][-1] == reloc[j][0]:
                        phase[i][7] = reloc[j][1]
                        phase[i][8] = reloc[j][2]
                        phase[i][9] = reloc[j][3]

    file = open(evtfile,'w')
    for i in range(len(phase)):
        for j in range(len(phase[i][:])):
            file.write(
                phase[i][j]+'\t'
            )
        file.write(
            '\n'
        )
