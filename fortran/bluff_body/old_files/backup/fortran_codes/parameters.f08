  ! this file ontains the parameters for bluff body computation
module parameters

  implicit none

  ! declaring common datatype for variable declarations
  integer,parameter :: ikd = selected_int_kind(8)
  integer,parameter :: rkd = selected_real_kind(8,8)

  ! variables related to geometry and meshing section
  integer(kind=ikd) :: i,j,nx,ny,itr
  real(kind=rkd),allocatable, dimension(:,:) :: X,Y,dxe,dye,dxn,dyn,Jac
  real(kind=rkd) :: dE,dN

  ! fluid flow parameters secton
  real(kind=rkd),parameter :: machno = 2.0, rho0 = 1.5, T0 = 300.0
  real(kind=rkd),parameter :: gamma = 1.4, Rc = 287.0, Cv = 718.0

  ! computation parameters section
  real(kind=rkd),parameter :: dt = 1e-3
  integer(kind=ikd),parameter :: timesteps = 1000

  ! computation variables section
  real(kind=rkd),allocatable, dimension(:,:) :: U,V,rho,T,u1,u2,u3,u4
  real(kind=rkd),allocatable, dimension(:,:) :: f1,f2,f3,f4,g1,g2,g3,g4
  real(kind=rkd),allocatable, dimension(:,:) :: p,E,H
  real(kind=rkd) :: Uin
  
end module parameters
