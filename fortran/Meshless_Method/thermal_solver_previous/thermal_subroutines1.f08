! this file contains
!     1. read_mesh subroutine
!     2. collector subroutine
!     3. initializer subroutine

subroutine read_mesh()

    use params
    use model_vars

    implicit none

    ! reading x y coordinates
    open(unit = 1, file = "coord.xy")
    read(unit = 1, fmt = *) dump

    Nxy = int(dump)

    allocate(X(Nxy),Y(Nxy))

    do i = 1,Nxy
        read(unit = 1, fmt = *) X(i),Y(i)
    end do

    close(unit = 1)

    ! reading INODES
    open(unit = 2, file = "INODES.nod")
    read(unit = 2, fmt = *) N_inodes

    allocate(INODES(N_inodes))

    do i = 1,N_inodes
        read(unit = 2, fmt = *) INODES(i)
    end do

    close(unit = 2)

    ! reading ONODES
    open(unit = 3, file = "ONODES.nod")
    read(unit = 3, fmt = *) N_onodes

    allocate(ONODES(N_onodes))

    do i = 1, N_onodes
        read(unit = 3, fmt = *) ONODES(i)
    end do

    close(unit = 3)

    ! reading WNODES
    open(unit = 4, file = "WNODES.nod")
    read(unit = 4, fmt = *) N_wnodes

    allocate(WNODES(N_wnodes))

    do i = 1,N_wnodes
        read(unit = 4, fmt = *) WNODES(i)
    end do

    close(unit = 4)

    ! reading INTNODES
    open(unit = 5, file = "INTNODES.nod")
    read(unit = 5, fmt = *) N_intnodes

    allocate(INTNODES(N_intnodes))

    do i = 1,N_intnodes
        read(unit = 5, fmt = *) INTNODES(i)
    end do

    close(unit = 5)

end subroutine read_mesh

subroutine collector()

    use params
    use model_vars

    implicit none

    ! allocating array
    allocate(NNODES(Nxy,10))

    NNODES = 0

    ! begining collection
    do i = 1,Nxy
        count = 1
        do j = 1,Nxy
            if( i .eq. j) then
                continue
            end if
            dist = sqrt((X(i)-X(j))**2 + (Y(i)-Y(j))**2)
            if( dist .le. Lcw) then
                NNODEs(i,count) = j
                count = count + 1
            end if
            if(count .ge. 10) then
                exit
            end if
        end do

    end do

end subroutine collector

subroutine initializer()

    use params
    use model_vars

    implicit none

    ! initializing temperature field
    allocate(T(Nxy),Ts(Nxy),dTx(Nxy),dTy(Nxy))
    T = Tinit
    T(INODES) = Ti
    T(ONODES) = To
    T(WNODES) = Tw

    Ts = T

    dTx = 0.0
    dTy = 0.0

    ! computing thermal diffusivity
    alpha = k/rho/C

end subroutine initializer
