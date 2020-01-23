! this is the main file for backward facing step computation code
program main

    use params
    use model_vars

    implicit none

    ! initializing the computational variables
    call initializer()
    print *,"Initialization Done..."

    ! entering main loop
    main_loop: do itr = 1,Nstep

        ! momentum equations coefficients computation
        call ME_coeff_compute()

        ! momentum equations Solution
        call solve_ME()

        ! pressure correction equation coefficients computation
        call PCE_coeff_compute()

        ! pressure correction equation solution
        call solve_PCE()
        !
        ! velocity and pressure correction and divergence check
        call correct_VP_DC()

        print *,"TimeStep : ",itr

        ! primitive variables co-location computation
        call colocate()

        ! export result to a CSV FILE for PARAFOAM
        call export()

        print *,"Data saved for TimeStep : ",itr

    end do main_loop

    print *,"Solution Done"

    print *,"Data exported successfully"

    print *,"Program Terminated ..."

end program main
