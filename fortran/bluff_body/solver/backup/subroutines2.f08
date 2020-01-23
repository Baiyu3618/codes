!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! bluff body aerodynamics subroutines 2 file !
! developed by Ramkumar                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! solution matrix generator subroutines-----------------------------------------
subroutine build_coeff_matrices(ip,jp)

  use params
  use model_vars

  implicit none

  integer(kind=ikd), intent(in) :: ip,jp

  aw = 0.0
  bw = 0.0

  ! computing speed of sound
  c = sqrt(gamma * p(ip,jp) / rho(ip,jp))

  ! initializing aw matrix
  aw(1,1) = u(ip,jp)
  aw(1,2) = rho(ip,jp)
  aw(2,2) = u(ip,jp)
  aw(2,4) = 1.0/rho(ip,jp)
  aw(3,3) = u(ip,jp)
  aw(4,2) = rho(ip,jp)*c**2
  aw(4,4) = u(ip,jp)

  ! initializing bw matrix
  bw(1,1) = v(ip,jp)
  bw(1,3) = rho(ip,jp)
  bw(2,2) = v(ip,jp)
  bw(3,3) = v(ip,jp)
  bw(3,4) = 1.0/rho(ip,jp)
  bw(4,3) = rho(ip,jp)*c**2
  bw(4,4) = v(ip,jp)
  
end subroutine build_coeff_matrices

! main solver subroutine--------------------------------------------------------
subroutine solver()

  use params
  use model_vars

  implicit none

  ! begining solver loop
  do i = 2,nx-1
     do j = 2,ny-1

        ! building coeff matrices for current index
        call build_coeff_matrices(i,j)

        ! building wx vector
        wx(1,1) = 1.0/jac(i,j) * ((rho(i+1,j) - rho(i-1,j))/de/2.0 * dyn(i,j) -&
             (rho(i,j+1) - rho(i,j-1))/dn/2.0 * dye(i,j)) ! density
        wx(2,1) = 1.0/jac(i,j) * ((u(i+1,j) - u(i-1,j))/de/2.0 * dyn(i,j) -&
             (u(i,j+1) - u(i,j-1))/dn/2.0 * dye(i,j)) ! x-velocity
        wx(3,1) = 1.0/jac(i,j) * ((v(i+1,j) - v(i-1,j))/de/2.0 * dyn(i,j) -&
             (v(i,j+1) - v(i,j-1))/dn/2.0 * dye(i,j)) ! y-velocity
        wx(4,1) = 1.0/jac(i,j) * ((p(i+1,j) - p(i-1,j))/de/2.0 * dyn(i,j) -&
             (p(i,j+1) - p(i,j-1))/dn/2.0 * dye(i,j)) ! pressure

        ! building wy vector
        wy(1,1) = 1.0/jac(i,j) * ((rho(i,j+1) - rho(i,j-1))/dn/2.0 * dxe(i,j) -&
             (rho(i+1,j) - rho(i-1,j))/de/2.0 * dxn(i,j)) ! density
        wy(2,1) = 1.0/jac(i,j) * ((u(i,j+1) - u(i,j-1))/dn/2.0 * dxe(i,j) -&
             (u(i+1,j) - u(i-1,j))/de/2.0 * dxn(i,j)) ! x-velocity
        wy(3,1) = 1.0/jac(i,j) * ((v(i,j+1) - v(i,j-1))/dn/2.0 * dxe(i,j) -&
             (v(i+1,j) - v(i-1,j))/de/2.0 * dxn(i,j)) ! y-velocity
        wy(4,1) = 1.0/jac(i,j) * ((p(i,j+1) - p(i,j-1))/dn/2.0 * dxe(i,j) -&
             (p(i+1,j) - p(i-1,j))/de/2.0 * dxn(i,j)) ! pressure

        ! computing wt
        wt = -matmul(aw,wx) -matmul(bw,wy)

        ! updating variables
        rhos(i,j) = rho(i,j) + wt(1,1)*dt
        us(i,j) = u(i,j) + wt(2,1)*dt
        vs(i,j) = v(i,j) + wt(3,1)*dt
        ps(i,j) = p(i,j) + wt(4,1)*dt
        
     end do
  end do

  ! applying boundary conditions
  rhos(:,ny) = 2.0*rhos(:,ny-1) - rhos(:,ny-2)
  rhos(:,1) = 2.0*rhos(:,2) - rhos(:,3)

  us(:,ny) = 2.0*us(:,ny-1) - us(:,ny-2)
  us(:,1) = 2.0*us(:,2) - us(:,3)

  vs(:,ny) = 2.0*vs(:,ny-1) - vs(:,ny-2)
  vs(:,1) = 2.0*vs(:,2) - vs(:,3)

  ps(:,ny) = 2.0*ps(:,ny-1) - ps(:,ny-2)
  ps(:,1) = 2.0*ps(:,2) - ps(:,3)

  rhos(nx,:) = 2.0*rhos(nx-1,:) - rhos(nx-2,:)
  ps(nx,:) = 2.0*ps(nx-1,:) - ps(nx-2,:)

  us(nx,:) = 0.0; vs(nx,:) = 0.0

  rho = rhos
  u = us
  v = vs
  p = ps
  
end subroutine solver

! data exporter subroutine------------------------------------------------------
subroutine exporter()

  use params
  use model_vars

  implicit none

  open(unit = 1, file = "data.dat")

50 format(f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5)

  do i = 1,nx
     do j = 1,ny
        write(unit = 1, fmt=50) x(i,j),y(i,j),rho(i,j),u(i,j),v(i,j),p(i,j)
     end do
  end do

  close(unit=1)

  print *,"Data export success"
  
end subroutine exporter
