# Treinamento
load DadosTreinamento.mat;
mTr = 393;
n = 20;
d = 30;

W = randn(n,d);
b = randn(n,1);
Gtr = tanh(W*Xtr+b);

A = zeros(n, n);
b = zeros(n, 1);
# A*alfa = b
for i=1:n
  # Calculo de A
  for j=1:n
    for k=1:mTr
      A(i, j) = A(i, j) + Gtr(i, k)*Gtr(j, k);
    endfor
  endfor
  
  # Calculo de b
  for k=1:mTr
    b(i) = b(i) + ytr(k)*Gtr(i, k);  
  endfor
endfor
alfa = A\b;

# Teste
load DadosTeste.mat;

mTe = 176;
m = mTe;
x = Xte;
y = yte;

Wte = randn(n,d);
bte = randn(n,1);
s = RNA(alfa, Wte, bte, x);

L = -0.7;
nCorr = 0;
nErr = 0;
nMal = 0;
for k=1:m
  if L < s(k)
    s(k) = 1;
  else
    s(k) = -1;
  endif
  if s(k) == y(k)
    nCorr = nCorr + 1;
  endif
  if y(k) == 1
    nMal = nMal + 1;
    if s(k) == -1
      nErr = nErr + 1;  
    endif
  endif
endfor

AC = nCorr/m;
TFN = nErr/nMal;