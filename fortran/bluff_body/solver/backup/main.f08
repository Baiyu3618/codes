!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! bluff body aerodynamics solver main file !
! developed by Ramkumar                    !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program main

  use params
  use model_vars

  implicit none

  ! reading the grid file
  call reader()

  ! computing inverse transformation components
  call inverse_transform()

  ! initializing computation primitive variables
  call initializer()

  ! initializing solution
  time_itr = 0.0
  
  main_loop: do while (time_itr .le. time)

     time_itr = time_itr + dt

     ! solving the equations
     call solver()

     print *,"Simulation Time : ",time_itr

     print *,maxval(rhos),maxval(us),maxval(vs),maxval(ps)
     
  end do main_loop

  ! writing the values to file
  call exporter()
  
end program main
