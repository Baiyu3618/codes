  ! this file contains all the solver subroutines

subroutine momentum_solver()

  use params
  use model_vars

  implicit none

  ! solving x-momentum equation
  do i = 2,nux-1
     do j = 2,nuy-1
        fe = rho*dy*0.5*(u(i,j)+u(i+1,j))
        fw = rho*dy*0.5*(u(i,j)+u(i-1,j))
        fn = rho*dx*0.5*(v(i,j)+v(i+1,j))
        fs = rho*dx*0.5*(v(i,j-1)+v(i+1,j-1))

        pe = fe/de; pw = fw/dw; pn = fn/dn; ps = fs/ds

        ae = de*max(0.0,(1.0-0.1*abs(pe))**5) + max(0.0,-fe)
        aw = dw*max(0.0,(1.0-0.1*abs(pw))**5) + max(0.0, fw)
        an = dn*max(0.0,(1.0-0.1*abs(pn))**5) + max(0.0,-fn)
        as = ds*max(0.0,(1.0-0.1*abs(ps))**5) + max(0.0, fs)
        ap = ae+aw+an+as+ap0; bu = ap0*u(i,j); du(i,j) = dy/ap

        ! solving equation
        us(i,j) = 1/ap*(ae*u(i+1,j)+aw*u(i-1,j)+an*u(i,j+1)+as*u(i,j-1)+bu)+du(i,j)*(p(i,j)-p(i+1,j))
        
     end do
  end do

  ! y-momentum equation solution
  do i = 2,nvx-1
     do j = 2,nvy-1
        fe = rho*dy*0.5*(u(i,j)+u(i,j+1))
        fw = rho*dy*0.5*(u(i-1,j)+u(i-1,j+1))
        fn = rho*dx*0.5*(v(i,j)+v(i,j+1))
        fs = rho*dx*0.5*(v(i,j)+v(i,j-1))

        pe = fe/de; pw = fw/dw; pn = fn/dn; ps = fs/ds

        ae = de*max(0.0,(1.0-0.1*abs(pe))**5) + max(0.0,-fe)
        aw = dw*max(0.0,(1.0-0.1*abs(pw))**5) + max(0.0, fw)
        an = dn*max(0.0,(1.0-0.1*abs(pn))**5) + max(0.0,-fn)
        as = ds*max(0.0,(1.0-0.1*abs(ps))**5) + max(0.0, fs)
        ap = ae+aw+an+as+ap0; bv = ap0*v(i,j); dv(i,j) = dx/ap

        ! solving equation
        vs(i,j) = 1/ap*(ae*v(i+1,j)+aw*v(i-1,j)+an*v(i,j+1)+as*v(i,j-1)+bv)+dv(i,j)*(p(i,j)-p(i,j+1))
        
     end do
  end do
  
end subroutine momentum_solver

! this is pressure correction equation coefficients computer
subroutine pce_coeff_computer()

  use params
  use model_vars
  
  implicit none

  do i = 2,npx-1
     do j = 2,npy-1
        aep(i,j) = rho*dy*du(i,j)
        awp(i,j) = rho*dy*du(i-1,j)
        anp(i,j) = rho*dx*dv(i,j)
        asp(i,j) = rho*dx*dv(i,j-1)
        app(i,j) = aep(i,j)+awp(i,j)+anp(i,j)+asp(i,j)
        bp(i,j) = rho*dy*(us(i-1,j)-us(i,j))+rho*dx*(vs(i,j-1)-vs(i,j))
     end do
  end do
  
end subroutine pce_coeff_computer

! this is pressure correction equation solution routine
subroutine pce_solver()

  use params
  use model_vars

  implicit none

  pprev = 0.0; pp = 0.0

  do iterate_p = 1,1000
     do i = 2,npx-1
        do j = 2,npy-1
           pp(i,j) = 1/app(i,j)*(aep(i,j)*pp(i+1,j)+awp(i,j)*pp(i-1,j)+anp(i,j)*pp(i,j+1)+asp(i,j)*pp(i,j-1)+bp(i,j))
        end do
     end do
     pp(1,:) = pp(2,:); pp(npx,:) = pp(npx-1,:)
     pp(:,1) = pp(:,2); pp(:,npy) = pp(:,npy-1)

     convergence_p = maxval(abs(pprev-pp)); pprev = pp

     if(convergence_p .le. 1e-7) then
        exit
     end if     
  end do  
  
end subroutine pce_solver

! this is pressure and velocity updater
subroutine pv_updater()

  use params
  use model_vars
  
  implicit none

  ! correcting pressure
  p = p + 0.1*pp

  ! correcting velocities
  do i = 2,nux-1
     do j = 2,nuy-1
        u(i,j) = us(i,j) + du(i,j)*(pp(i,j)-pp(i+1,j))
     end do
  end do

  do i = 2,nvx-1
     do j = 2,nvy-1
        v(i,j) = vs(i,j) + dv(i,j)*(pp(i,j)-pp(i,j+1))
     end do
  end do  
  
end subroutine pv_updater
