% read image and convert to double
% im = double(imread('lena.pgm'));
img = imread('test01.png');
size(img);
im = double(rgb2gray(img));
% im = imcrop(I);

% run diffusion process
iterations = 500;
[result, video] = diffusion_filter(im, 'pm1', iterations, 1, 0.1);

% show result
imshow(uint8(result));

verticalEdgeImage  = imfilter(result, [-1 0 1]);
imshow(uint8(verticalEdgeImage));

% write video to avi file
% v = VideoWriter('diffusion.avi', 'Uncompressed AVI');
% open(v);
% for i=1:size(video,3)
%     writeVideo(v, uint8(video(:,:,i)));
% end
% close(v);

