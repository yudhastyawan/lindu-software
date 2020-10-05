!*********************************************************************************************
!*  Program name : Hypo_GeigerAD
!*  Function     : Solve Normal Equation using adaptive damping method.
!* 
!*  Coordinate system:
!*                 Cartecian: North  (+), East  (+), Downward (+)
!*
!*  Velocity Structure:
!*				   Up to 6 horizontal homogeneous layers
!*
!*  Units:
!*                 Length: km, Time: second
!*
!*                 --------------------------------------------------------------------
!* Version History:Version     1.0
!*                 Date         January 15, 2005
!*                 Author       K. Nishi
!*                 Contents     Created	by extracting Geiger method part from Hypo_Fermat and
!*                              modified.
!*                 --------------------------------------------------------------------
!*
!*
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!*******************************************************************
! Main program
      common /weight/ wp(50),ws(50),w(50),wratio
 
	  wratio=0.7  ! PîgÇ…ëŒÇ∑ÇÈSîgÇÃèdÇ›
!--------------------------------------------------------------------
! Output File to write Results
      open (8,file='Results.dat',access='sequential',status='unknown')
!--------------------------------------------------------------------
!--------------------------------------------------------------------
! Station coordinates
      open (10,file='station.dat',access='sequential',status='old')
	  call get_station
!--------------------------------------------------------------------
!--------------------------------------------------------------------
! Velocity Structure
      open (11,file='velocity.dat',access='sequential',status='old')
	  call get_velocity
!--------------------------------------------------------------------
!--------------------------------------------------------------------
! Ariival Time Data	file open
      open (7,file='arrival.dat',access='sequential',status='old')
!--------------------------------------------------------------------
      write(8,40)
   40 format(1h ,/'Hypocenter')

	  i1=0
   10 continue
      i1=i1+1 
!--------------------------------------------------------------------
! Read Arrival Time Data
      call read_arrival(istop)
      if(istop.eq.1) goto 1000
!--------------------------------------------------------------------
! Initial Hypo
      call get_initial(x0,y0,z0,t0)
!--------------------------------------------------------------------
! Geiger
      call Geiger(x0,y0,z0,t0,xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf)
  450 continue
!--------------------------------------------------------------------
! Write the results
	  call results(xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf)
  950 continue
!--------------------------------------------------------------------
!      read(*,77) ijk
      goto 10
 1000 continue
      close (8)
      stop  
!**** END OF MAIN PROGRAM ***** 
      end 
!********************************************************************
!********************************************************************
      subroutine results(xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf)
      common /arvdata/ ndata,iyear,imonth,iday,ihour,imini,st_name,p(50),pol,accp,s(50),accs
      common /station/nst,StList(50),stx(50),sty(50),stz(50)
      common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      character*4 StList,st_name(50),pol(50),accp(50),accs(50)
  	  real*8 c,d,dd

       write(8,100) iyear,imonth,iday,ihour,imini
	   write(*,100)	iyear,imonth,iday,ihour,imini
       write(8,110)
	   write(*,110)
       write(8,120)	xf,dxf
	   write(*,120) xf,dxf
       write(8,130)	yf,dyf
	   write(*,130) yf,dyf
       write(8,140)	zf,dzf
	   write(*,140) zf,dzf
       write(8,150)	tf,dtf
	   write(*,150) tf,dtf
	   write(8,155) rms
	   write(*,155) rms
!		   	  write(*,62) iyear,imonth,iday,ihour,imini,xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf
!	          write(8,62) iyear,imonth,iday,ihour,imini,xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf
      write(*,65) 
      write(8,65)
 	  write(8,160)
	  write(*,160)
  do 200 i=1,nps
		j=numst(i)
		cal=c(i,5)+ttobs(i)
		if(i.gt.np) goto 180
		write(8,170) StList(j),ttobs(i),cal,-c(i,5)
        write(*,170) StList(j),ttobs(i),cal,-c(i,5)
		goto 200
	 180 continue
         write(8,190) StList(j),ttobs(i),cal,-c(i,5)
		 write(*,190) StList(j),ttobs(i),cal,-c(i,5)
     200 continue
		    write(8,65)
            write(8,65)
			write(*,65)
			write(*,65)
 !--------------------------------------------------------------------
! Format
   40 format(1h ,/'Hypocenter')
   50 format(1h ,5i2,1x,'(',3f7.3,')',2x,'ot rms:',2f8.3)
   62 format(1h ,5i2,1x,'(',3f7.3,')',2x,'ot rms:',6f8.3,'   Geiger')
   65 format(1h ,'')
   77 format(i1)
  100 format(1h , 'Date ',3i3,3x,'Time ',i2,':',i2)
  110 format(1h ,4x,'Focal Element   Probable Error')
  120 format(1h ,4x,'X',1x,f7.3,8x,f7.3)
  130 format(1h ,4x,'Y',1x,f7.3,8x,f7.3)
  140 format(1h ,4x,'Z',1x,f7.3,8x,f7.3)    
  150 format(1h ,4x,'T',1x,f7.3,8x,f7.3)
  155 format(1h ,'Travel time residual rms=',f5.3,'sec.')
  160 format(1h ,' ST      P       S      Cal    (Obs-Cal)')
  170 format(1h ,a4,2x,f7.3,9x,f7.3,2x,f7.3)
  190 format(1h ,a4,10x,f7.3,1x,f7.3,2x,f7.3)
!--------------------------------------------------------------------
		return
		end
!********************************************************************
      subroutine get_initial(x0,y0,z0,t0)
!-----------------------------------------------------------------
	  common /station/nst,StList(50),stx(50),sty(50),stz(50)
	  common /arvdata/ ndata,iyear,imonth,iday,ihour,imini,st_name,p(50),pol,accp,s(50),accs
	  character*4 StList,st_name(50)
	  character*4 pol(50),accp(50),accs(50)	

	  pmin=99.0
	  do 10 i=1,nst
				if(p(i).lt.pmin) then
						pmin=p(i)
						min=i
				end if
  10  continue
		
	  x0=stx(min)+0.1
	  y0=sty(min)+0.1
	  z0=stz(min)+1.0
	  t0=pmin-2.0
	  write(*,20) x0,y0,z0,t0
  20  format(' Initial:'4f10.3)
      return
	  end
!********************************************************************                                             
       subroutine read_arrival(istop)
!      read arrival time data
!--------------------------------------------------------------------
	   common /station/nst,StList(50),stx(50),sty(50),stz(50)
	   common /arvdata/ ndata,iyear,imonth,iday,ihour,imini,st_name,p(50),pol,accp,s(50),accs
       common /weight/ wp(50),ws(50),w(50),wratio
	   character*4 StList,st_name(50),st_namein
	   character*4 pol(50),polin,accp(50),accpin,accs(50),accsin	

	   istop=0

	   do 3 i=1,nst
			p(i)=99.990
			s(i)=99.990
     3 continue
	 
	10 continue
			read(7,20,end=100) iyearin,imonthin,idayin,ihourin,iminiin,st_namein,pin,polin,accpin,ssin,accsin
			if(iyearin.eq.0) goto 30
			if(imonthin.eq.99) goto 100

			iyear=iyearin
			imonth=imonthin
			iday=idayin
			ihour=ihourin
			imini=iminiin
			do 5 i=1,nst
				if(st_namein.eq.StList(i)) then
					p(i)=pin
					pol(i)=polin
					accp(i)=accpin
					if(accpin.eq."I".or.accpin.eq."i") then
					     wp(i)=1.0
                    else
					     wp(i)=0.7
                    end if
					s(i)=ssin
					accs(i)=accsin
					if(accsin.eq."I".or.accsin.eq."i") then
					     ws(i)=1.0*wratio
                    else
					     ws(i)=0.7*wratio
                    end if
				end if
		    5 continue
	   goto 10
	30 continue
	   do 50 i=1,nst
	        if(p(i).eq.99.99) goto 50
			write(*,60) iyear,imonth,iday,ihour,imini,StList(i),p(i),pol(i),accp(i),s(i),accs(i)
!			write(8,60) iyear,imonth,iday,ihour,imini,StList(i),p(i),pol(i),accp(i),s(i),accs(i)

		!	read(*,77) ijk

	50 continue
	   write(*,70)
!--------------------------------------------------------------------
	   goto 150
   100 continue
       write(*,120)
	   istop=1
       close (7)
   150 continue
!	   read(*,160) ijk
 	   return
!--------------------------------------------------------------------	 
! Format	   
	20 format(5i2,1x,a3,1x,f6.3,1x,a1,1x,a1,1x,f6.3,1x,a1)
	60 format(1h ,5i2,1x,a3,1x,f6.3,1x,a1,1x,a1,1x,f6.3,1x,a1)
	70 format(1h ,'')
   120 format(1h ,' End of data ')
   160 format(i1)
!--------------------------------------------------------------------
	   end
!*************************************************************************************
       subroutine get_station
! Read Station name and coordinates from station.dat file
!------------------------------------------------------
      common /station/nst,StList(50),stx(50),sty(50),stz(50)
      character*4 StList
!--------------------------------------------------------
! Read station
	  read(10,240) nst
      do 250 i=1,nst
             read(10,245) StList(i),stx(i),sty(i),stz(i)
      250 continue
! Write station
      write(8,290) nst
      do 300 i=1,nst
             write(8,295) StList(i),stx(i),sty(i),stz(i)
      300 continue
!--------------------------------------------------------
      close (10)
	  return
!--------------------------------------------------------------------
! Format
  240 format(i2)
  245 format(a3,2x,3f10.3)
  290 format('nst    :',i2/'Station List')
  295 format(1h ,2x,a3,1x,3f8.3)
!--------------------------------------------------------------------
       end
!*************************************************************************************
       subroutine get_velocity
! Read velocity structure from velocity.dat file
! Calculate velocity coeeficient
!------------------------------------------------------
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
!------------------------------------------------------
      dimension zLayer(5)	
! Read parameters of layered velocity structure 
      read (11,10) nZLayer
	  write(8,12) nZLayer
	  if(nZLayer.eq.1) then
				read(11,10) idumy
				goto 18
	  end if
      read(11,17) (zLayer(i),i=1,nZLayer-1)
	  write(8,20) (zLayer(i),i=1,nZLayer-1)
	  zL1=zLayer(1)
      zL2=zLayer(2)
      zL3=zLayer(3)
      zL4=zLayer(4)
      zL5=zLayer(5)
   18 continue
	  do 25 ips=1,2
	       read(11,27) (VL(j,ips),j=1,nZLayer)
      25 continue
	  write(8,28) (VL(i,1),i=1,nZLayer)
	  write(8,29) (VL(i,2),i=1,nZLayer)
!------------------------------------------------------
! Calculate velocity coefficient
       do 600 ips=1,2
	        call velocitycoefficient(ips)
	   600 continue
!--------------------------------------------------------------------
      close (11)
	  return
!--------------------------------------------------------------------
! Format
   10 format(15x,i4)
   12 format('nZLayer: ',i1)
   17 format(15x,5f8.3)
   20 format('zLayer : ',5f8.3)
   27 format(15x,6f8.3)
   28 format('Vp     : ', 6f8.3)
   29 format('Vs     : ', 6f8.3)
!--------------------------------------------------------------------
       end
!********************************************************************

!********************************************************************
!********** calculation of velocity coefficient **********
      subroutine velocitycoefficient(ips)
!********************************************************************
 	  common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
      dimension v12(2),v13(2),v14(2),v15(2),v16(2),v23(2),v24(2),v25(2),v26(2),  &
                v34(2),v35(2),v36(2),v45(2),v46(2),v56(2)
 
      if(nZLayer.eq.1) goto 20
      do 10 ips=1,2
           V12(ips) = VL(2,ips) * VL(2,ips) - VL(1,ips) * VL(1,ips)
           C12(ips) = (VL(2,ips) / VL(1,ips) - VL(1,ips) / VL(2,ips)) / SQRt(V12(ips))
           if(nZLayer.eq.2) goto 10

           V13(ips) = VL(3,ips) * VL(3,ips) - VL(1,ips) * VL(1,ips)
           V23(ips) = VL(3,ips) * VL(3,ips) - VL(2,ips) * VL(2,ips)
           C13(ips) = (VL(3,ips) / VL(1,ips) - VL(1,ips) / VL(3,ips)) / SQRt(V13(ips))
           C23(ips) = (VL(3,ips) / VL(2,ips) - VL(2,ips) / VL(3,ips)) / SQRt(V23(ips))
           if(nZLayer.eq.3) goto 10

           V14(ips) = VL(4,ips) * VL(4,ips) - VL(1,ips) * VL(1,ips)
           V24(ips) = VL(4,ips) * VL(4,ips) - VL(2,ips) * VL(2,ips)
           V34(ips) = VL(4,ips) * VL(4,ips) - VL(3,ips) * VL(3,ips)
           C14(ips) = (VL(4,ips) / VL(1,ips) - VL(1,ips) / VL(4,ips)) / SQRt(V14(ips))
           C24(ips) = (VL(4,ips) / VL(2,ips) - VL(2,ips) / VL(4,ips)) / SQRt(V24(ips))
           C34(ips) = (VL(4,ips) / VL(3,ips) - VL(3,ips) / VL(4,ips)) / SQRt(V34(ips))
           if(nZLayer.eq.4) goto 10

           V15(ips) = VL(5,ips) * VL(5,ips) - VL(1,ips) * VL(1,ips)
           V25(ips) = VL(5,ips) * VL(5,ips) - VL(2,ips) * VL(2,ips)
           V35(ips) = VL(5,ips) * VL(5,ips) - VL(3,ips) * VL(3,ips)
           V45(ips) = VL(5,ips) * VL(5,ips) - VL(4,ips) * VL(4,ips)
           C15(ips) = (VL(5,ips) / VL(1,ips) - VL(1,ips) / VL(5,ips)) / SQRt(V15(ips))
           C25(ips) = (VL(5,ips) / VL(2,ips) - VL(2,ips) / VL(5,ips)) / SQRt(V25(ips))
           C35(ips) = (VL(5,ips) / VL(3,ips) - VL(3,ips) / VL(5,ips)) / SQRt(V35(ips))
           C45(ips) = (VL(5,ips) / VL(4,ips) - VL(4,ips) / VL(5,ips)) / SQRt(V45(ips))
           if(nZlayer.eq.5) goto 10

           V16(ips) = VL(6,ips) * VL(6,ips) - VL(1,ips) * VL(1,ips)
           V26(ips) = VL(6,ips) * VL(6,ips) - VL(2,ips) * VL(2,ips)
           V36(ips) = VL(6,ips) * VL(6,ips) - VL(3,ips) * VL(3,ips)
           V46(ips) = VL(6,ips) * VL(6,ips) - VL(4,ips) * VL(4,ips)
           V56(ips) = VL(6,ips) * VL(6,ips) - VL(5,ips) * VL(5,ips)
           C16(ips) = (VL(6,ips) / VL(1,ips) - VL(1,ips) / VL(6,ips)) / SQRt(V16(ips))
           C26(ips) = (VL(6,ips) / VL(2,ips) - VL(2,ips) / VL(6,ips)) / SQRt(V26(ips))
           C36(ips) = (VL(6,ips) / VL(3,ips) - VL(3,ips) / VL(6,ips)) / SQRt(V36(ips))
           C46(ips) = (VL(6,ips) / VL(4,ips) - VL(4,ips) / VL(6,ips)) / SQRt(V46(ips))
           C56(ips) = (VL(6,ips) / VL(5,ips) - VL(5,ips) / VL(6,ips)) / SQRt(V56(ips))

   10 continue
   20 continue
      return
      end
!********************************************************************

!********************************************************************
!********** Travel time for T10 **********
      subroutine calT10(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      t=dist/VL(1,ips)
      return
      end
!********************************************************************
!********** Travel time for T11 **********
      subroutine calT11(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(2,ips))
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL1-z1)*tan(TH1)

      if ((xx0+xx1).gt.delt) then
          t=99.9
      else
          t = delt / VL(2,ips) + (2.0*zL1-zst-z1) * C12(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T12 **********
      subroutine calT12(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(3,ips))
      TH2=asin(VL(2,ips)/VL(3,ips))
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL1-z1)*tan(TH1)
      xx2=(zL2-zL1)*tan(TH2)
      delt0=xx0+xx1+2.0*xx2
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(3,ips)+2.0*(zL2-zL1)*C23(ips)+(2.0*zL1-zst-z1)*C13(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T13 **********
      subroutine calT13(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(4,ips))
      TH2=asin(VL(2,ips)/VL(4,ips))
      TH3=asin(VL(3,ips)/VL(4,ips))
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL1-z1)*tan(TH1)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      delt0=xx0+xx1+2.0*xx2+2.0*xx3
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(4,ips)+2.0*(zL3-zL2)*C34(ips)+2.0*(zL2-zL1)*C24(ips)+   &
            (2.0*zL1-zst-z1)*C14(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T14 **********
      subroutine calT14(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(5,ips))
      TH2=asin(VL(2,ips)/VL(5,ips))
      TH3=asin(VL(3,ips)/VL(5,ips))
      TH4=asin(VL(4,ips)/VL(5,ips))
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL1-z1)*tan(TH1)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      delt0=xx0+xx1+2.0*xx2+2.0*xx3+2.0*xx4
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(5,ips)+2.0*(zL4-zL3)*C45(ips)+   &
          2.0*(zL3-zL2)*C35(ips)+2.0*(zL2-zL1)*C25(ips)+   &
          (2.0*zL1-zst-z1)*C15(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T15 **********
      subroutine calT15(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(6,ips))
      TH2=asin(VL(2,ips)/VL(6,ips))
      TH3=asin(VL(3,ips)/VL(6,ips))
      TH4=asin(VL(4,ips)/VL(6,ips))
      TH5=asin(VL(5,ips)/VL(6,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL1-z1)*tan(TH1)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      xx5=(zL5-zL4)*tan(TH5)
      delt0=xx0+xx1+2.0*xx2+2.0*xx3+2.0*xx4+2.0*xx5
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(6,ips)+2.0*(zL5-zL4)*C56(ips)+   &
            2.0*(zL4-zL3)*C46(ips)+2.0*(zL3-zL2)*C36(ips)+   &
            2.0*(zL2-zL1)*C26(ips)+(2.0*zL1-zst-z1)*C16(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T21 **********
      subroutine calT21(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(3,ips))
      TH2=asin(VL(2,ips)/VL(3,ips))     
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-z1)*tan(TH2)
      xx2=(zL2-zL1)*tan(TH2)
      delt0=xx0+xx1+xx2
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(3,ips)+(zL2-z1)*C23(ips)+(zL2-zL1)*C23(ips)+(zL1-zst)*C13(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T22 **********
      subroutine calT22(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(4,ips))
      TH2=asin(VL(2,ips)/VL(4,ips))
      TH3=asin(VL(3,ips)/VL(4,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-z1)*tan(TH2)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      delt0=xx0+xx1+xx2+2.0*xx3
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(4,ips)+2.0*(zL3-zL2)*C34(ips)+(zL2-z1)*C24(ips)+   &
            (zL2-zL1)*C24(ips)+(zL1-zst)*C14(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T23 **********
      subroutine calT23(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(5,ips))
      TH2=asin(VL(2,ips)/VL(5,ips))
      TH3=asin(VL(3,ips)/VL(5,ips))
      TH4=asin(VL(4,ips)/VL(5,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-z1)*tan(TH2)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      delt0=xx0+xx1+xx2+2.0*(xx3+xx4)
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(5,ips)+2.0*(zL4-zL3)*C45(ips)+   &
            2.0*(zL3-zL2)*C35(ips)+(zL2-z1)*C25(ips)+   &
            (zL2-zL1)*C25(ips)+(zL1-zst)*C15(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T24 **********
      subroutine calT24(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(6,ips))
      TH2=asin(VL(2,ips)/VL(6,ips))
      TH3=asin(VL(3,ips)/VL(6,ips))
      TH4=asin(VL(4,ips)/VL(6,ips))
      TH5=asin(VL(5,ips)/VL(6,ips))
      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-z1)*tan(TH2)
      xx2=(zL2-zL1)*tan(TH2)
      xx3=(zL3-zL2)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      xx5=(zL5-zL4)*tan(TH5)
      delt0=xx0+xx1+xx2+2.0*(xx3+xx4+xx5)
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(6,ips)+2.0*(zL5-zL4)*C56(ips)+  &
            2.0*(zL4-zL3)*C46(ips)+2.0*(zL3-zL2)*C36(ips)+   &
            (zL2-z1)*C26(ips)+(zL2-zL1)*C26(ips)+   &
            (zL1-zst)*C16(ips)
       end if
      return
      end
!********************************************************************
!********** Travel time for T31 **********
      subroutine calT31(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(4,ips))
      TH2=asin(VL(2,ips)/VL(4,ips))
      TH3=asin(VL(3,ips)/VL(4,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL3-z1)*tan(TH3)
      delt0=xx0+xx1+xx2+xx3
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(4,ips)+(zL3-z1)*C34(ips)+(zL3-zL2)*C34(ips)+   &
            (zL2-zL1)*C24(ips)+(zL1-zst)*C14(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T32 **********
      subroutine calT32(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(5,ips))
      TH2=asin(VL(2,ips)/VL(5,ips))
      TH3=asin(VL(3,ips)/VL(5,ips))
      TH4=asin(VL(4,ips)/VL(5,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL3-z1)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      delt0=xx0+xx1+xx2+xx3+2.0*xx4
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(5,ips)+(zL3-z1)*C35(ips)+(zL3-zL2)*C35(ips)+   &
            (zL2-zL1)*C25(ips)+(zL1-zst)*C15(ips)+2.0*(zL4-zL3)*C45(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T33 **********
      subroutine calT33(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(6,ips))
      TH2=asin(VL(2,ips)/VL(6,ips))
      TH3=asin(VL(3,ips)/VL(6,ips))
      TH4=asin(VL(4,ips)/VL(6,ips))
      TH5=asin(VL(5,ips)/VL(6,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL3-z1)*tan(TH3)
      xx4=(zL4-zL3)*tan(TH4)
      xx5=(zL5-zL4)*tan(TH5)

      delt0=xx0+xx1+xx2+xx3+2.0*(xx4+xx5)
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(6,ips)+(zL3-z1)*C36(ips)+(zL3-zL2)*C36(ips)+   &
            (zL2-zL1)*C26(ips)+(zL1-zst)*C16(ips)+   &
            2.0*(zL4-zL3)*C46(ips)+2.0*(zL5-zL4)*C56(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T41 **********
      subroutine calT41(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(5,ips))
      TH2=asin(VL(2,ips)/VL(5,ips))
      TH3=asin(VL(3,ips)/VL(5,ips))
      TH4=asin(VL(4,ips)/VL(5,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL4-zL3)*tan(TH4)
      xx4=(zL4-z1)*tan(TH4)
      delt0=xx0+xx1+xx2+xx3+xx4
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(5,ips)+(zL4-z1)*C45(ips)+(zL4-zL3)*C45(ips)+   &
            (zL3-zL2)*C35(ips)+(zL2-zL1)*C25(ips)+(zL1-zst)*C15(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T42 **********
      subroutine calT42(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(6,ips))
      TH2=asin(VL(2,ips)/VL(6,ips))
      TH3=asin(VL(3,ips)/VL(6,ips))
      TH4=asin(VL(4,ips)/VL(6,ips))
      TH5=asin(VL(5,ips)/VL(6,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL4-zL3)*tan(TH4)
      xx4=(zL4-z1)*tan(TH4)
      xx5=(zL5-zL4)*tan(TH5)
      delt0=xx0+xx1+xx2+xx3+xx4+2.0*xx5
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(6,ips)+(zL4-z1)*C46(ips)+(zL4-zL3)*C46(ips)+   &
            (zL3-zL2)*C36(ips)+(zL2-zL1)*C26(ips)+   &
            (zL1-zst)*C16(ips)+2.0*(zL5-zL4)*C56(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T51 **********
      subroutine calT51(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                   c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)

      TH1=asin(VL(1,ips)/VL(6,ips))
      TH2=asin(VL(2,ips)/VL(6,ips))
      TH3=asin(VL(3,ips)/VL(6,ips))
      TH4=asin(VL(4,ips)/VL(6,ips))
      TH5=asin(VL(5,ips)/VL(6,ips))

      xx0=(zL1-zst)*tan(TH1)
      xx1=(zL2-zL1)*tan(TH2)
      xx2=(zL3-zL2)*tan(TH3)
      xx3=(zL4-zL3)*tan(TH4)
      xx4=(zL5-zL4)*tan(TH5)
      xx5=(zL5-z1)*tan(TH5)
      delt0=xx0+xx1+xx2+xx3+xx4+xx5
      if (delt0.gt.delt) then
          t=99.9
      else
          t=delt/VL(6,ips)+(zL5-z1)*C56(ips)+(zL5-zL4)*C56(ips)+   &
            (zL4-zL3)*C46(ips)+(zL3-zL2)*C36(ips)+   &
            (zL2-zL1)*C26(ips)+(zL1-zst)*C16(ips)
      end if
      return
      end
!********************************************************************
!********** Travel time for T20 **********
      subroutine calT20(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
	  common/rayparm/pp,cos2
      external FL2
      real*8 Bisec,FL2,sinth2,th2,sinth1,th1,thed,pp,cos2
 
      eps=1.0E-13
      thed=1.0-eps
      sinth2=Bisec(FL2,0.0D0,thed,eps)
      th2=dasin(sinth2)
      sinth1=(VL(1,ips)/VL(2,ips))*sinth2
      th1=dasin(sinth1)
	  pp=sinth2/VL(2,ips)
	  cos2=dcos(th2)
      
      r1=(zL1-zst)/dcos(th1)
      r2=(z1-zL1)/dcos(th2)
      t=r1/VL(1,ips)+r2/VL(2,ips)
      return
      end
!********************************************************************
!********** Travel time for T30 **********
      subroutine calT30(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
	  common/rayparm/pp,cos2
      external FL3
      real*8 Bisec,FL3,sinth3,th3,sinth2,th2,sinth1,th1,thed,pp,cos2
 
      eps=1.0E-13
      thed=1.0-eps
      sinth3=Bisec(FL3,0.0D0,thed,eps)
      th3=dasin(sinth3)
 
      sinth2=(VL(2,ips)/VL(3,ips))*sinth3
      th2=dasin(sinth2)
      
      sinth1=(VL(1,ips)/VL(3,ips))*sinth3
      th1=dasin(sinth1)
      pp=sinth3/VL(3,ips)
	  cos2=dcos(th3)

      r1=(zL1-zst)/dcos(th1)
      r2=(zL2-zL1)/dcos(th2)
      r3=(z1-zL2)/dcos(th3)
      t=r1/VL(1,ips)+r2/VL(2,ips)+r3/VL(3,ips)
      return
      end
!********************************************************************
!********** Travel time for T40 **********
      subroutine calT40(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      external FL4
      real*8 Bisec,FL4,sinth4,th4,sinth3,th3,sinth2,th2,sinth1,th1,thed,pp,cos2
 
      eps=1.0E-13
      thed=1.0-eps
      sinth4=Bisec(FL4,0.0D0,thed,eps)
      th4=dasin(sinth4)

      sinth3=(VL(3,ips)/VL(4,ips))*sinth4
      th3=dasin(sinth3)

      sinth2=(VL(2,ips)/VL(4,ips))*sinth4
      th2=dasin(sinth2)

      sinth1=(VL(1,ips)/VL(4,ips))*sinth4
      th1=dasin(sinth1)

	  pp=sinth4/VL(4,ips)
	  cos2=dcos(th4)

      r1=(zL1-zst)/dcos(th1)
      r2=(zL2-zL1)/dcos(th2)
      r3=(zL3-zL2)/dcos(th3)
      r4=(z1-zL3)/dcos(th4)
      t=r1/VL(1,ips)+r2/VL(2,ips)+r3/VL(3,ips)+r4/VL(4,ips)
      return
      end
!********************************************************************
!********** Travel time for T50 **********
      subroutine calT50(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      external FL5
      real*8 Bisec,FL5
      real*8 sinth5,th5,sinth4,th4,sinth3,th3,sinth2,th2,sinth1,th1,thed,pp,cos2

      eps=1.0E-13
      thed=1.0-eps
      sinth5=Bisec(FL5,0.0D0,thed,eps)
      th5=dasin(sinth5)

      sinth4=(VL(4,ips)/VL(5,ips))*sinth5
      th4=dasin(sinth4)

      sinth3=(VL(3,ips)/VL(5,ips))*sinth5
      th3=dasin(sinth3)

      sinth2=(VL(2,ips)/VL(5,ips))*sinth5
      th2=dasin(sinth2)

      sinth1=(VL(1,ips)/VL(5,ips))*sinth5
      th1=dasin(sinth1)

      pp=sinth5/VL(5,ips)
	  cos2=dcos(th5)

	  r1=(zL1-zst)/dcos(th1)
      r2=(zL2-zL1)/dcos(th2)
      r3=(zL3-zL2)/dcos(th3)
      r4=(zL4-zL3)/dcos(th4)
      r5=(z1-zL4)/dcos(th5)
      t=r1/VL(1,ips)+r2/VL(2,ips)+r3/VL(3,ips)+r4/VL(4,ips)+r5/VL(5,ips)
      return
      end
!********************************************************************
!********** Travel time for T60 **********
      subroutine calT60(t)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      external FL6
      real*8 Bisec,FL6
      real*8 sinth6,th6,sinth5,th5,sinth4,th4,sinth3,th3,sinth2,th2,sinth1,th1,thed,pp,cos2

      eps=1.0E-13
      thed=1.0-eps
      sinth6=Bisec(FL6,0.0D0,thed,eps)
      th6=dasin(sinth6)

      sinth5=(VL(5,ips)/VL(6,ips))*sinth6
      th5=dasin(sinth5)

      sinth4=(VL(4,ips)/VL(6,ips))*sinth6
      th4=dasin(sinth4)

      sinth3=(VL(3,ips)/VL(6,ips))*sinth6
      th3=dasin(sinth3)

      sinth2=(VL(2,ips)/VL(6,ips))*sinth6
      th2=dasin(sinth2)
      
      sinth1=(VL(1,ips)/VL(6,ips))*sinth6
      th1=dasin(sinth1)

	  pp=sinth6/VL(6,ips)
	  cos2=dcos(th6)

      
      r1=(zL1-zst)/dcos(th1)
      r2=(zL2-zL1)/dcos(th2)
      r3=(zL3-zL2)/dcos(th3)
      r4=(zL4-zL3)/dcos(th4)
      r5=(zL5-zL4)/dcos(th5)
      r6=(z1-zL5)/dcos(th6)
      t=r1/VL(1,ips)+r2/VL(2,ips)+r3/VL(3,ips)+r4/VL(4,ips)+r5/VL(5,ips)+r6/VL(6,ips)
      return
      end
!********************************************************************
!********************************************************************
      real*8 function FL2(s)
      real*8 s

      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      FL2=delt-((zL1-zst)*VL(1,ips)*s)/dsqrt(VL(2,ips)**2-VL(1,ips)**2*s**2)   &
              -((z1-zL1)*s)/dsqrt(1.0-s**2)
      end
!********************************************************************
!********************************************************************
      real*8 function FL3(s)
      real*8 s

      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      FL3=delt-((zL1-zst)*VL(1,ips)*s)/dsqrt(VL(3,ips)**2-VL(1,ips)**2*s**2)   &
              -((zL2-zL1)*VL(2,ips)*s)/dsqrt(VL(3,ips)**2-VL(2,ips)**2*s**2)   &
              -((z1-zL2)*s)/dsqrt(1.0-s**2)
      end
!********************************************************************
!********************************************************************
      real*8 function FL4(s)
      real*8 s

      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      FL4=delt-((zL1-zst)*VL(1,ips)*s)/dsqrt(VL(4,ips)**2-VL(1,ips)**2*s**2)   &
              -((zL2-zL1)*VL(2,ips)*s)/dsqrt(VL(4,ips)**2-VL(2,ips)**2*s**2)   &
              -((zL3-zL2)*VL(3,ips)*s)/dsqrt(VL(4,ips)**2-VL(3,ips)**2*s**2)   &
              -((z1-zL3)*s)/dsqrt(1.0-s**2)
      end
!********************************************************************
!********************************************************************
      real*8 function FL5(s)
      real*8 s

      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
 
      FL5=delt-((zL1-zst)*VL(1,ips)*s)/dsqrt(VL(5,ips)**2-VL(1,ips)**2*s**2)   &
              -((zL2-zL1)*VL(2,ips)*s)/dsqrt(VL(5,ips)**2-VL(2,ips)**2*s**2)   &
              -((zL3-zL2)*VL(3,ips)*s)/dsqrt(VL(5,ips)**2-VL(3,ips)**2*s**2)   &
              -((zL4-zL3)*VL(4,ips)*s)/dsqrt(VL(5,ips)**2-VL(4,ips)**2*s**2)   &
              -((z1-zL4)*s)/dsqrt(1.0-s**2)
      end
!********************************************************************
!********************************************************************
      real*8 function FL6(s)
      real*8 s

      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
 
      FL6=delt-((zL1-zst)*VL(1,ips)*s)/dsqrt(VL(6,ips)**2-VL(1,ips)**2*s**2)   &
              -((zL2-zL1)*VL(2,ips)*s)/dsqrt(VL(6,ips)**2-VL(2,ips)**2*s**2)   &
              -((zL3-zL2)*VL(3,ips)*s)/dsqrt(VL(6,ips)**2-VL(3,ips)**2*s**2)   &
              -((zL4-zL3)*VL(4,ips)*s)/dsqrt(VL(6,ips)**2-VL(4,ips)**2*s**2)   &
              -((zL5-zL4)*VL(5,ips)*s)/dsqrt(VL(6,ips)**2-VL(5,ips)**2*s**2)   &
              -((z1-zL5)*s)/dsqrt(1.0-s**2)
      end
!********************************************************************
!********************************************************************
!********** Bisec Method **********
      real*8 function Bisec(func,a,b,eps)
      real*8 func,a,b,x1,x2,y,xm

      x1=a
      x2=b
      y=func(x1)
   10 continue
      xm=(x1+x2)/2.0
      if(y*func(xm).gt.0.0) then
           x1=xm
      else
           x2=xm
      end if
      if(abs(x1-x2).ge.eps) goto 10
      Bisec=xm
      end

!******************************************************************
!******************************************************************
!***********************************************************************************
!***********************************************************************************
!******************************************************************
!******************************************************************
      subroutine Geiger(x0,y0,z0,t0,xf,yf,zf,tf,rms,dxf,dyf,dzf,dtf)
      common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
   	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
	  real*8 c,d,dd
	  dimension sigma(4),proer(4)

! parameter setting
      damping=0.001
	  maxitaration=50
	  dx=0.001
	  dy=0.001
	  dz=0.001
	  dt=0.001
	  
	  L=0
	  nsol=0
	  call makePSarray
	  call getMatrix(x0,y0,z0,t0)
	  call calRMS(rms,sig)
			  
   10 continue
	  call normalEQ
	  call solution(nsol)
	       exrms=rms ; exx0=x0 ; exy0=y0 ; exz0=z0 ; ext0=t0
		   exdamping=damping
	!	   write(*,*) d(1,5),d(2,5),d(3,5),d(4,5)
		   x0=x0+d(1,5)	; y0=y0+d(2,5) ; z0=z0+d(3,5) ; t0=t0+d(4,5)
	  call getMatrix(x0,y0,z0,t0)
	  call calRMS(rms,sig)

	       write(*,77) L,x0,y0,z0,t0,rms,damping
		   77 format(1h ,'L,x0,y0,z0,t0,rms,damping',i2,6f8.3)
!		   read(*,78) ijk
		   78 format(i1)

		   if(rms.gt.exrms) then
		        x0=exx0	; y0=exy0 ;	z0=exz0	; t0=ext0
				exdamping=damping
				damping=4.0*damping
				L=L+1
		        if(L.gt.maxitaration) goto 100
				goto 10
           end if
		   exrms=rms ; exx0=x0 ; exy0=y0 ; exz0=z0 ; ext0=t0
		   exdamping=damping
		   damping=0.6*damping
		   L=L+1
		   ddx=abs(d(1,5)) ; ddy=abs(d(2,5)) ; ddz=abs(d(3,5)) ; ddt=abs(d(4,5))
		   if(ddx.lt.dx.and.ddy.lt.dy.and.ddz.lt.dz.and.ddt.lt.dt) goto 100
		   if(L.gt.maxitaration) goto 100
		   goto 10
  100 continue
	    xf=x0;yf=y0;zf=z0;tf=t0 ;resf=rms
		write(*,77) L,x0,y0,z0,t0,rms,damping
!-----------------------------------------------------------------
		if(nps.le.4) goto 300

	!		nsol=1
			do 200 i=1,4
				do 150 j=1,4
					dd(j,5)=0.0
					if(i.eq.j) then
						dd(j,5)=1.0
					end if
				150 continue
				call solution(nsol)
				sigma(i)=sig*d(i,5)
				sigma(i)=abs(sigma(i))
				proer(i)=0.6745*sqrt(sigma(i))
			200 continue
			dxf=proer(1)
			dyf=proer(2)
			dzf=proer(3)
			dtf=proer(4)
  300 continue
	  return
	  end
!******************************************************************
      subroutine calRMS(rms,sig)
      common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common /weight/ wp(50),ws(50),w(50),wratio
  	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
	  real*8 c,d,dd

	  rms1=0.0
	  do 10 i=1,nps
	       rms1=rms1+(c(i,5)*w(i))**2
   10 continue
	  rms=sqrt(rms1/(nps-1))
	  if(nps.le.4) goto 20
	  sig=rms1/(nps-4)	  
   20 return
	  end
!******************************************************************
      subroutine getMatrix(x0,y0,z0,t0)
      common /station/nst,StList(50),stx(50),sty(50),stz(50)
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)

!	  integer*4 Ndst
	  character*4 StList

	  x1=x0
	  y1=y0
	  z1=z0
	  t1=t0
	  do 100 i=1,nps
	       j=numst(i)
		   xst=stx(j)
		   yst=sty(j)
		   zst=stz(j)
		   delt=sqrt((x1-xst)**2+(y1-yst)**2)	 ! epicentral distance
           dist=sqrt(delt**2+(z1-zst)**2)		 ! hypocentral distance
           ips=1
		   if(i.gt.np) ips=2                                  
! 1 Layer
           if(nZLayer.eq.1) then
                call ttL1mat(i)
                goto 1000
           end if
! 2 Layer
           if(nZLayer.eq.2) then
                call ttL2mat(i)
                goto 1000
           end if
! 3 Layer
           if(nZLayer.eq.3) then
                call ttL3mat(i)
                goto 1000
           end if
! 4 Layer
           if(nZLayer.eq.4) then
                call ttL4mat(i)
                goto 1000
           end if
! 5 Layer
           if(nZLayer.eq.5) then
                call ttL5mat(i)
                goto 1000
           end if
! 6 Layer
           if(nZLayer.eq.6) then
                call ttL6mat(i)
                goto 1000
           end if
 
          1000 continue
	  100 continue

	  return
	  end
!******************************************************************
      subroutine normalEQ
      
      common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
	  common /weight/ wp(50),ws(50),w(50),wratio
  	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
	  real*8 c,d,dd
  
  
      do 100 i=1, 4
          do 50 j=1, 5
               dd(i, j) = 0!
               do 10 k=1,nps
                 	dd(i, j) = dd(i, j) + c(k, i) * c(k, j) * w(k) * w(k)
               10 continue
          50 continue
     100 continue
! Damping
	
		dd(1,1)=dd(1,1)+damping
		dd(2,2)=dd(2,2)+damping
	    dd(3,3)=dd(3,3)+damping
	 	dd(4,4)=dd(4,4)+damping
      RETURN
	  end
!*******************************************************************
!      subroutine solution
	  subroutine solution (nsol)
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
	  real*8 c,d,dd
	  real*8 cc,ccc

! SOLUTION 
      IF(nsol.eq.1) goto 15
      do 10 P = 1, 4
          do 5 Q = 1, 5
               d(P, Q) = DD(P, Q)
          5 continue
      10 continue 
      GOTO 20
   15 continue 
      do 18 P = 1, 4
          do 17 Q = 1,  4
               d(P, Q) = DD(P, Q)
          17 continue
      18 continue 
   20 continue
      do 100 I = 1, 4
          J = I
          IF (d(I, J).ne.0.0d0) goto 30
   25 continue 
          J = J + 1
          IF(J.gt. 4) goto 150
          IF( d(I, J).eq.0.0d0) goto 25
          do 27 K = 1, 4
		       ccc=d(i,k)
			   d(i,k)=d(j,k)
			   d(j,k)=ccc
 !              SWAP d(I, K), d(J, K)
          27 continue

		  ccc=d(i,5)
		  d(i,5)=d(j,5)
		  d(j,5)=ccc
 !         SWAP d(I, 5), d(J, 5)
   30 continue
          CC = d(I, I)
          IF (CC.eq. 0.0d0) goto 150
          do 35 J = 1, 5
               d(I, J) = d(I, J) / CC
          35 continue
		  do 45 k=1,4
               IF (K.eq.i) goto 40
               CC = d(K, I)
               do 37 J = 1, 5
                    d(K, J) = d(K, J) - CC * d(I, J)
               37 continue
               40 continue
          45 continue
          50 continue
     100 continue
     goto 200
 150 continue
     write(*,60)
	 60 format(1h ,'ERROR')
 200 continue
	 RETURN
     END
!*****************************************************************
      subroutine makePSarray
! PÇ∆SÇÃóLå¯ÉfÅ[É^ÇàÍë±Ç´ÇÃÉtÉ@ÉCÉãÇ…Ç∑ÇÈ
       common /station/nst,StList(50),stx(50),sty(50),stz(50)
	   common /arvdata/ ndata,iyear,imonth,iday,ihour,imini,st_name,p(50),pol,accp,s(50),accs
       common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
       common /weight/ wp(50),ws(50),w(50),wratio
	   character*4 StList,st_name(50),pol(50),accp(50),accs(50)

	  np=0
! P
	  do 10 i=1,nst
	       if(p(i).eq.99.99) goto 10
	        np=np+1
		    numst(np)=i
    	    ttobs(np)=p(i)
		    w(np)=wp(i)
	  10 continue
! S
	  ns=0
	  do 20 i=1,nst
	       if(s(i).eq.99.99) goto 20
	        ns=ns+1
		    numst(np+ns)=i
    	    ttobs(np+ns)=s(i)
		    w(np+ns)=ws(i)
	  20 continue
	     nps=np+ns
		 return
		 end
!********************************************************************
!********** êÖïΩê¨1ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈÅ@*********
      subroutine ttL1mat(i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      call calT10(T10)
 !     tt=T10
	  call matT10(T10,i)
      return
      end
!********************************************************************
!********** êÖïΩê¨1ëwç\ë¢Ç…Ç®ÇØÇÈ T10ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT10(T10,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

      real*8 c,d,dd
      v=VL(1,ips)
	  vd=v*dist
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=(zst-z1)/vd
	  c(i,4)=-1.0
	  c(i,5)=(T10+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨2ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈÅ@*********
      subroutine ttL2mat(i)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      ! 1) z1<=zL1
      if(z1.le.zL1) then
           call calT10(T10)
           call calT11(T11)
		   if(T10.lt.T11) then
		        call matT10(T10,i)
           else
		        call matT11(T11,i)
           end if
           goto 10
      end if

      ! 2) z1>zL1
      call calT20(T20)
      call matT20(T20,i)
   10 continue
      return
      end
!********************************************************************
!********** êÖïΩê¨2ëwç\ë¢Ç…Ç®ÇØÇÈ T11ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT11(T11,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(2,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c12(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T11+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨2ëwç\ë¢Ç…Ç®ÇØÇÈ T20ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT20(T20,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/rayparm/pp,cos2
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      real*8 pp,cos2
	  real*8 c,d,dd

      v=VL(2,ips)
	  c(i,1)=pp*(xst-x1)/delt
	  c(i,2)=pp*(yst-y1)/delt
	  c(i,3)=-dsqrt(cos2)/v
	  c(i,4)=-1.0
	  c(i,5)=(T20+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨3ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈ *********
      subroutine ttL3mat(i)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      ! 1) z1<=zL1
      if(z1.le.zL1) then
           call calT10(T10)
           call calT11(T11)
           call calT12(T12)
           tt=min(T10,T11,T12)
		   if(tt.eq.T10) call matT10(T10,i)
		   if(tt.eq.T11) call matT11(T11,i)
		   if(tt.eq.T12) call matT12(T12,i)
           goto 10
       end if

      ! 2) zL1<z1<=zL2
      if(z1.gt.zL1.and.z1.le.zL2) then
           call calT20(T20)
           call calT21(T21)
           tt=min(T20,T21)
		   if(tt.eq.T20) call matT20(T20,i)
		   if(tt.eq.T21) call matT21(T21,i)
           goto 10
      end if

      ! 3) z1>zL2
      call calT30(T30)
      tt=T30
	  call matT30(T30,i)

   10 continue
      return
      end
!********************************************************************
!********** êÖïΩê¨3ëwç\ë¢Ç…Ç®ÇØÇÈ T12ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT12(T12,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(3,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c13(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T12+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨3ëwç\ë¢Ç…Ç®ÇØÇÈ T21ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT21(T21,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(3,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c23(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T21+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨3ëwç\ë¢Ç…Ç®ÇØÇÈ T30ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT30(T30,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/rayparm/pp,cos2
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      real*8 pp,cos2
	  real*8 c,d,dd

      v=VL(3,ips)
	  c(i,1)=pp*(xst-x1)/delt
	  c(i,2)=pp*(yst-y1)/delt
	  c(i,3)=-dsqrt(cos2)/v
	  c(i,4)=-1.0
	  c(i,5)=(T30+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨4ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈ *********
      subroutine ttL4mat(i)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      ! 1) z1<=zL1
      if(z1.le.zL1) then
           call calT10(T10)
           call calT11(T11)
           call calT12(T12)
           call calT13(T13)
           tt=min(T10,T11,T12,T13)
		   if(tt.eq.T10) call matT10(T10,i)
		   if(tt.eq.T11) call matT11(T11,i)
		   if(tt.eq.T12) call matT12(T12,i)
		   if(tt.eq.T13) call matT13(T13,i)
           goto 10
      end if
      ! 2) zL1<z1<=zL2
      if(z1.gt.zL1.and.z1.le.zL2) then
           call calT20(T20)
           call calT21(T21)
           call calT22(T22)
           tt=min(T20,T21,T22)
		   if(tt.eq.T20) call matT20(T20,i)
		   if(tt.eq.T21) call matT21(T21,i)
		   if(tt.eq.T22) call matT22(T22,i)
	       goto 10
      end if
      ! 3) zL2<z1<=zL3
      if(z1.gt.zL2.and.z1.le.zL3) then
           call calT30(T30)
           call calT31(T31)
           tt=min(T30,T31)
		   if(tt.eq.T30) call matT30(T30,i)
		   if(tt.eq.T31) call matT31(T31,i)
           goto 10
      end if
      ! 4) z1>zL3
      call calT40(T40)
      tt=T40
	  call matT40(T40,i)
   10 continue
      return
      end
!********************************************************************
!********** êÖïΩê¨4ëwç\ë¢Ç…Ç®ÇØÇÈ T13ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT13(T13,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(4,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c14(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T13+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨4ëwç\ë¢Ç…Ç®ÇØÇÈ T22ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT22(T22,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(4,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c24(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T22+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨4ëwç\ë¢Ç…Ç®ÇØÇÈ T31ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT31(T31,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(4,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c34(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T31+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨4ëwç\ë¢Ç…Ç®ÇØÇÈ T40ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT40(T40,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/rayparm/pp,cos2
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      real*8 pp,cos2
	  real*8 c,d,dd

      v=VL(4,ips)
	  c(i,1)=pp*(xst-x1)/delt
	  c(i,2)=pp*(yst-y1)/delt
	  c(i,3)=-dsqrt(cos2)/v
	  c(i,4)=-1.0
	  c(i,5)=(T40+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈ *********
      subroutine ttL5mat(i)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      ! 1) z1<=zL1
      if(z1.le.zL1) then
           call calT10(T10)
           call calT11(T11)
           call calT12(T12)
           call calT13(T13)
           call calT14(T14)
           tt=min(T10,T11,T12,T13,T14)
		   if(tt.eq.T10) call matT10(T10,i)
		   if(tt.eq.T11) call matT11(T11,i)
		   if(tt.eq.T12) call matT12(T12,i)
		   if(tt.eq.T13) call matT13(T13,i)
		   if(tt.eq.T14) call matT14(T14,i)
		   goto 10
      end if
      ! 2) zL1<z1<=zL2
      if(z1.gt.zL1.and.z1.le.zL2) then
           call calT20(T20)
           call calT21(T21)
           call calT22(T22)
           call calT23(T23)
           tt=min(T20,T21,T22,T23)
		   if(tt.eq.T20) call matT20(T20,i)
		   if(tt.eq.T21) call matT21(T21,i)
		   if(tt.eq.T22) call matT22(T22,i)
		   if(tt.eq.T23) call matT23(T23,i)
		   goto 10
      end if
      ! 3) zL2<z1<=zL3
      if(z1.gt.zL2.and.z1.le.zL3) then
           call calT30(T30)
           call calT31(T31)
           call calT32(T32)
           tt=min(T30,T31,T32)
		   if(tt.eq.T30) call matT30(T30,i)
		   if(tt.eq.T31) call matT31(T31,i)
		   if(tt.eq.T32) call matT32(T32,i)
	       goto 10
      end if
      ! 4) zL3<z1<=zL4
      if(z1.gt.zL3.and.z1.le.zL4) then
           call calT40(T40)
           call calT41(T41)
           tt=min(T40,T41)
  		   if(tt.eq.T40) call matT40(T40,i)
		   if(tt.eq.T41) call matT41(T41,i)
           goto 10
      end if
      ! 5) z1>zL4
      call calT50(T50)
      tt=T50
	  call matT50(T50,i)
   10 continue

      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T14ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT14(T14,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(5,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c15(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T14+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T23ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT23(T23,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(5,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c25(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T23+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T32ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT32(T32,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(5,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c35(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T32+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T41ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT41(T41,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(5,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c45(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T41+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T50ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT50(T50,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/rayparm/pp,cos2
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      real*8 pp,cos2
	  real*8 c,d,dd

      v=VL(5,ips)
	  c(i,1)=pp*(xst-x1)/delt
	  c(i,2)=pp*(yst-y1)/delt
	  c(i,3)=-dsqrt(cos2)/v
	  c(i,4)=-1.0
	  c(i,5)=(T50+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ MatrixÇãÅÇﬂÇÈ *********
      subroutine ttL6mat(i)
!********************************************************************
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist

      ! 1) z1<=zL1
      if(z1.le.zL1) then
           call calT10(T10)
           call calT11(T11)
           call calT12(T12)
           call calT13(T13)
           call calT14(T14)
           call calT15(T15)
           tt=min(T10,T11,T12,T13,T14,T15)
           if(tt.eq.T10) call matT10(T10,i)
		   if(tt.eq.T11) call matT11(T11,i)
		   if(tt.eq.T12) call matT12(T12,i)
		   if(tt.eq.T13) call matT13(T13,i)
		   if(tt.eq.T14) call matT14(T14,i)
		   if(tt.eq.T15) call matT15(T15,i)
		   goto 10
      end if
      ! 2) zL1<z1<=zL2
      if(z1.gt.zL1.and.z1.le.zL2) then
           call calT20(T20)
           call calT21(T21)
           call calT22(T22)
           call calT23(T23)
           call calT24(T24)
           tt=min(T20,T21,T22,T23,T24)
		   if(tt.eq.T20) call matT20(T20,i)
		   if(tt.eq.T21) call matT21(T21,i)
		   if(tt.eq.T22) call matT22(T22,i)
		   if(tt.eq.T23) call matT23(T23,i)
		   if(tt.eq.T24) call matT24(T24,i)
            goto 10
      end if
      ! 3) zL2<z1<=zL3
      if(z1.gt.zL2.and.z1.le.zL3) then
           call calT30(T30)
           call calT31(T31)
           call calT32(T32)
           call calT33(T33)
           tt=min(T30,T31,T32,T33)
		   if(tt.eq.T30) call matT30(T30,i)
		   if(tt.eq.T31) call matT31(T31,i)
		   if(tt.eq.T32) call matT32(T32,i)
		   if(tt.eq.T33) call matT33(T33,i)
	       goto 10
      end if
      ! 4) zL3<z1<=zL4
      if(z1.gt.zL3.and.z1.le.zL4) then
           call calT40(T40)
           call calT41(T41)
           call calT42(T42)
           tt=min(T40,T41,T42)
		   if(tt.eq.T40) call matT40(T40,i)
		   if(tt.eq.T41) call matT41(T41,i)
		   if(tt.eq.T42) call matT42(T42,i)
		   goto 10
      end if
      ! 5) zL4<z1<=zL5
      if(z1.gt.zL4.and.z1.le.zL5) then
           call calT50(T50)
           call calT51(T51)
           tt=min(T50,T51)
		   if(tt.eq.T50) call matT50(T50,i)
		   if(tt.eq.T51) call matT51(T51,i)
           goto 10
      end if
      ! 6) z1>zL5
      call calT60(T60)
      tt=T60
	  call matT60(T60,i)
   10 continue
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ T14ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT15(T15,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(6,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c16(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T15+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨5ëwç\ë¢Ç…Ç®ÇØÇÈ T41ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT42(T42,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(6,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c46(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T42+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ T24ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT24(T24,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd

      v=VL(6,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c26(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T24+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ T33ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT33(T33,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(6,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c36(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T33+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ T51ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT51(T51,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/mat/damping,c(50,5),d(4,5),dd(4,5)

	  real*8 c,d,dd
      
	  v=VL(6,ips)
	  vd=v*delt
	  c(i,1)=(xst-x1)/vd
	  c(i,2)=(yst-y1)/vd
	  c(i,3)=c56(ips)
	  c(i,4)=-1.0
	  c(i,5)=(T51+t1)-ttobs(i)
      return
      end
!********************************************************************
!********** êÖïΩê¨6ëwç\ë¢Ç…Ç®ÇØÇÈ T60ópMatrixÇãÅÇﬂÇÈ *********
      subroutine matT60(T60,i)
!********************************************************************
      common/ttparm/xst,yst,zst,x1,y1,z1,t1,tt,ips,delt,dist
      common/snell/nZLayer,zL1,zL2,zL3,zL4,zL5,VL(6,2)
	  common /tt/np,ns,nps,numst(50),ttobs(50),ttcal(50),spobs(50),spcal(50)
      common/vcoeff/c12(2),c13(2),c14(2),c15(2),c16(2),c23(2),c24(2),c25(2),c26(2),  &
                    c34(2),c35(2),c36(2),c45(2),c46(2),c56(2)
 	  common/rayparm/pp,cos2
	  common/mat/damping,c(50,5),d(4,5),dd(4,5)
      real*8 pp,cos2
	  real*8 c,d,dd

      v=VL(6,ips)
	  c(i,1)=pp*(xst-x1)/delt
	  c(i,2)=pp*(yst-y1)/delt
	  c(i,3)=-dsqrt(cos2)/v
	  c(i,4)=-1.0
	  c(i,5)=(T60+t1)-ttobs(i)
      return
      end
!********************************************************************
