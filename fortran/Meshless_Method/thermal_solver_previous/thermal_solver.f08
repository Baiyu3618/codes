! this file contains
!     1. main solver code
program main

    use params
    use model_vars

    implicit none

    ! reading nodes from mesh files
    call read_mesh()
    print *,"Mesh read done..."

    ! collecting nearby nodes to each node
    print *,"collecting nearby nodes ..."
    call collector()
    print *,"Done ..."

    ! initializing computational variables
    call initializer()
    print *,"Initialization done..."

    ! main loop of computation
    main_loop: do itr = 1,Nstep

        ! computing 1st order derivatives of temperature
        call compute_1st_der()

        ! solving heat equation
        call solver()

        print *,"Time Step : ",itr," of ",Nstep

        ! checking convergence
        convergence = maxval(abs(Ts - T)); T = Ts

        if(any(isnan(T))) then
            error stop "Solution Diverged!!!"
        end if

        if(convergence .le. residual) then
            print *,"Solution Converged!!!!"
            exit
        end if

    end do main_loop

    ! exporting data in CSV file
    call exporter()

    print *,"Data export done..."

    print *,"Post-computation Residual : ",convergence

    print *,"Program terminated with code 0"

end program main
