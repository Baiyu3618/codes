! this file contains
!     1. compute_1st_der subroutine
!     2. solver subroutine
!     3. exporter subroutine

subroutine compute_1st_der()

    use params
    use model_vars

    implicit none

    do j = 1,N_intnodes

        i = INTNODES(j)
        count = 1
        dFidXi = 0.0
        dFidYi = 0.0
        dXi2 = 0.0
        dYi2 = 0.0
        dXidYi = 0.0
        det = 0.0

        do while(NNODES(i,count) /= 0)
            no = NNODES(i,count)
            dFidXi = dFidXi + abs(T(i)-T(no))*abs(X(i)-X(no))
            dFidYi = dFidYi + abs(T(i)-T(no))*abs(Y(i)-Y(no))
            dXi2 = dXi2 + (X(i)-X(no))**2
            dYi2 = dYi2 + (Y(i)-Y(no))**2
            dXidYi = dXidYi + abs(X(i)-X(no))*abs(Y(i)-Y(no))
            count = count + 1
        end do

        det = dXi2*dYi2 - dXidYi**2

        dTx(i) = (dFidXi*dYi2 - dFidYi*dXidYi)/det
        dTy(i) = (dFidYi*dXi2 - dFidXi*dXidYi)/det

        print *,dTx(i),dTy(i)

    end do

end subroutine compute_1st_der

subroutine solver()

    use params
    use model_vars

    implicit none

    do j = 1,N_intnodes

        i = INTNODES(j)

        ! computing 2nd order x derivative of temperature
        count = 1
        dFidXi = 0.0
        dFidYi = 0.0
        dFidXi1 = 0.0
        dFidYi1 = 0.0
        dXi2 = 0.0
        dYi2 = 0.0
        dXidYi = 0.0
        det = 0.0

        do while(NNODES(i,count) /= 0)
            no = NNODES(i,count)
            dFidXi = dFidXi + abs(dTx(i)-dTx(no))*abs(X(i)-X(no))
            dFidYi = dFidYi + abs(dTx(i)-dTx(no))*abs(Y(i)-Y(no))
            dFidXi1 = dFidXi1 + abs(dTy(i)-dTy(no))*abs(X(i)-X(no))
            dFidYi1 = dFidYi1 + abs(dTy(i)-dTy(no))*abs(Y(i)-Y(no))
            dXi2 = dXi2 + (X(i)-X(no))**2
            dYi2 = dYi2 + (Y(i)-Y(no))**2
            dXidYi = dXidYi + abs(X(i)-X(no))*abs(Y(i)-Y(no))
            count = count + 1
        end do
        det = dXi2*dYi2 - dXidYi**2

        dTxx = (dFidXi*dYi2 - dFidYi*dXidYi)/det
        dTyy = (dFidYi1*dXi2 - dFidXi1*dXidYi)/det

        ! heat equation solution
        Ts(i) = T(i) + alpha*(dTxx + dTyy)*dt

    end do

end subroutine solver

subroutine exporter()

    use params
    use model_vars

    implicit none

    open(unit = 7, file = "Data.csv")

    50 format(f12.5,",",f12.5,",",f12.5,",",f12.5)

    write(unit = 7, fmt = *) "X,Y,Z,T"

    do i = 1,Nxy
        write(unit = 7, fmt = 50) X(i),Y(i),0.0,T(i)
    end do

    close(unit = 7)

end subroutine exporter
