!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! geometry and mesh generator script for bluff body aerodynamics !
! developed by Ramkumar                                          !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program main

  use params                    !parameter module
  use model_vars                !model variables module

  implicit none

  ! creating initial mesh-------------------------------------------------------
  call initial_mesh_generator()

  ! elliptic grid generation----------------------------------------------------
  main_loop: do itr = 1,iteration

     ! previous values allocation
     xprev = x; yprev = y

     do i = 2,nx-1
        do j = 2,ny-1

           ! computing alpha, beta and gamma values for current step
           call compute_alpha(i,j)
           call compute_beta(i,j)
           call compute_gamma(i,j)

           ! computing new ofset x and y value
           call compute_x(x(i,j),i,j)
           call compute_y(y(i,j),i,j)
           
        end do
     end do

     ! checking for convergence
     convergence = maxval(abs(xprev-x))

     print *,"Iteration ",itr," Convergence : ",convergence

     if (convergence .le. converg) then
        print *,"Converged !"
        exit
     end if
  
  end do main_loop

  ! writing the new x,y values to file
  call exporter()

  print *,"Done!"
  
end program main
