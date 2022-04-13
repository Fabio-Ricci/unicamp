load DadosProjeto1_TurmaM.mat
n = 98;
alfa = 0.85;
v = 1/n;

p = zeros(n, n);
for i=1:n
  for j=1:n
    if s(j) == 0
      p(i, j) = 1/n;
    else
      p(i, j) = A(j, i)/s(j);
    endif
  endfor
endfor
for i=1:n
  p(i, i) = p(i, i) - 1/alfa;
endfor

b = ones(n, 1)*v*(alfa-1)/alfa;

x0 = ones(98, 1)
[x,Dr]=MetodoGaussSeidel(p,b,x0,30,0.001);

[max_values representante] = max(x);
RA(representante)
[max_values vice] = max(x(x<max(x)));
RA(vice)