! this file contains following
! 1. ME_coeff_compute subroutine
! 2. solve_ME subroutine

subroutine ME_coeff_compute()

    use params
    use model_vars

    implicit none

    ! x momentum equation coefficients computation
    do i = 2,nux-1
        do j = 2,nuy-1
            Fe = rho*dy*0.5*(u(i,j)+u(i+1,j))
            Fw = rho*dy*0.5*(u(i,j)+u(i-1,j))
            Fn = rho*dx*0.5*(v(i,j)+v(i+1,j))
            Fs = rho*dx*0.5*(v(i,j-1)+v(i+1,j-1))

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aeu(i,j) = De*max(0.0,(1.0-0.1*abs(Pe))**5) + max(0.0,-Fe)
            awu(i,j) = Dw*max(0.0,(1.0-0.1*abs(Pw))**5) + max(0.0, Fw)
            anu(i,j) = Dn*max(0.0,(1.0-0.1*abs(Pn))**5) + max(0.0,-Fn)
            asu(i,j) = Ds*max(0.0,(1.0-0.1*abs(Ps))**5) + max(0.0, Fs)
            apu(i,j) = aeu(i,j)+awu(i,j)+anu(i,j)+asu(i,j)+ap0
            bu(i,j) = ap0*u(i,j); du(i,j) = dy/apu(i,j)
        end do
    end do

    ! y momentum equation coefficients computation
    do i = 2,nvx-1
        do j = 2,nvy-1
            Fe = rho*dy*0.5*(u(i,j)+u(i,j+1))
            Fw = rho*dy*0.5*(u(i-1,j)+u(i-1,j+1))
            Fn = rho*dx*0.5*(v(i,j)+v(i,j+1))
            Fs = rho*dx*0.5*(v(i,j)+v(i,j-1))

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aev(i,j) = De*max(0.0,(1.0-0.1*abs(Pe))**5) + max(0.0,-Fe)
            awv(i,j) = Dw*max(0.0,(1.0-0.1*abs(Pw))**5) + max(0.0, Fw)
            anv(i,j) = Dn*max(0.0,(1.0-0.1*abs(Pn))**5) + max(0.0,-Fn)
            asv(i,j) = Ds*max(0.0,(1.0-0.1*abs(Ps))**5) + max(0.0, Fs)
            apv(i,j) = aev(i,j)+awv(i,j)+anv(i,j)+asv(i,j)+ap0
            bv(i,j) = ap0*v(i,j); dv(i,j) = dx/apv(i,j)
        end do
    end do

end subroutine ME_coeff_compute

subroutine solve_ME()

    use params
    use model_vars

    implicit none

    ! momentum equations solution
    uprev = us; vprev = vs
    do  iterate_v = 1,1000
        do i = 2,nux-1
            do j = 2,nuy-1
                us(i,j) = 1/apu(i,j)*(aeu(i,j)*us(i+1,j)+awu(i,j)*us(i-1,j)+ &
                    anu(i,j)*us(i,j+1)+asu(i,j)*us(i,j-1)+bu(i,j)) + &
                    du(i,j)*(p(i,j)-p(i+1,j))
            end do
        end do
        do i = 2,nvx-1
            do j = 2,nvy-1
                vs(i,j) = 1/apv(i,j)*(aev(i,j)*vs(i+1,j)+awv(i,j)*vs(i-1,j)+ &
                    anv(i,j)*vs(i,j+1)+asv(i,j)*vs(i,j-1)+bv(i,j)) + &
                    dv(i,j)*(p(i,j)-p(i,j+1))
            end do
        end do
        us(nux,:) = us(nux-1,:)
        vs(nvx,:) = vs(nvx-1,:)

        con_u = maxval(abs(uprev-us)); uprev = us
        con_v = maxval(abs(vprev-vs)); vprev = vs

        if (con_u<1e-9 .and. con_v<1e-9) then
            exit
        end if
    end do

end subroutine solve_ME
