  ! this is the parameters module for LDC problem
module params

  implicit none

  ! declaring common datatype
  integer,parameter :: ikd = selected_int_kind(8)
  integer,parameter :: rkd = selected_real_kind(8,8)

  ! density and viscosity of fluid
  real(kind=ikd),parameter :: rho = 1.225, mu = 1.789e-5
  ! length and width of fluid domain
  real(kind=rkd),parameter :: length = 0.1, width = 0.1
  ! fluid reynolds number and computational timestep size
  real(kind=rkd),parameter :: Re = 10000, dt = 5e-4
  ! number of nodes in computational domain
  integer(kind=ikd),parameter :: nx = 129, ny = 129

  ! staggered grid arrangement
  integer(kind=ikd),parameter :: npx = nx+1, npy = ny+1
  integer(kind=ikd),parameter :: nux = npx-1, nuy = npy
  integer(kind=ikd),parameter :: nvx = npx, nvy = npy-1
  
end module params

! this is the computational varaiables module
module model_vars

  use params

  implicit none

  ! computation coefficients required for momentum equations
  real(kind=rkd) :: ap,ae,aw,an,as,bu,bv,du(nux,nuy),dv(nvx,nvy)
  ! computation coefficients required for pressure correction equations
  real(kind=rkd),dimension(npx,npy) :: app,aep,awp,anp,asp,bp,pprev
  ! computation primitive variables declaration
  real(kind=rkd) :: u(nux,nuy),us(nux,nuy),vs(nvx,nvy),X(nx,ny)
  real(kind=rkd) :: p(npx,npy),pp(npx,npy),v(nvx,nvy),Y(nx,ny)
  real(kind=rkd) :: Uc(nx,ny),Vc(nx,ny),Pc(nx,ny)
  ! misceleaneous integer and real variables required for computation
  integer(kind=ikd) :: itr_out,itr_in,i,j,iterate_p
  real(kind=rkd) :: dx,dy,de,dw,dn,ds,fe,fw,fn,fs,uplate,convergence_p
  real(kind=rkd) :: pe,pw,pn,ps,ap0
  
end module model_vars
