!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! bluff body aerodynamics solver main file !
! developed by Ramkumar                    !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program main

  implicit none

  real*4,dimension(3,3) :: a
  real*4,dimension(3,3) :: b
  real*4,dimension(3,3) :: c
  integer*4 :: i,j

  ! do i = 1,3
  !    do j = 1,3
  !       a(i,j) = i+j
  !       b(i,j) = i*j
  !    end do
  ! end do
  a = rand(100)
  b = 1

  c = matmul(a,b)

15 format(f12.5," ",f12.5," ",f12.5," ",f12.5)

  print *,"A matrix"
  do i = 1,ubound(a,1)
     write(unit=*,fmt=15) (a(i,j), j=1,ubound(a,2))
  end do

  print *,"B matrix"
  do i = 1,ubound(b,1)
     write(unit=*,fmt=15) (b(i,j), j=1,ubound(b,2))
  end do

  print *,"C matrix"
  do i = 1,ubound(c,1)
     write(unit=*,fmt=15) (c(i,j), j=1,ubound(c,2))
  end do
  
end program main
