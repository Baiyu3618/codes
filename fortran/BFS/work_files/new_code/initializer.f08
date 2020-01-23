! this file contains the initializer subroutine for backward facing step
subroutine initializer()

    use params
    use model_vars

    implicit none

    ! computing the mesh grid
    dx = length/float(nx-1); dy = width/float(ny-1)
    X = 0.0; Y = 0.0
    do i = 1,nx
        do j = 1,ny
            X(i,j) = float(i-1)*dx
            Y(i,j) = -width/2+float(j-1)*dy
        end do
    end do

    ! computing Y co-ordinates for U staggered grid
    do i = 1,nuy
        Yu(i) = -dy/2 + float(i-1)*dy
    end do

    ! computing molecular dynamic viscosity
    mu = rho*Vavg*width/Re

    ! computing diffusion and source-related terms
    De = mu/dx*dy; Dw = De; Dn = mu/dy*dx; Ds = Dn
    ap0 = rho*dx*dy/dt

    ! initializing primitive variables
    u = 0.0; v = 0.0; p = 0.0; pp = 0.0
    u(1,Nwend+1:nuy) = 24*Y(1,Nwend:ny)*(width/2-Y(1,Nwend:ny))
    u(1,1:Nwend+1) = 0 ! adjustments regarding parabolic velocity inlet
    us = u; vs = v; p = 0; Pressure_prev = p
    max_p_residual = 0

end subroutine initializer
