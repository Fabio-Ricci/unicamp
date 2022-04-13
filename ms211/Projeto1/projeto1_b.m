load DadosProjeto1_TurmaM.mat
n = 98;
alfa = 0.88;
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

b = zeros(n, 1)
b(2) = (alfa-1)/alfa;

x0 = ones(98, 1)
[x,Dr]=MetodoGaussSeidel(p,b,x0,30,0.001);

[max_values indice] = max(x)
RA(indice)