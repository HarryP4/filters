
[y, Fs] = audioread("IFree_Test_Data_500KB_WAV.wav");
L = length(y) - 1;
t = (0:L);

figure
subplot 211
grid on
plot(t, y(:, 1))

subplot 212
plot(t, y(:, 2))
title("Left and Right Channel Signal Compression = 1")
xlabel("Sample")
ylabel("Magnitude")





f = fft(y);

freq = Fs*((0:L)/L);

figure
plot(freq, f(:, 1))
plot(freq, f(:, 2))
title("Frequency Response Compression = 1")
xlabel("Frequency")
ylabel("Magnitude")




