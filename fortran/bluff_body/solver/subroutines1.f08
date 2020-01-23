!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! bluff body aerodynamics subroutine 1 file !
!   developed by Ramkumar                   !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! mesh file reader module-----------------------------------------------------
subroutine reader()

  use params
  use model_vars

  implicit none

  ! ! opening the grid file
  ! open(unit = 1, file = "grid.grd")

  ! ! reading number of elements line
  ! read(unit = 1, fmt='(F12.5 F12.5 F12.5)') tmp1, tmp2, tmp2

  ! nx = int(tmp1)
  ! ny = int(tmp2)
  
  ! ! allocating grid variables and reading data from file
  ! allocate(x(nx,ny),y(nx,ny))

  ! do i = 1,nx
  !    do j = 1,ny
  !       read(unit = 1, fmt='(F12.5 F12.5 F12.5)') x(i,j), tmp1, y(i,j)
  !    end do
  ! end do
    
  ! close(unit = 1)

  nx = 101; ny = 101

  allocate(x(nx,ny),y(nx,ny))

  x = 0.0; y = 0.0

  do i = 1,nx
     do j = 1,ny
        x(i,j) = float((i-1)/(nx-1))
        y(i,j) = float((j-1)/(ny-1))
     end do
  end do 

  print *,"Mesh read success! "
  
end subroutine reader

! inverse_transformer subroutine definition-------------------------------------
subroutine inverse_transform()

  use params
  use model_vars

  implicit none

  ! allocating variables
  allocate(jac(nx,ny), dye(nx,ny), dyn(nx,ny), dxe(nx,ny), dxn(nx,ny))

  jac = 0.0
  dye = 0.0; dyn = 0.0
  dxe = 0.0; dxn = 0.0

  ! computing transformation parameters
  do i = 2,nx-1
     do j = 2,ny-1
        dxe(i,j) = (x(i+1,j) - x(i-1,j))/de/2.0
        dxn(i,j) = (x(i,j+1) - x(i,j-1))/dn/2.0

        dye(i,j) = (y(i+1,j) - y(i-1,j))/de/2.0
        dyn(i,j) = (y(i,j+1) - y(i,j-1))/dn/2.0

        jac(i,j) = dxe(i,j)*dyn(i,j) - dxn(i,j)*dye(i,j)
     end do
  end do

  print *,"Transformation parameters computed .."
  
end subroutine inverse_transform

! initializer subroutine--------------------------------------------------------
subroutine initializer()

  use params
  use model_vars

  implicit none

  ! allocating the variables
  allocate(rho(nx,ny),u(nx,ny),v(nx,ny),p(nx,ny))
  allocate(rhos(nx,ny),us(nx,ny),vs(nx,ny),ps(nx,ny))

  ! initializing variables
  ! rho = rho0
  ! p = p0
  
  ! do j = 1,ny
  !    u(:,j) = (/(i,i=0,nx-1,1)/)*(0 - mach*sqrt(gamma*R*T0))/(nx-1) &
  !         + mach*sqrt(gamma*R*T0)
  ! end do
  ! v = 0.01*u

  ! rho = (x - minval(x))/(maxval(x) - minval(x))*0.9*rho0 + rho0
  ! u = (x - minval(x))/(maxval(x) - minval(x))*0.9*mach*sqrt(gamma*R*T0) &
  !      + mach*sqrt(gamma*R*T0)
  ! v = 0.0
  ! p = (x - minval(x))/(maxval(x) - minval(x))*0.9*p0 &
  !      + p0

  rho = rho0
  p = p0
  u = mach*sqrt(gamma*R*T0)
  v = 0.0

  print *,"initialization done .. "
    
end subroutine initializer
