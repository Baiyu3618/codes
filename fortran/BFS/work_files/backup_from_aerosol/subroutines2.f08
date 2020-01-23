! this file contains
! 1. PCE_coeff_compute subroutine
! 2. solve_PCE subroutine
! 3. correct_VP_DC subroutine

subroutine PCE_coeff_compute()

    use params
    use model_vars

    implicit none

    ! pressure correction equation coefficients computation
    do i = 2,npx-1
        do j = 2,npy-1
            aep(i,j) = rho*dy*du(i,j)
            awp(i,j) = rho*dy*du(i-1,j)
            anp(i,j) = rho*dx*dv(i,j)
            asp(i,j) = rho*dx*dv(i,j-1)
            app(i,j) = aep(i,j)+awp(i,j)+anp(i,j)+asp(i,j)
            Bp(i,j) = rho*(dy*(us(i-1,j)-us(i,j))+dx*(vs(i,j-1)-vs(i,j)))
        end do
    end do
    pp = 0.0; pprev = pp

end subroutine PCE_coeff_compute

subroutine solve_PCE()

    use params
    use model_vars

    implicit none

    ! pressure correction equation solution
    do iterate_p = 1,100
        do i = 2,npx-2
            do j = 2,npy-1
                pp(i,j) = 1.0/app(i,j)*(aep(i,j)*pp(i+1,j)+awp(i,j)*pp(i-1,j) &
                    +anp(i,j)*pp(i,j+1)+asp(i,j)*pp(i,j-1)+Bp(i,j))
            end do
        end do
        pp(1,:) = pp(2,:); pp(:,1) = pp(:,2); pp(:,npy) = pp(:,npy-1)

        con_p = maxval(abs(pprev-pp)); pprev = pp
        if (con_p < 1e-7) then
            exit
        end if
    end do

end subroutine solve_PCE

subroutine correct_VP_DC()

    use params
    use model_vars

    implicit none

    ! pressure correction
    p = p + 0.1*pp

    ! x velocity correction
    do i = 2,nux-1
        do j = 2,nuy-1
            u(i,j) = us(i,j) + du(i,j)*(pp(i,j)-pp(i+1,j))
        end do
    end do
    u(nux,:) = u(nux-1,:)

    ! y-velocity correction
    do i = 2,nvx-1
        do j = 2,nvy-1
            v(i,j) = vs(i,j) + dv(i,j)*(pp(i,j)-pp(i,j+1))
        end do
    end do
    v(nvx,:) = v(nvx-1,:)

    if(any(isnan(p))) then
        error stop "solution diverged"
    end if

end subroutine correct_VP_DC
