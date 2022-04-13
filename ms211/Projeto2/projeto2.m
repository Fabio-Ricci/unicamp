[y,fs] = audioread("AudioEco.wav");

n = length(y);
duracao = n/fs;
deltaT = fs;

x = y
for i=1:n
  for k=2:ceil(i/deltaT)
    x(i) = x(i) - x(i-(k-1)*deltaT);
  endfor
endfor

plot([0:n-1]/fs,x);
axis([0 15 -1 1]);
grid
[x,fs] = sound(x,fs);