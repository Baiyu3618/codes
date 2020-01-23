  ! this is the main file for bluff body simulation
program main

  use parameters

  implicit none

  ! reading the geometry from file
  call reader()

  ! performing grid transformations
  call transformer()

  ! initializing computation variables
  call initializer()

  ! begining main loop
  ! main_loop: do itr = 1,timesteps
  !    ! encoding the previous result values
  !    call encoder(U1,U2,U3,U4,F1,F2,F3,F4,G1,G2,G3,G4)

  !    ! calling solver routine
  !    call solver()

  !    ! checking for solution divergence
  !    if (any(isnan(U2))) then
  !       error stop "solution diverged"
  !    end if

  !    ! printing the current time step number
  !    print *,"Time Step : ",itr
     
  ! end do main_loop

  ! call decoder()

  call writer()
  
end program main
