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
  call encoder(U1,U2,U3,U4,F1,F2,F3,F4,G1,G2,G3,G4)
  call solver()

  call decoder()

  call writer()
  
end program main
