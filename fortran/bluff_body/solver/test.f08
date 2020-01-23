program main

  implicit none

  integer,dimension(10,10) :: a
  integer :: i,k

  do i = 1,1000000     
     k = k*99999
  end do

  print *,k

contains

  integer function man(x)

    implicit none

    integer,intent(in) :: x

    man = (x-1)/(x-x)

    return
    
  end function man
  
end program main
