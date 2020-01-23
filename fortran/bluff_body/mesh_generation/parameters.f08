  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ! submain 1 file of grid generation script !
  ! developed by Ramkumar                    !
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

module params

  implicit none

  ! uniform datatype declaration------------------------------------------------
  integer,parameter :: ikd = selected_int_kind(8), rkd = selected_real_kind(8,8)

  ! mesh parameters declaration-------------------------------------------------
  real(kind=rkd),parameter :: a1 = 0.1, b1 = 0.05, a2 = 0.5, b2 = 0.25
  integer(kind=ikd),parameter :: nx = 11, ny = 21, iteration = 100000
  real(kind=rkd),parameter :: pi = 4.0*atan(1.0), de = 1.0, dn = 1.0
  real(kind=rkd),parameter :: converg = 1e-7
  
end module params

module model_vars

  use params

  implicit none

  ! single integer definitions
  integer(kind=ikd) :: i,j,itr

  ! single real definitions
  real(kind=rkd) :: alpha,beta,gamma,p,q,convergence,r,s

  ! real array definitions
  real(kind=rkd),dimension(nx,ny) :: x,y,xprev,yprev
  real(kind=rkd),dimension(nx) :: a,b
  real(kind=rkd),dimension(ny) :: t
  
end module model_vars
