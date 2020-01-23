! this module contains parameters required for computation
module params

    implicit none

    ! declaring standard datatypes for variables
    integer,parameter :: ikd = selected_int_kind(8)
    integer,parameter :: rkd = selected_real_kind(8,8)

    ! density and Reynolds Number of fluid, based on width
    real(kind=rkd),parameter :: rho = 1.0, Re = 800
    ! length and width of fluid domain
    real(kind=rkd),parameter :: length = 30.0, width = 1.0
    ! average inlet velocity and computational time step size
    real(kind=rkd),parameter :: Vavg = 1.0, dt = 1e-3
    ! number of nodes and timesteps
    integer(kind=ikd),parameter :: nx = 1801, ny = 61, Nstep = 100000
    ! wall step start and end nodes
    integer(kind=ikd),parameter :: Nwstart = 1, Nwend = int(ny/2)

    ! nodal arrangements for staggered grid
    integer(kind=ikd),parameter :: npx = nx+1, npy = ny+1
    integer(kind=ikd),parameter :: nux = npx-1, nuy = npy
    integer(kind=ikd),parameter :: nvx = npx, nvy = npy-1

end module params

! this module contains all the variables used in this program
module model_vars

    use params

    implicit none

    ! 2 dimensional variables
    real(kind=rkd),dimension(nux,nuy) :: u,us,apu,aeu,awu,anu,asu,bu,du,uprev
    real(kind=rkd),dimension(nvx,nvy) :: v,vs,apv,aev,awv,anv,asv,dv,bv,vprev
    real(kind=rkd),dimension(npx,npy) :: p,pp,app,aep,awp,anp,asp,pprev,Bp
    real(kind=rkd),dimension(nx,ny) :: X,Y,Uc,Vc,Pc

    ! 1d variable for implementing BC
    real(kind=rkd),dimension(nuy) :: Yu

    ! scalar variables
    real(kind=rkd) :: Fe,Fw,Fn,Fs,De,Dw,Dn,Ds,con_p,con_u
    real(kind=rkd) :: Pe,Pw,Pn,Ps,con_v,dx,dy,mu,ap0
    integer(kind=ikd) :: itr,i,j,iterate_p,iterate_v

end module model_vars
