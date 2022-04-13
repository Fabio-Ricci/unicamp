x0 = 10;
Niter = 30;
tol = 0.01;
for i=1:Niter
  x=x0-f(x0)/df(x0);
  if (f(x0)==0 | abs(x-x0)<tol)
    return;
  else
    epsilon=abs(x-x0);
    x0=x;
  endif
endfor