  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ! subroutines 1 file for the bluff body grid generation !
  ! developed by Ramkumar                                 !
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! initial mesh generator module
subroutine initial_mesh_generator()

  use params
  use model_vars
  
  implicit none

  ! initiating grid arrays
  a = (/(i, i=0,nx-1, 1)/)*(a1-a2)/(nx-1) + a2
  b = (/(i, i=0,nx-1, 1)/)*(b1-b2)/(nx-1) + b2
  t = (/(i, i=0,ny-1, 1)/)*pi/(ny-1) - pi/2.0

  x = 0.0; y = 0.0

  ! making grid
  do i = 1,nx
     do j = 1,ny
        x(i,j) = -a(i)*cos(t(j))
        y(i,j) =  b(i)*sin(t(j))
     end do
  end do

  print *,"Initial grid generated ! "
  
end subroutine initial_mesh_generator

! data file exporter module
subroutine exporter()

  use params
  use model_vars

  implicit none

  ! creating file
  open(unit = 1, file = "grid.grd")

15 format(f12.6,",",f12.6)

  ! writing data to file
  write(unit = 1, fmt = 15) float(nx),float(ny)

  do i = 1,nx
     do j = 1,ny
        write(unit = 1, fmt = 15) x(i,j), y(i,j)        
     end do
  end do

  ! closing file
  close(unit=1)

  print *,"file writen successfully !"
  
end subroutine exporter

! alpha computer module
subroutine compute_alpha(ip,jp)

  use params
  use model_vars

  implicit none

  integer(kind=ikd),intent(in) :: ip,jp

  p = (x(ip,jp+1) - x(ip,jp-1))/dn/2.0
  q = (y(ip,jp+1) - y(ip,jp-1))/dn/2.0

  alpha = p**2 + q**2
  
end subroutine compute_alpha

! beta computer module
subroutine compute_beta(ip,jp)

  use params
  use model_vars

  implicit none

  integer(kind=ikd),intent(in) :: ip,jp

  p = (x(ip+1,jp) - x(ip-1,jp))/de/2.0
  q = (y(ip+1,jp) - y(ip-1,jp))/de/2.0
  r = (x(ip,jp+1) - x(ip,jp-1))/dn/2.0
  s = (y(ip,jp+1) - y(ip,jp-1))/dn/2.0

  beta = p*r + q*s
  
end subroutine compute_beta

! gamma computer module
subroutine compute_gamma(ip,jp)

  use params
  use model_vars

  implicit none

  integer(kind=ikd),intent(in) :: ip,jp

  p = (x(ip+1,jp) - x(ip-1,jp))/de/2.0
  q = (y(ip+1,jp) - y(ip-1,jp))/de/2.0

  gamma = p**2 + q**2
  
end subroutine compute_gamma

! x ofset value computation module
subroutine compute_x(xc,ip,jp)

  use params
  use model_vars

  implicit none

  real(kind=rkd),intent(out) :: xc
  integer(kind=ikd),intent(in) :: ip,jp

  ! computing ofset
  p = alpha*(x(ip+1,jp) + x(ip-1,jp))/de**2
  
  q = 2.0*beta*(x(ip+1,jp+1) + x(ip-1,jp-1) - x(ip+1,jp-1) - x(ip-1,jp+1))/4.0/de/dn
  
  r = gamma*(x(ip,jp+1) + x(ip,jp-1))/dn**2
  
  s = 2.0*(alpha/de**2 + gamma/dn**2)

  xc = 1.0/s * (p - q + r)
  
end subroutine compute_x

! y ofset value computation module
subroutine compute_y(yc,ip,jp)

  use params
  use model_vars

  implicit none

  real(kind=rkd),intent(out) :: yc
  integer(kind=ikd),intent(in) :: ip,jp

  ! computing ofset
  p = alpha*(y(ip+1,jp) + y(ip-1,jp))/de**2
  q = 2.0*beta*(y(ip+1,jp+1) + y(ip-1,jp-1) - y(ip+1,jp-1) - y(ip-1,jp+1))/4.0/de/dn
  r = gamma*(y(ip,jp+1) + y(ip,jp-1))/dn**2
  s = 2.0*(alpha/de**2 + gamma/dn**2)

  yc = 1.0/s * (p - q + r)
  
end subroutine compute_y
