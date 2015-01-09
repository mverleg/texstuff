
set terminal epslatex color colortext standalone
if (!exists("outname")) outname='plot.tex'
set output outname

plot '../fft_in.dat' using 1:2 with lines title 'Real signal', '' using 1:3 with lines title 'Imag signal'
set grid


