! this file contains
! 1. collocate subroutine
! 2. export subroutine
! 3. export_staggered subroutine
! 4. resume subroutine
subroutine colocate

    use params
    use model_vars

    implicit none

    ! colocating x velocity
    Uc = 0.0; Uc(:,1) = u(:,1); Uc(:,ny) = u(:,nuy)
    do j = 2,ny-1
        Uc(:,j) = 0.5*(u(:,j)+u(:,j+1))
    end do

    ! colocating y velocity
    Vc = 0.0; Vc(1,:) = v(1,:); Vc(nx,:) = v(nvx,:)
    do i = 2,nx-1
        Vc(i,:) = 0.5*(v(i,:)+v(i+1,:))
    end do

    ! colocating pressure
    Pc = 0.0
    do i = 1,nx
        do j = 1,ny
            Pc(i,j) = 0.25*(p(i,j)+p(i+1,j)+p(i,j+1)+p(i+1,j+1))
        end do
    end do

end subroutine colocate

subroutine export()

    use params
    use model_vars

    open(unit=1, file="Data.csv", status="replace")

    15 format(f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5)

    write(unit=1,fmt=*) "X,Y,Z,U,V,P"

    do i = 1,nx
        do j = 1,ny
            write(unit=1,fmt=15) X(i,j),Y(i,j),0.0,Uc(i,j),Vc(i,j),Pc(i,j)
        end do
    end do

    close(unit=1)

end subroutine export

subroutine export_staggered()

    use params
    use model_vars

    implicit none

    open(unit = 3, file = "u.txt", status = "replace")
    do i = 1,nux
        do j = 1,nuy
            write(unit = 3, fmt = *) u(i,j)
        end do
    end do
    close(unit = 3)

    open(unit = 4, file = "v.txt", status = "replace")
    do i = 1,nvx
        do j = 1,nvy
            write(unit = 4, fmt = *) v(i,j)
        end do
    end do
    close(unit = 4)

    open(unit = 5, file = "p.txt", status = "replace")
    do i = 1,npx
        do j = 1,npy
            write(unit = 5, fmt = *) p(i,j)
        end do
    end do
    close(unit = 5)

end subroutine export_staggered

subroutine resume()

    use params
    use model_vars

    implicit none

    ! reading previous stopped timestep
    open(unit=11, file="TimeStep.txt")
    read(unit = 11, fmt = *) istart,tmp
    close(unit=11)

    ! reading previous pressure values
    open(unit = 13, file = "p.txt")
    do i = 1,npx
        do j = 1,npy
            read(unit = 13, fmt=*) p(i,j)
        end do
    end do
    close(unit = 13)

    ! reading previous x-velocity values
    open(unit = 21, file = "u.txt")
    do i = 1,nux
        do j = 1,nuy
            read(unit = 21, fmt = *) u(i,j)
        end do
    end do
    close(unit = 21)

    ! reading previous y-velocity values
    open(unit = 22, file = "v.txt")
    do i = 1,nvx
        do j = 1,nvy
            read(unit = 22, fmt = *) v(i,j)
        end do
    end do
    close(unit = 22)

    ! reading residual values of pressure
    max_p_residual = 0.0
    open(unit = 23, file = "p_residual.txt")
    do i = 1,Nstep
        read(unit = 23, fmt = *) max_p_residual(i)
    end do
    close(unit = 23)

end subroutine resume
