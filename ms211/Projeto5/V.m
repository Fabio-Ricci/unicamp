function v = V(deltaX, vmax, deltaS)
  v = (vmax/2)*(tanh((deltaX-deltaS)/20)+tanh(4));
endfunction
