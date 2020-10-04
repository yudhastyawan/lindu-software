class velest_cmn(object):
    def __init__(self,output,line_modelfile,line_statfile,line_quake,line_regnames,line_regcoor,line_seisfile,olat,olon,
                 rotate,coordsys,zshift,itrial,ztrial,ised,neq,nshot,isingle,iresolcalc,dmax,itopo,zmin,veladj,zadj,
                 lowveloclay,nsp,swtfac,vpvsrat,nmod,othet,xythet,zthet,vthet,stathet,nsinv,nshcor,nshfix,iuseelev,
                 iusestacorr,iturbo,icnvout,istaout,ismpout,irayout,idrvout,ialeout,idspout,irflout,irfrout,iresout,
                 delmin,ittmax,invertratio,line_velestout,line_statlist,line_hypott,line_hypo71,line_veloutsmp,
                 line_veloutray,line_veloutdrv,line_veloutale,line_veloutdspr,line_veloutrfl,line_veloutrfr,line_veloutres):
        file = open(output,'w')
        file.write(
            '******* CONTROL-FILE FOR PROGRAM  V E L E S T  (28-SEPT1993) *******'+'\n'+
            '***'+'\n'+
            '*** ( all lines starting with  *  are ignored! )'+'\n'+
            '*** ( where no filename is specified,'+'\n'+
            '***   leave the line BLANK. Do NOT delete!)'+'\n'+
            '***'+'\n'+
            '*** next line contains a title (printed on output):'+'\n'+
            'CALAVERAS area7 1.10.93 EK startmodell vers. 1.1'+'\n'+
            '***      starting model 1.1 based on Castillo and Ellsworth 1993, JGR'+'\n'+
            '***  olat       olon   icoordsystem      zshift   itrial ztrial    ised'+'\n'+
            '\t'+olat+'\t'+olon+'\t'+coordsys+'\t'+zshift+'\t'+itrial+'\t'+ztrial+'\t'+ised+'\n'+
            '***'+'\n'+
            '*** neqs   nshot   rotate'+'\n'+
            '\t'+neq+'\t'+nshot+'\t'+rotate+'\n'+
            '***'+'\n'+
            '*** isingle   iresolcalc'+'\n'+
            '\t'+isingle+'\t'+iresolcalc+'\n'+
            '***'+'\n'+
            '*** dmax    itopo    zmin     veladj    zadj   lowveloclay'+'\n'+
            '\t'+dmax+'\t'+itopo+'\t'+zmin+'\t'+veladj+'\t'+zadj+'\t'+lowveloclay+'\n'+
            '***'+'\n'+
            '*** nsp    swtfac   vpvs       nmod'+'\n'+
            '\t'+nsp+'\t'+swtfac+'\t'+vpvsrat+'\t'+nmod+'\n'+
            '***'+'\n'+
            '***   othet   xythet    zthet    vthet   stathet'+'\n'+
            '\t'+othet+'\t'+xythet+'\t'+zthet+'\t'+vthet+'\t'+stathet+'\n'+
            '***'+'\n'+
            '*** nsinv   nshcor   nshfix     iuseelev    iusestacorr'+'\n'+
            '\t'+nsinv+'\t'+nshcor+'\t'+nshfix+'\t'+iuseelev+'\t'+iusestacorr+'\n'+
            '***'+'\n'+
            '*** iturbo    icnvout   istaout   ismpout'+'\n'+
            '\t'+iturbo+'\t'+icnvout+'\t'+istaout+'\t'+ismpout+'\n'+
            '***'+'\n'+
            '*** irayout   idrvout   ialeout   idspout   irflout   irfrout   iresout'+'\n'+
            '\t'+irayout+'\t'+idrvout+'\t'+ialeout+'\t'+idspout+'\t'+irflout+'\t'+irfrout+'\t'+iresout+'\n'+
            '***'+'\n'+
            '*** delmin   ittmax   invertratio'+'\n'+
            '\t'+delmin+'\t'+ittmax+'\t'+invertratio+'\n'+
            '***'+'\n'+
            '*** Modelfile:'+'\n'+
            line_modelfile+'\n'+
            '***'+'\n'+
            '*** Stationfile:'+'\n'+
            line_statfile+'\n'+
            '***'+'\n'+
            '*** Seismofile:'+'\n'+
            line_seisfile+'\n'+
            '***'+'\n'+
            '*** File with region names:'+'\n'+
            line_regnames+'\n'+
            '***'+'\n'+
            '*** File with region coordinates:'+'\n'+
            line_regcoor+'\n'+
            '***'+'\n'+
            '*** File #1 with topo data:'+'\n'+
            ''+'\n'+
            '***'+'\n'+
            '*** File #2 with topo data:'+'\n'+
            ''+'\n'+
            '***'+'\n'+
            '*** DATA INPUT files:'+'\n'+
            '***'+'\n'+
            '*** File with Earthquake data:'+'\n'+
            line_quake+'\n'+
            '***'+'\n'+
            '*** File with Shot data:'+'\n'+
            ''+'\n'+
            '***'+'\n'+
            '*** OUTPUT files:'+'\n'+
            '***'+'\n'+
            '*** Main print output file:'+'\n'+
            line_velestout+'\n'+
            '***'+'\n'+
            '*** File with single event locations:'+'\n'+
            ''+'\n'+
            '***'+'\n'+
            '*** File with final hypocenters in *.cnv format:'+'\n'+
            line_hypott+'\n'+
            '***'+'\n'+
            '*** File with new station corrections:'+'\n'+
            line_statlist+'\n'+
            '***'+'\n'+
            '*** File with summary cards (e.g. for plotting):'+'\n'+
            line_veloutsmp+'\n'+
            '***'+'\n'+
            '*** File with raypoints:'+'\n'+
            line_veloutray+'\n'+
            '***'+'\n'+
            '*** File with derivatives:'+'\n'+
            line_veloutdrv+'\n'+
            '***'+'\n'+
            '*** File with ALEs:'+'\n'+
            line_veloutale+'\n'+
            '***'+'\n'+
            '*** File with Dirichlet spreads:'+'\n'+
            line_veloutdspr+'\n'+
            '***'+'\n'+
            '*** File with reflection points:'+'\n'+
            line_veloutrfl+'\n'+
            '***'+'\n'+
            '*** File with refraction points:'+'\n'+
            line_veloutrfr+'\n'+
            '***'+'\n'+
            '*** File with residuals:'+'\n'+
            line_veloutres+'\n'+
            '***'+'\n'+
            '******* END OF THE CONTROL-FILE FOR PROGRAM  V E L E S T  *******'+'\n'
        )
        file.close()