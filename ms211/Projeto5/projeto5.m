n = 5;
h = 0.1;
a = 1;
vmax = 50;
deltaS = 42;
L = 1700; # Comprimento trajeto

# x = posicao
# x = velocidade
x = zeros(n);
v = zeros(n);
x(1, 1) = beta(0);
x(1, 2) = -14;
x(1, 3) = -18;
x(1, 4) = -26;
x(1, 5) = -31;
t = -h;

# Variaveis para guardar posicoes e tempos anteriores
k = 1;
graph_t = zeros(1, 300);
graph_x = zeros(4, 300);
graph_v = zeros(4, 300);
graph_t(k) = t;
graph_x(:, k) = x(2:n)';
graph_v(:, k) = v(2:n)';

# Vel max dos carros
max = zeros(1, n-1);

# p = Passo de Euler
while (x(5) < L)
  t = t + h;    
  # Atualiza posicao
  p = v;
  x = x + h*p;
  x(1) = beta(t); # onibus

  # Atualiza velocidade
  for i=2:n
    p(i) = a*(V(x(i - 1) - x(i), vmax, deltaS) - v(i));
  endfor
  v = v + h*p;
  
  # Atualiza vel max dos carros
  for i=2:n
    # Vel max
    if v(i) > max(i-1)
      max(i-1) = v(i)*3.6; # m/s para km/h
    endif
  endfor
  
  # Guarda os valores atuais para o gráfico
  k += 1;
  graph_t(k) = t;
  graph_x(:, k) = x(2:5)';
  graph_v(:, k) = v(2:5)';
endwhile
# Vel media dos carros
med = (x(2:n)/t)*3.6; # m/s para km/h

graph_x /= 1000; # transforma m para km na posicao

plot(graph_t, graph_x);
title("Gráfico 1 - Posição dos carros em função do tempo");
xlabel("Tempo (s)");
ylabel("Posição (km)");
#plot(graph_t, graph_v);
#title("Gráfico 2 - Velocidade dos carros em função do tempo");
#xlabel("Tempo (s)");
#ylabel("Velocidade (km/h)");