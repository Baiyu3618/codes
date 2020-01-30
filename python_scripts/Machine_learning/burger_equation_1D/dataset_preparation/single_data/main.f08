  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ! dataset preparation for burgers equation 1d !
  ! developed by Ramkumar                       !
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program main

  implicit none

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ! variables declaration section !
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  ! uniform variable type declaration
  integer,parameter :: ikd = selected_int_kind(8), rkd = selected_real_kind(8,8)

  integer(kind = ikd), dimension(1), parameter :: n = (/2/) !number of phase shifts
  real(kind = rkd), dimension(1), parameter :: phi = (/0.0/), amplitude = (/0.6/) !number of phase angles
  integer(kind = ikd), parameter :: nx = 51, ntimes = 1000
  real(kind = rkd), parameter :: len = 1.0, time = 1.0, nu = 0.01 !max simulation length and time, diffusion coefficient
  real(kind = rkd), parameter :: pi = 4.0*atan(1.0)

  real(kind = rkd) :: dx = len/float(nx-1), dt = time/ntimes
  integer(kind = ikd) :: i,j,itr, ni, phi_i, a_i
  real(kind = rkd),dimension(nx) :: X, U, U_new, dudt
  character(len = 50) :: filename
  real(kind = rkd), dimension(nx,nx) :: Amatrix


50 format("data_n",i0,"_phi",f0.2,"_A",f0.2,".csv")

  ! initializing x variable
  do i = 1,nx
    X(i) = float(i-1)*dx
 end do

 ! begining computation
 do ni = 1,size(n)
    do phi_i = 1,size(phi)
       do a_i = 1,size(amplitude)
          ! initializing u
          U = amplitude(a_i)*sin(n(ni)*pi*(X - phi(phi_i)))
          ! opening a new file
          write(filename, fmt=50) n(ni),phi(phi_i),amplitude(a_i)
          open(unit = 1, file = filename)

          do itr = 1,ntimes
             call matrix_maker()

             dudt = matmul(Amatrix, U)

             U_new = U + dudt*dt

             write(unit = 1, fmt = *) U_new

             U = U_new

          end do

          print *,"writen file: ",filename
          exit
       end do
       exit
    end do
    exit
 end do

 call matrix_maker()

 ! matrix subroutine definition
contains

 subroutine matrix_maker()
   Amatrix = 0.0
   do  i = 2,nx - 1
      Amatrix(i,i) = U(i+1)/2/dx - 2*nu/dx**2
      Amatrix(i,i+1) = nu/dx**2
      Amatrix(i,i-1) = nu/dx**2 - U(i)/2/dx
   end do

 end subroutine matrix_maker


end program main
