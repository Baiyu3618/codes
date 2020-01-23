! this is the main file for backward facing step computation code
program main

    use params
    use model_vars

    implicit none

    ! initializing the computational variables
    call initializer()
    print *,"Initialization Done..."

    ! resume computation
    call resume()

    ! entering main loop
    main_loop: do itr = istart,Nstep

        ! momentum equations coefficients computation
        call ME_coeff_compute()

        ! momentum equations Solution
        call solve_ME()

        ! pressure correction equation coefficients computation
        call PCE_coeff_compute()

        ! pressure correction equation solution
        call solve_PCE()

        ! velocity and pressure correction and divergence check
        call correct_VP_DC()

        print *,"TimeStep : ",itr

        ! writing the current timestep value to a file and checking convergence
        convergence = maxval(abs(Pressure_prev-p))
        open(unit=2, file="TimeStep.txt", status="replace")
        write(unit = 2, fmt = *) itr, convergence
        close(unit=2)

        ! writing max residual of p per timestep for post-computation plotting
        max_p_residual(itr) = convergence
        open(unit = 10, file='p_residual.txt', status = "replace")
        do i = 1,Nstep
            write(unit = 10, fmt = *) max_p_residual(i)
        end do
        close(unit = 10)

        ! export current time step staggered parameters for Resumability
        call export_staggered()

        if(convergence < 1e-9) then
            print *,"Solution Converged!!!"
            exit
        end if

        print *,"Data saved for TimeStep : ",itr

    end do main_loop

    ! primitive variables co-location computation
    call colocate()
    print *,"Colocation of variables done..."

    ! export result to a CSV FILE for PARAFOAM
    call export()
    print *,"CSV File generated..."

    print *,"Solution Done"

    print *,"Program Terminated ..."

end program main
