function [Jd, frames]=diffusion_filter(J,method,N,K,dt)
% [Jd, frames]=diffusion_filter(J,method,N,K,dt)
% Simulates N iterations of diffusion, parameters:
% J =  source image (2D gray-level matrix) for diffusion
% method =  'lin':  Linear diffusion (constant c=1).
%           'pm1': perona-malik, c=exp{-(|grad(J)|/K)^2} [PM90]
%           'pm2': perona-malik, c=1/{1+(|grad(J)|/K)^2} [PM90]
% N    number of iterations
% K    edge threshold parameter
% dt   time increment (0 < dt <= 0.25, default 0.2)
% Return values:
% Jd   diffused image size (height x width)
% frames  all intermediate frames (for video) of size (height x width x N+1)

if ~exist('N')
    N=50;
end
if ~exist('K')
    K=1;
end
if ~exist('dt')
    dt=0.2;
end

[Ny,Nx]=size(J); 

if (nargin<2) 
    error('not enough arguments (at least 2 should be given)');
end

% The idea is to implement the discretization from the penultimate slide of 
% Chapter 2: Diffusion filtering.
%
% Plugging in the discretizations from the lower two equations in the first equation 
% from that slide, and solving for u^{t+1} we arrive at the update:
%
% u^{t+1} = u^t + dt * (Ge .* Ie + Gw .* Iw + Gn .* In + Gs .* Is),
%
% with (Ie)_{i,j} = u^t_{i+1,j} - u^t_{i,j},
%      (Iw)_{i,j} = u^t_{i-1,j} - u^t_{i,j},
%      (In)_{i,j} = u^t_{i,j-1} - u^t_{i,j},
%      (Is)_{i,j} = u^t_{i,j+1} - u^t_{i,j},
% 
% and (Ge)_{i,j} = sqrt(g_{i+1,j} * g_{i,j}),
%     (Gw)_{i,j} = sqrt(g_{i-1,j} * g_{i,j}),
%     (Gn)_{i,j} = sqrt(g_{i,j-1} * g_{i,j}),
%     (Gs)_{i,j} = sqrt(g_{i,j+1} * g_{i,j}).
%

% create frames of video
frames = zeros(Ny, Nx, N + 1); 
frames(:, :, 1) = J; % first frame is input image
for i=1:N
    
    % calculate gradient magnitude for diffusivities (central differences)
    Iy=(J([2:end end],:)-J([1 1:end-1],:))/2;
    Ix=(J(:,[2:end end])-J(:,[1 1:end-1]))/2;
    D=(Ix.*Ix)+(Iy.*Iy);

    % calculate diffusivities
    if (method == 'lin')
        G=1;
    elseif (method == 'pm1')
        G=exp(-(D/K^2));
    elseif (method == 'pm2')
        G=1./(1+(D/K^2));
    else
        error(['Unknown method "' method '"']);
    end
    
    % calculate one-sided differences (north, south, east, west)
    In=J([1 1:end-1],:)-J;
    Is=J([2:end end],:)-J;
    Ie=J(:,[2:end end])-J;
    Iw=J(:,[1 1:end-1])-J;
    
    % calculate the corresponding diffusion weights
    gn = sqrt(G([1 1:end-1],:).*G);
    gs = sqrt(G([2:end end],:).*G);
    ge = sqrt(G(:,[2:end end]).*G);
    gw = sqrt(G(:,[1 1:end-1]).*G);

    % compute the update direction
    Jty = gn.*In + gs.*Is;
    Jtx = ge.*Ie + gw.*Iw;
    Jt = Jtx + Jty;
    
    % Next Image J
    J = J + Jt*dt;
    
    % Display image for debugging
    if rem(i, 20) == 0
        imshow(uint8(J));
    end

    % Update frame with current image
    frames(:, :, 1+i) = J;
    
end % for i

Jd = J;


%%%% Refs:
% [PM90] P. Perona, J. Malik, "Scale-space and edge detection using anisotropic diffusion", PAMI 12(7), pp. 629-639, 1990.
% [CLMC92] F. Catte, P. L. Lions, J. M. Morel and T. Coll, "Image selective smoothing and edge detection by nonlinear diffusion", SIAM J. Num. Anal., vol. 29, no. 1, pp. 182-193, 1992.
% [GSZ01] G. Gilboa, N. Sochen, Y. Y. Zeevi, "Complex Diffusion Processes for Image Filtering", Scale-Space 2001, LNCS 2106, pp. 299-307, Springer-Verlag 2001.
