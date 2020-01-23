  ! this is the initializer module required for computation
subroutine initializer()

  use params
  use model_vars

  implicit none

  ! creating mesh region
  dx = length/float(nx-1)
  dy = width/float(ny-1)
  X = 0; y = 0;
  
  do i = 1,nx
     do j = 1,ny
        X(i,j) = dx*float(i-1)
        Y(i,j) = dy*float(j-1)
     end do
  end do

  ! computing plate velocity and initialzing field variables
  uplate = Re*mu/rho/length
  p = 0.0; u = 0.0; v = 0.0
  u(:,nuy) = uplate;
  us = u; vs = v; pp = p;

  ! initializing diffusion parts
  de = mu/dx*dy; dw = de
  dn = mu/dy*dx; ds = dn

  ap0 = rho*dx*dy/dt
  
end subroutine initializer

! this is the colocator module
subroutine colocator()

  use params
  use model_vars

  ! colocating U velocity
  Uc(:,1) = u(:,1); Uc(:,ny) = u(:,nuy)  
  do j = 2,ny-1
     Uc(:,j) = 0.5*(u(:,j) + u(:,j+1))
  end do

  ! colocating V velocity
  Vc(1,:) = v(1,:); Vc(nx,:) = v(nvx,:)
  do i = 2,nx-1
     Vc(i,:) = 0.5*(v(i,:) + v(i+1,:))
  end do

  ! colocating pressure
  do i = 1,nx
     do j = 1,ny
        Pc(i,j) = 0.25*(p(i,j)+p(i+1,j)+p(i,j+1)+p(i+1,j+1))
     end do
  end do  
  
end subroutine colocator

! this is the exporter module
subroutine exporter()

  use params
  use model_vars

  implicit none

  ! creating format for export
50 format(f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5)

  ! creating file
  open(unit = 2, file = "Data.csv")

  ! writing header line
  write(unit = 2, fmt = *) "X,Y,U,V,P"

  ! writing the data to the file
  do i = 1,nx
     do j = 1,ny
        write(unit = 2, fmt = 50) X(i,j),Y(i,j),Uc(i,j),Vc(i,j),Pc(i,j)
     end do
  end do

  ! closing the file
  close(unit = 2)
  
end subroutine exporter
