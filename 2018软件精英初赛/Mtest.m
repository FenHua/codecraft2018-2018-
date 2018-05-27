clear ;
%在[-3*pi,3*pi]生成50个数据点 sin(x)/x
n = 50 ;
x = linspace(-3,3,n)' ;
pix = pi * x ;
y = sin(pix) ./ (pix) + 0.1 * x + 0.05 * randn(n,1) ;

X = linspace(-3,3,100)' ;

A=(x'x)
%生成图像
hold on ;
axis([-2.8 2.8 -0.5 1.2]) ;
plot(X,F,'g-') ;
plot(x,y,'bo') ;