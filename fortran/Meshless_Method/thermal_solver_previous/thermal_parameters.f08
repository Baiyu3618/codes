! this file contains :
!     1. thermal parameters
!     2. computational variables
module params

    implicit none

    ! uniform datatype declaration
    integer,parameter :: ikd = selected_int_kind(8)
    integer,parameter :: rkd = selected_real_kind(8,8)

    ! material density
    real(kind=rkd),parameter :: rho = 2700.0        ! kg/cub.m
    ! material thermal conductivity
    real(kind=rkd),parameter :: k = 237.0           ! W/m.K.
    ! material specific heat
    real(kind=rkd),parameter :: c = 921.096         ! J/kg.K.

    ! temperature at INODES
    real(kind=rkd),parameter :: Ti = 393.0          ! K.
    ! temperature at ONODES
    real(kind=rkd),parameter :: To = 293.0          ! K.
    ! temperature at WNODES
    real(kind=rkd),parameter :: TW = 293.0          ! K.
    ! initial temperature at INTNODES
    real(kind=rkd),parameter :: Tinit = 293.0       ! k.

    ! computation timestep
    real(kind=rkd),parameter :: dt = 1e-3           ! s.
    ! number of timesteps
    integer(kind=ikd),parameter :: Nstep = 1
    ! cut-off width
    real(kind=rkd),parameter :: Lcw = 0.08          ! m.
    ! residual for convergence checking
    real(kind=rkd),parameter :: residual = 1e-7

end module params

module model_vars

    use params

    implicit none

    ! computation variables allocation
    real(kind=rkd),allocatable,dimension(:) :: X,Y,T,Ts,dTx,dTy
    ! mesh read variables allocation
    integer(kind=ikd),allocatable,dimension(:) :: INODES,WNODES,ONODES,INTNODES
    ! nearby nodes NNODES array declaration
    integer(kind=ikd),allocatable,dimension(:,:) :: NNODES

    ! scalar computation variables declaration
    integer(kind=ikd) :: i,itr,N_intnodes,N_inodes,N_onodes,N_wnodes,Nxy
    integer(kind=ikd) :: j,count,no
    real(kind=rkd) :: convergence,dump,dist,alpha,dFidXi,dYi2
    real(kind=rkd) :: det,dFidYi,dXi2,dXidYi,dTxx,dTyy,dFidXi1,dFidYi1

end module model_vars
