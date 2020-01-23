  ! this script contains the subroutines necessary for post processing

! decoder subroutine
subroutine decoder()

  use parameters

  implicit none

  ! decoding density
  rho = U1

  ! decoding x velocity
  U = U2/U1

  ! decoding y velocity
  V = U3/U1

  ! decoding temperature
  T = (gamma - 1.0)/Rc*(U4/U1 - 0.5*(U2**2 + U3**2)/U1**2)

  ! computing presssure
  P = rho*T*Rc
  
end subroutine decoder

! data writer subroutine
subroutine writer()

  use parameters

  implicit none

  real(kind=rkd),dimension(nx,ny) :: Vr,Mach

  Vr = sqrt(U**2 + V**2)        ! computing resultant velocity
  Mach = Vr/sqrt(gamma*Rc*T)    ! computing mach number

50 format(f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5,",",f12.5)

  open(unit = 1, file = "Data.csv")

  write(unit = 1, fmt = *) "X,Y,Z,U,V,Vr,P,T,rho,Mach"

  do i = 1,nx
     do j = 1,ny
        write(unit = 1, fmt = 50) X(i,j),Y(i,j),0.0,U(i,j),V(i,j),Vr(i,j),P(i,j),T(i,j),rho(i,j),Mach(i,j)
     end do
  end do

  print *,"File Written Successfully"
  
end subroutine writer
