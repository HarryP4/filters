
[y, Fs] = audioread("IFree_Test_Data_500KB_WAV.wav");
L = length(y) - 1;
t = (0:L);

figure
plot(t, y(:, 1))
grid on
hold on
plot(t, y(:, 2))
hold off

f = fft(y);

freq = Fs*((0:L)/L);

%figure
%plot(freq, f(:, 1))
%plot(freq, f(:, 2))