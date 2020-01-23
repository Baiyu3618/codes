  ! this is the main file for computation of LDC Re10000
program main

  use params
  use model_vars
  
  implicit none

  ! initializing external calling variables
  integer :: system, status
  integer(kind=ikd) :: count = 0,loop_counter = 1

  ! creating directories for saving contours
  status = system("mkdir velocity_contour")
  status = system("mkdir pressure_contour")  

  ! initializing computational variables
  call initializer()
  print *,"initialization done"

  ! creating id file and writing initial data to the disk
  open(unit = 1, file = "fileid.txt")
  write(unit=1,fmt=*) count
  close(unit = 1)
  count = count + 1
  call colocator()
  call exporter()
  
  status = system("python3 plotter.py")
  print*,"created initial data plot"

  ! entering main loop
  outer_loop: do itr_out = 1,480

     inner_loop: do itr_in = 1,50

        ! solving momentum equations
        call momentum_solver()

        ! computing pressure correction equation coefficients
        call PCE_coeff_computer()

        ! solving pressure correction equation
        call PCE_solver()

        ! updating velocity and pressure
        call PV_updater()

        ! updating in the terminal
        print *,"Current Step : ",loop_counter
        loop_counter = loop_counter+1

     end do inner_loop

     ! colocating data and exporting it to plotter
     open(unit = 1, file = "fileid.txt")
     write(unit=1,fmt=*) count
     close(unit = 1)
     count = count + 1
     call colocator()
     call exporter()
     status = system("python3 plotter.py")
     print *,"Plotted data for current step"
     
  End do outer_loop
  
end program main

