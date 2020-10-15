#Skrip ini digunakan untuk mengkonvert data buletin BMKG ke pha

def bmkg2pha(fileinput, fileoutput):
    # membaca data dari file input dan memulai membuat file output
    file = open(fileinput, 'r')
    baris = file.readlines()
    for i in range(len(baris)):
        baris[i] = baris[i].split()
    file.close()
    file = open(fileoutput, 'w')

    # menyalin data tiap baris file input ke dalam file output
    i = 0
    event = 0
    while i < len(baris):
        if len(baris[i]) > 0 and baris[i][0] == 'EventID:':
            event = event + 1
            eventid = baris[i][1][3::]
            tahun = baris[i + 2][0].split('-')[0]
            bulan = baris[i + 2][0].split('-')[1].zfill(2)
            tanggal = baris[i + 2][0].split('-')[2].zfill(2)
            jam = baris[i + 2][1].split(':')[0].zfill(2)
            menit = baris[i + 2][1].split(':')[1].zfill(2)
            detik = (('%.1f') % float(baris[i + 2][1].split(':')[0])).zfill(4)
            lintang = (('%.2f') % float(baris[i + 2][2])).zfill(6)
            bujur = (('%.2f') % float(baris[i + 2][3])).zfill(6)
            depth = ('%.1f') % float(baris[i + 2][4])
            mag = ('%.1f') % float(baris[i + 2][5])
            unknown = '0.0'
            rms = ('%.3f') % float(baris[i + 2][10])
            time0 = float(detik) + float(menit) * 60 + float(jam) * 3600 + float(tanggal) * 24 * 3600
            file.write('#' + '\t' + tahun
                       + '\t' + bulan
                       + '\t' + tanggal
                       + '\t' + jam
                       + '\t' + menit
                       + '\t' + detik
                       + '\t' + lintang
                       + '\t' + bujur
                       + '\t' + depth
                       + '\t' + mag
                       + '\t' + unknown
                       + '\t' + unknown
                       + '\t' + rms
                       + '\t' + str(event)
                       + '\n')
        if len(baris[i]) > 0 and baris[i][0] == 'Net':
            try:
                j = 0
                while j < 1:
                    i = i + 1
                    try:
                        idSta = baris[i][1]
                        phase = baris[i][2]
                        tanggal = baris[i][3].split('-')[2]
                        jam = baris[i][4].split(':')[0]
                        menit = baris[i][4].split(':')[1]
                        detik = baris[i][4].split(':')[2]
                        time1 = float(detik) + float(menit) * 60 + float(jam) * 3600 + float(tanggal) * 24 * 3600
                        deltatime = ('%.2f') % float(time1 - time0)
                        unknown = '1.000'
                        file.write(idSta.rjust(5)
                                   + deltatime.rjust(12)
                                   + unknown.rjust(8)
                                   + phase.rjust(4)
                                   + '\n'
                                   )
                    except:
                        break
            except:
                break
        i = i + 1
    file.close()
