!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! bluff body aerodynamics solver parameters file !
! developed by Ramkumar                          !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! parameters module definition--------------------------------------------------
module params

  implicit none

  ! uniform variable type declaration
  integer,parameter :: ikd = selected_int_kind(8), rkd = selected_real_kind(8,8)

  ! inlet fluid parameters definition
  real(kind=rkd),parameter :: rho0 = 1.225, T0 = 300.0, gamma = 1.4, R = 287.0
  ! far field definitions
  real(kind=rkd),parameter :: mach = 1.0, p0 = rho0*R*T0
  ! simulation parameters
  real(kind=rkd),parameter :: time = 0.001, dt = 1.0e-5, de = 1.0, dn = 1.0
  
end module params

! model variables definition----------------------------------------------------
module model_vars

  use params

  implicit none

  ! single integer variables
  integer(kind=ikd) :: i,j,nx,ny

  ! single real variables
  real(kind=rkd) :: tmp1,tmp2,c,time_itr

  ! multidimensional real variables
  real(kind=rkd),allocatable, dimension(:,:) :: jac, dyn,dye,dxn,dxe,X,Y
  real(kind=rkd),allocatable, dimension(:,:) :: rho,u,v,p,rhos,us,vs,ps
  real(kind=rkd), dimension(4,4) :: aw, bw
  real(kind=rkd), dimension(4,1) :: wt,wx,wy
  
end module model_vars
