 ! this is the reader subroutine for bluff body simulation
subroutine reader()

  use parameters

  implicit none

  ! declaring some temporary variables
  character(len = 10) :: tmp
  real(kind=rkd) :: tmp1,tmp2

  ! opening the grid file
  open(unit = 1, file = "Grid.csv")
  
  ! reading the first header line
  read(unit = 1, fmt = *) tmp

  ! reading the second number of elements line
  read(unit = 1, fmt = *) tmp1,tmp2
  nx = int(tmp1); ny = int(tmp2)
  
  ! allocating the mesh grid arrays
  allocate(X(nx,ny),Y(nx,ny))

  ! reading the grid data
  do j = 1,ny
     do i = 1,nx
        read(unit = 1, fmt = *) X(i,j),Y(i,j)
     end do
  end do

  close(unit = 1)
  
end subroutine reader

! this is transformer subroutine for inverse grid transformation
subroutine transformer()

  use parameters

  ! allocating variables for transformation
  allocate(dxe(nx,ny),dye(nx,ny),Jac(nx,ny),dxn(nx,ny),dyn(nx,ny))

  dE = 1.0;  dN = 1.0

  ! computing grid transformation parameters
  dxe = 0.0; dye = 0.0; dxn = 0.0; dyn = 0.0
  
  do i = 2,nx-1
     do j = 2,ny-1
        dxe(i,j) = (X(i+1,j)-X(i-1,j))/dE/2.0
        dxn(i,j) = (X(i,j+1)-X(i,j-1))/dN/2.0
        dye(i,j) = (Y(i+1,j)-Y(i-1,j))/dE/2.0
        dyn(i,j) = (Y(i,j+1)-Y(i,j-1))/dN/2.0
        Jac(i,j) = dxe(i,j)*dyn(i,j) - dye(i,j)*dxn(i,j)
     end do
  end do  
  
end subroutine transformer

! this is the initializer module
subroutine initializer()

  use parameters

  implicit none

  real(kind=rkd) :: temp

  ! computing inlet velocity
  Uin = machno*sqrt(gamma*Rc*T0)

  ! allocating all the required variables
  allocate(rho(nx,ny),u(nx,ny),v(nx,ny),T(nx,ny))
  allocate(u1(nx,ny),u2(nx,ny),u3(nx,ny),u4(nx,ny))
  allocate(f1(nx,ny),f2(nx,ny),f3(nx,ny),f4(nx,ny))
  allocate(g1(nx,ny),g2(nx,ny),g3(nx,ny),g4(nx,ny))

  ! initializing primitive flow field variables
  do j = 1,ny
     do i = 1,nx
        rho(i,j) = (rho0-1.0)/(1.0-float(nx))*i + (rho0*nx-1.0)/(float(nx) - 1.0)
        T(i,j) = (T0-293.0)/(1.0-float(nx))*i + (T0*nx-293.0)/(float(nx) - 1.0)
        U(i,j) = (Uin-0.0)/(1.0-float(nx))*i + (Uin*nx-0.0)/(float(nx) - 1.0) 
     end do
  end do
  v = 0.0
  
  P = rho*T*Rc                  ! computing the initial pressure field

  E = 1.0/(gamma-1.0)*P/rho + 0.5*(U**2 + V**2) ! computing specific total energy

  H = E + p/rho                 ! computing specific total enthalpy

  ! initializing conservative flow field variables
  U1 = rho
  U2 = rho*U
  U3 = rho*V
  U4 = rho*E

end subroutine initializer
