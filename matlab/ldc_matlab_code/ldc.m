% matlab code for staggered grid ldc problem
% developed by ramkumar

clc
clear

% geometry and meshing section---------------------------------------------
L = 0.01;
W = 0.01;
nx = 41;
ny = 41;

[X,Y] = meshgrid(linspace(0,L,nx),linspace(0,W,ny));
dx = X(1,2)-X(1,1);
dy = Y(2,1)-Y(1,1);

% staggered grid arrangement
npx = nx+1; npy = ny+1;
nux = npx-1; nuy = npy;
nvx = npx; nvy = npy-1;

% fluid flow variables section---------------------------------------------
rho = 1.225;
mu = 1.789e-5;
Re = 1000;
dt = 1e-3;

% computation variables section--------------------------------------------
u = zeros(nuy,nux); v = zeros(nvy,nvx); p = zeros(npy,npx);
Uplate = Re*mu/rho/L;
u(nuy,:) = Uplate;
us = u; vs = v; pp = p;
app = p; aep = p; awp = p; anp = p; asp = p; bp = p;
du = u; dv = v;
ap0 = rho*dx*dy/dt;

De = mu/dx*dy; Dw = De; Dn = mu/dy*dx; Ds = Dn;

% computation section------------------------------------------------------
for itr = 1:10000
   
    % x momentum equation solution
    for i = 2:nux-1
        for j = 2:nuy-1
            Fe = rho*dy*0.5*(u(j,i)+u(j,i+1));
            Fw = rho*dy*0.5*(u(j,i)+u(j,i-1));
            Fn = rho*dx*0.5*(v(j,i)+v(j,i+1));
            Fs = rho*dx*0.5*(v(j-1,i)+v(j-1,i+1));
            
            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds;
            
            ae = De*max(0,(1-0.1*abs(Pe))^5) + max(0,-Fe);
            aw = Dw*max(0,(1-0.1*abs(Pw))^5) + max(0, Fw);
            an = Dn*max(0,(1-0.1*abs(Pn))^5) + max(0,-Fn);
            as = Ds*max(0,(1-0.1*abs(Ps))^5) + max(0, Fs);
            ap = ae+aw+an+as+ap0;
            du(j,i) = dy/ap; bu = ap0*u(j,i);
            
            us(j,i) = 1/ap*(ae*u(j,i+1)+aw*u(j,i-1)+an*u(j+1,i)+as*u(j-1,i)+bu)+du(j,i)*(p(j,i)-p(j,i+1));
            
        end 
    end
    
    % y momentum equation solution
    for i = 2:nvx-1
        for j = 2:nvy-1
            Fe = rho*dy*0.5*(u(j,i)+u(j+1,i));
            Fw = rho*dy*0.5*(u(j,i-1)+u(j+1,i-1));
            Fn = rho*dx*0.5*(v(j,i)+v(j+1,i));
            Fs = rho*dx*0.5*(v(j,i)+v(j-1,i));
            
            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds;
            
            ae = De*max(0,(1-0.1*abs(Pe))^5) + max(0,-Fe);
            aw = Dw*max(0,(1-0.1*abs(Pw))^5) + max(0, Fw);
            an = Dn*max(0,(1-0.1*abs(Pn))^5) + max(0,-Fn);
            as = Ds*max(0,(1-0.1*abs(Ps))^5) + max(0, Fs);
            ap = ae+aw+an+as+ap0;
            dv(j,i) = dx/ap; bv = ap0*v(j,i);
            
            vs(j,i) = 1/ap*(ae*v(j,i+1)+aw*v(j,i-1)+an*v(j+1,i)+as*v(j-1,i)+bv)+dv(j,i)*(p(j,i)-p(j+1,i));
        end 
    end
    
    % pressure correction equation coefficients computation
    for i = 2:npx-1
        for j = 2:npy-1
            aep(j,i) = rho*dy*du(j,i);
            awp(j,i) = rho*dy*du(j,i-1);
            anp(j,i) = rho*dx*dv(j,i);
            asp(j,i) = rho*dx*dv(j-1,i);
            app(j,i) = aep(j,i)+awp(j,i)+anp(j,i)+asp(j,i);
            bp(j,i) = rho*dy*(us(j,i-1)-us(j,i))+rho*dx*(vs(j-1,i)-vs(j,i));
        end
    end
    
    % pressure correction equation solution
    pprev = pp*0; pp = pp*0;
    for iterate_p = 1:100
        for i = 2:npx-1
            for j = 2:npy-1
                pp(j,i) = 1/app(j,i)*(aep(j,i)*pp(j,i+1)+awp(j,i)*pp(j,i-1)+anp(j,i)*pp(j+1,i)+asp(j,i)*pp(j-1,i)+bp(j,i));                
            end
        end
        pp(:,1) = pp(:,2); pp(:,npx) = pp(:,npx-1);
        pp(1,:) = pp(2,:); pp(npy,:) = pp(npy-1,:);
        convergence_p = max(max(abs(pprev-pp))); pprev = pp;
        
        if convergence_p<1e-9
            break
        end
    end
    
    % pressure and velocity correction
    p = p + 0.1*pp;
    
    for i = 2:nux-1
        for j = 2:nuy-1
            u(j,i) = us(j,i) + du(j,i)*(pp(j,i)-pp(j,i+1));            
        end
    end
    for i = 2:nvx-1
        for j = 2:nvy-1
            v(j,i) = vs(j,i) + dv(j,i)*(pp(j,i)-pp(j+1,i));
        end
    end
    
    fprintf("\n Iteration : %d",itr);
    
    if max(max(isnan(pp)))
        fprintf("solution diveged");
        break
    end
    
end

% collocation section------------------------------------------------------
U = zeros(ny,nx); V=U; P=U;

U(1,:) = u(1,:);
U(ny,:) = u(nuy,:);
for j = 2:ny-1
    U(j,:) = 0.5*(u(j,:)+u(j+1,:));
end

V(:,1) = v(:,1);
V(:,nx) = v(:,nvx);
for i = 2:nx-1
    V(:,i) = 0.5*(v(:,i)+v(:,i+1));
end

for i = 1:nx
    for j = 1:ny
        P(j,i) = 0.25*(p(j,i+1)+p(j,i)+p(j+1,i)+p(j+1,i+1));
    end
end

% exporting data to csv file-----------------------------------------------
fid = fopen("Data.csv","w");

fprintf(fid,"X,Y,Z,U,V,P");
for i = 1:nx
    for j = 1:ny
        fprintf(fid,"\n%f,%f,%f,%f,%f,%f",X(j,i),Y(j,i),0.0,U(j,i),V(j,i),P(j,i));
    end 
end
fclose(fid);

% contours plotting section------------------------------------------------

figure
contourf(X,Y,sqrt(U.^2+V.^2),100,'edgecolor','none');
axis image;
colorbar;
colormap jet;
title("Velocity Magnitude Contour");

figure
contourf(X,Y,P,100,'edgecolor','none');
axis image;
colorbar;
colormap jet;
title("Pressure Contour")

figure
streamslice(X,Y,U,V,5);
axis image
title("Streamlines Contour");
