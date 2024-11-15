%% A/D converter :
[y, Fs] = audioread('project.wav',[1,2000]);
audio_normalized = y / max(abs(y));
audio_normalized_reshaped = audio_normalized(:);
audio_uint16 = typecast(audio_normalized_reshaped, 'uint16');audio_binary_temp = dec2bin(audio_uint16, 16);audio_with_noise = awgn(audio_normalized,16, 'measured', 'db'); % Add white Gaussian noise
audio_with_noise = awgn(audio_with_noise,16, 'measured', 'db'); % Add white Gaussian noise
audio_with_noise = awgn(audio_with_noise,16, 'measured', 'db'); % Add white Gaussian noiseaudio_with_noise = audio_normalized + audio_with_noise;audio_with_noise = (audio_with_noise .* audio_normalized)/10;
audio_binary = audio_binary_temp';
audio_with_noise = awgn(audio_with_noise,16, 'measured', 'db'); % Add white Gaussian noise
audio_with_noise = awgn(audio_with_noise,16, 'measured', 'db'); % Add white Gaussian noiseaudio_with_noise = audio_normalized + audio_with_noise;audio_with_noise = (audio_with_noise .* audio_normalized)/10;
audio_with_noise = conv(audio_normalized, audio_with_noise);
% audiowrite('noisy_audio.wav', audio_with_noise, Fs);
bits = audio_binary(:)';
% disp(length(audio_normalized_reshaped));
% disp(length(audio_uint16)/16);
% disp(length(bits));
% disp(bits);

% Constants and parameters
a = 0.5;  % Excess bandwidth
m = 4;    % Oversampling factor
n = 16;   % Length of raised cosine response (one-sided, multiple of symbol time)

num_bits=length(bits);
A=1;
symbols=zeros(1,num_bits/2);
index=1;
for k = 1:2:num_bits-1
    if((bits(k)==bits(k+1)) && bits(k)=='0')
        symbols(index)=A+A*1j;
    end
    if(bits(k)=='0' && bits(k+1)=='1')
        symbols(index)=A-A*1j;
    end
    if((bits(k)==bits(k+1)) && bits(k)=='1')
        symbols(index)=-A-A*1j;
    end
    if(bits(k)=='1' && bits(k+1)=='0')
        symbols(index)=-A+A*1j;
    end
    index=index+1;
end

Eb_N0_dB = 0:2:20; % Set the range of Eb/N0 values in dB
Eb_N0_linear = 10.^(Eb_N0_dB/10); 

% Calculate theoretical BER for QPSK in AWGN
BER_theo = 1/2 * erfc(sqrt(Eb_N0_linear/2));

%% Plotting BER vs. Eb/N0
figure;
semilogy(Eb_N0_dB, BER_theo, 'r-*');
title('BER Performance for QPSK in AWGN');
xlabel('Eb/N0 (dB)');
ylabel('Bit Error Rate');
grid on;

%% Calculating Power Efficiency
% Find the Eb/N0 value required for a target BER of 1e-6
target_BER = 1e-6;
Eb_N0_required = interp1(BER_theo, Eb_N0_dB, target_BER);

fprintf('Power Efficiency: Eb/N0 required for BER = 1e-6 is %.2f dB\n', Eb_N0_required);

% Plot QPSK constellation
figure;
scatter(real(symbols), imag(symbols), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('QPSK Constellation');
axis([-2 2 -2 2]);
grid on;
figure;
noise = randn(1,length(symbols)) + 1j * randn(1,length(symbols));
symbols_noise = symbols + noise;
scatter(real(symbols_noise), imag(symbols_noise), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('QPSK Constellation');
axis([-2 2 -2 2]);
grid on;

% Generate raised cosine pulse
figure;
subplot(3,1,1);
rc = raised_cosine(a, m, n);
length_rc = length(rc);
Tb = 0.1;
time_axis = 0 : Tb/length_rc : Tb-Tb/length_rc;
% disp(length(time_axis));
disp(length(rc)/Tb);
plot(time_axis, rc,'color','r');
xlabel("time");
ylabel("rc(t)");
title("RAISED COSINE");

% Generate Rectanfular pulse
rect = ones(1,length(time_axis)); % NRZ mode
symbols_upsampled = upsample(symbols,length(time_axis));

% Transmit filter response (convolution of symbols with raised cosine)
tx_raised_cosine = conv(symbols_upsampled, rc);
tx_rect = conv(symbols_upsampled,rect);
time_axis_line_coded = 0 : length(time_axis)/length_rc : length(tx_rect)-length(time_axis)/length_rc;
subplot(3,1,2);
plot(time_axis_line_coded, real(tx_raised_cosine),'Color','b');
xlabel("time");
ylabel("real(rc)");
title("READ PART OF RAISED COSINE LINE CODED SIGNAL");
   xlim([0,200]);

subplot(3,1,3);
plot(time_axis_line_coded, imag(tx_raised_cosine),'Color','b');
xlabel("time");
ylabel("imag(rc)");
title("IMAGINARY PART OF RAISED COSINE LINE CODED SIGNAL");
  xlim([0,200]);

figure;
subplot(2,1,1);
plot(time_axis_line_coded, real(tx_rect),'Color','g');
xlabel("time");
ylabel("imag(rect)");
title("IMAGINARY PART OF RECTANGULAR LINE CODED SIGNAL");
  xlim([0,2000]);

subplot(2,1,2);
plot(time_axis_line_coded, imag(tx_rect),'Color','b');
xlabel("time");
ylabel("imag(rect)");
title("IMAGINARY PART OF RECTANGULAR LINE CODED SIGNAL");
  xlim([0,2000]);
% specAn11 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn11(tx_raised_cosine); 
% 
% specAn12 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn12(tx_rect);
%% Modulation :
fc = 1e6;  % Carrier frequency (Hz)
Ac = 2;    % Carrier amplitude
wc = 2 * pi * fc;  % Carrier angular frequency
% Calculate the total time duration based on symbol duration (Tb) and
% number of symbolsq

% Modulate using Rectangular Pulse
x4_rect_I = Ac * real(tx_rect) .* cos(wc * time_axis_line_coded);
x4_rect_Q = Ac * imag(tx_rect) .* sin(wc * time_axis_line_coded);
x4_rect = x4_rect_I + x4_rect_Q;

% Modulate using Raised Cosine Pulse (assuming you have defined x3_raised_cosine)
x4_raised_cosine_I = Ac * real(tx_raised_cosine) .* cos(wc * time_axis_line_coded);
x4_raised_cosine_Q = Ac * imag(tx_raised_cosine) .* sin(wc * time_axis_line_coded);
x4_raised_cosine = x4_raised_cosine_I + x4_raised_cosine_Q;

% Plot Modulated Signals
figure;
subplot(2,1,1);
plot(time_axis_line_coded, x4_rect);
title('Modulated Signal (Rectangular Pulse)');
xlabel('Time (s)');
ylabel('Amplitude');
  xlim([0,200]);
grid on;

subplot(2,1,2);
plot(time_axis_line_coded, x4_raised_cosine);
title('Modulated Signal (Raised Cosine Pulse)');
xlabel('Time (s)');
ylabel('Amplitude');
  xlim([0,200]);
grid on;

figure;
scatter(x4_raised_cosine_I,x4_raised_cosine_Q , 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('AFTER MODULATION THROUGH CHANNEL (RAISED COSINE -MEMORYLESS)');
axis([-2 2 -2 2]);
grid on;

figure;
scatter(x4_rect_I,x4_rect_Q , 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('AFTER MODULATION THROUGH CHANNEL (RECTANGLE -MEMORYLESS)');
axis([-2 2 -2 2]);
grid on;

% specAn13 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn13(x4_rect);
% 
% specAn14 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn14(x4_raised_cosine);


num_bits=length(bits);
A=1;
symbols=zeros(1,num_bits/2);
index=1;
for k = 1:2:num_bits-1
    if((bits(k)==bits(k+1)) && bits(k)=='0')
        symbols(index)=A+A*1j;
    end
    if(bits(k)=='0' && bits(k+1)=='1')
        symbols(index)=A-A*1j;
    end
    if((bits(k)==bits(k+1)) && bits(k)=='1')
        symbols(index)=-A-A*1j;
    end
    if(bits(k)=='1' && bits(k+1)=='0')
        symbols(index)=-A+A*1j;
    end
    index=index+1;
end

noise_std_dev = 0.1; % Adjust this value to control the amount of noise
noise_real = noise_std_dev * randn(size(symbols));
noise_imag = noise_std_dev * randn(size(symbols));

symbols_with_noise = symbols + noise_real + 1j * noise_imag;

scatter(real(symbols_with_noise), imag(symbols_with_noise), 'filled');
hold on;
grid on;
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('QPSK-type-2 Constellation');
axis([-2 2 -2 2]);
%% MEMORYLESS CHANNEL 
% characterising noise
length_noise_sequence = length(x4_raised_cosine);
noise_variance = 1;
imag_index =  1;
real_part_noise = noise_variance * randn(1, length_noise_sequence);
imag_part_noise = noise_variance * randn(1, length_noise_sequence);

noise_memoryless = real_part_noise + 1j *imag_index * imag_part_noise;

% sending the signals into the memoryless channels
% 1) Rectangular modulated signal
r_rectangular_memoryless = x4_rect + noise_memoryless;
% 2) Raised Cosine modulated signal
r_raised_cosine = x4_raised_cosine + noise_memoryless;

figure;
subplot(2,2,1);
plot(time_axis_line_coded, real(r_raised_cosine),"Color",'r');
xlabel("time");
ylabel("channel output");
title("MEMORYLESS, RAISED COSINE OUTPUT from channel (REAL PART)");
 xlim([0,200]);

subplot(2,2,2);
plot(time_axis_line_coded, imag(r_raised_cosine),"Color",'r');
xlabel("time");
ylabel("channel output");
title("MEMORYLESS, RAISED COSINE OUTPUT from channel (IMAG PART)");
 xlim([0,200]);
subplot(2,2,3);
plot(time_axis_line_coded, real(r_rectangular_memoryless),"Color",'r');
xlabel("time");
ylabel("channel output");
title("MEMORYLESS, RECTANGULAR OUTPUT from channel (REAL PART)");
 xlim([0,200]);
subplot(2,2,4);
plot(time_axis_line_coded, imag(r_rectangular_memoryless),"Color",'r');
xlabel("time");
ylabel("channel output");
title("MEMORYLESS, RECTANGULAR OUTPUT from channel (IMAG PART)");
 xlim([0,200]);

 figure;
 scatter(real(r_raised_cosine), imag(r_raised_cosine), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('CHANNEL OUTPUT CONSTELLATION : MEMORYLESS (RAISED COSINE)');
axis([-2 2 -2 2]);
grid on;


figure;
 scatter(real(r_rectangular_memoryless), imag(r_rectangular_memoryless), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('CHANNEL OUTPUT CONSTELLATION : MEMORYLESS (RECTANGULAR)');
axis([-2 2 -2 2]);
grid on;



% specAn15 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn15(r_raised_cosine);
% 
% 
% specAn16 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn16(r_rectangular_memoryless);

%% AWGN CHANNEL WITH MEMORY
% impulse response h = a del(t) + (1-a) * del(t-bTb)
% constants a and b
a = 0.5;
b = 1;

% sending the signals into the channel with memory
% 1) Rectangular modulated signal
r_rectangular_memory = zeros(1, length_noise_sequence);
for k = 1 : length(r_rectangular_memory)
    if((k-b*length(time_axis)) >  0)
    r_rectangular_memory(k) = (a* x4_rect(k) + (1-a)* x4_rect(k-b*length(time_axis))) + noise_memoryless(k);
    else
        r_rectangular_memory(k) = a* x4_rect(k) + noise_memoryless(k);
    end
end


% 2) Raised Cosine modulated signal
r_raised_cosine_memory = zeros(1, length_noise_sequence);
for k = 1 : length(r_raised_cosine_memory)
    if((k > b* length(time_axis)))
        r_raised_cosine_memory(k) = ( a* x4_raised_cosine(k) + (1-a)* x4_raised_cosine(k-b*length(time_axis))) + noise_memoryless(k);
    else
        r_raised_cosine_memory(k) = a* x4_raised_cosine(k) + noise_memoryless(k);
    end
end

figure;
subplot(2,2,1);
plot(time_axis_line_coded, real(r_raised_cosine_memory),"Color",'b');
xlabel("time");
ylabel("channel output");
title("MEMORY, RAISED COSINE OUTPUT from channel (REAL PART)");
 xlim([0,200]);
subplot(2,2,2);
plot(time_axis_line_coded, imag(r_raised_cosine_memory),"Color",'b');
xlabel("time");
ylabel("channel output");
title("MEMORY, RAISED COSINE OUTPUT from channel (IMAG PART)");
 xlim([0,200]);
subplot(2,2,3);
plot(time_axis_line_coded, real(r_rectangular_memory),"Color",'b');
xlabel("time");
ylabel("channel output");
title("MEMORY, RECTANGULAR OUTPUT from channel (REAL PART)");
 xlim([0,200]);
subplot(2,2,4);
plot(time_axis_line_coded, imag(r_rectangular_memory),"Color",'b');
xlabel("time");
ylabel("channel output");
title("MEMORY, RECTANGULAR OUTPUT from channel (IMAG PART)");

figure;
 scatter(real(r_raised_cosine_memory), imag(r_raised_cosine_memory), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('CHANNEL OUTPUT CONSTELLATION : MEMORY (RAISED COSINE)');
axis([-2 2 -2 2]);
grid on;


figure;
 scatter(real(r_rectangular_memory), imag(r_rectangular_memory), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('CHANNEL OUTPUT CONSTELLATION : MEMORY (RECTANGULAR)');
axis([-2 2 -2 2]);
grid on;
%  xlim([0,200]);
% specAn17 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn17(r_raised_cosine_memory);
% 
% specAn18 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn18(r_rectangular_memory);


%% DEMODULATION : 
% trying to get real part
% from memoryless channel
% demodulating rect modulated signal
y_memoryless_rect_1 = 2 * r_rectangular_memoryless .* cos(2 * pi * fc * time_axis_line_coded);
y_memoryless_rect_2 = 2 * r_rectangular_memoryless .* sin(2 * pi * fc * time_axis_line_coded);
y_memoryless_rect_lpf_real = lowpass(y_memoryless_rect_1,Fs,fc);
y_memoryless_rect_lpf_imag = lowpass(y_memoryless_rect_2,Fs,fc);

figure;
subplot(2,1,1);
plot(time_axis_line_coded,real(y_memoryless_rect_lpf_real), 'color','r');
xlabel("time");
ylabel("demodulated signal");
title("REAL PART OF DEMODULATED RECT SIGNAL - MEMORYLESS");

subplot(2,1,2);
plot(time_axis_line_coded,real(y_memoryless_rect_lpf_imag), 'color','r');
xlabel("time");
ylabel("demodulated signal");
title("IMAG PART OF DEMODULATED RECT SIGNAL - MEMORYLESS");


% for raised cosine signal
y_memoryless_rect_3 = 2 * r_raised_cosine .* cos(2 * pi * fc * time_axis_line_coded);
y_memoryless_rect_4 = 2 * r_raised_cosine .* sin(2 * pi * fc * time_axis_line_coded);
y_memoryless_rc_lpf_real = lowpass(y_memoryless_rect_3,Fs,fc);
y_memoryless_rc_lpf_imag = lowpass(y_memoryless_rect_4,Fs,fc);

figure;
subplot(2,1,1);
plot(time_axis_line_coded,real(y_memoryless_rc_lpf_real), 'color','g');
xlabel("time");
ylabel("demodulated signal");
title("REAL PART OF DEMODULATED RAISED COSINE SIGNAL - MEMORYLESS");

subplot(2,1,2);
plot(time_axis_line_coded,real(y_memoryless_rc_lpf_imag), 'color','g');
xlabel("time");
ylabel("demodulated signal");
title("IMAG PART OF DEMODULATED RAISED COSINE SIGNAL - MEMORYLESS");

% specAn19 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn19(y_memoryless_rc_lpf_real);
% 
% specAn20 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn20(y_memoryless_rc_lpf_imag);
% 
% specAn21 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn21(y_memoryless_rect_lpf_real);
% 
% specAn22 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn22(y_memoryless_rect_lpf_imag);



% from memory channel
% demodulating rect modulated signal
y_memory_rect_1 = 2 * r_rectangular_memory .* cos(2 * pi * fc * time_axis_line_coded);
y_memory_rect_2 = 2 * r_rectangular_memory .* sin(2 * pi * fc * time_axis_line_coded);
y_memory_rect_lpf_real = lowpass(y_memory_rect_1,Fs,fc);
y_memory_rect_lpf_imag = lowpass(y_memory_rect_2,Fs,fc);

figure;
subplot(2,1,1);
plot(time_axis_line_coded,real(y_memory_rect_lpf_real), 'color','r');
xlabel("time");
ylabel("demodulated signal");
title("REAL PART OF DEMODULATED RECT SIGNAl - MEMORY");

subplot(2,1,2);
plot(time_axis_line_coded,real(y_memory_rect_lpf_imag), 'color','r');
xlabel("time");
ylabel("demodulated signal");
title("IMAG PART OF DEMODULATED RECT SIGNAL - MEMORY");


% for raised cosine signal
y_memory_rect_3 = 2 * r_raised_cosine .* cos(2 * pi * fc * time_axis_line_coded);
y_memory_rect_4 = 2 * r_raised_cosine .* sin(2 * pi * fc * time_axis_line_coded);
y_memory_rc_lpf_real = lowpass(y_memory_rect_3,Fs,fc);
y_memory_rc_lpf_imag = lowpass(y_memory_rect_4,Fs,fc);

figure;
subplot(2,1,1);
plot(time_axis_line_coded,real(y_memory_rc_lpf_real), 'color','g');
xlabel("time");
ylabel("demodulated signal");
title("REAL PART OF DEMODULATED RAISED COSINE SIGNAL - MEMORY");
 xlim([0,200]);
subplot(2,1,2);
plot(time_axis_line_coded,real(y_memory_rc_lpf_imag), 'color','g');
xlabel("time");
ylabel("demodulated signal");
title("IMAG PART OF DEMODULATED RAISED COSINE SIGNAL - MEMORY");
 xlim([0,200]);





 figure;
 scatter(real(y_memoryless_rc_lpf_real), imag(y_memoryless_rc_lpf_imag), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('DEMODULATED OUTPUT CONSTELLATION : MEMORYLESS (RAISED COSINE)');
axis([-2 2 -2 2]);
grid on;


figure;
 scatter(real(y_memoryless_rect_lpf_real), imag(y_memoryless_rect_lpf_imag), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('DEMODULATED OUTPUT CONSTELLATION : MEMORYLESS (RECTANGULAR)');
axis([-2 2 -2 2]);
grid on;


 figure;
 scatter(real(y_memory_rc_lpf_real), imag(y_memory_rc_lpf_imag), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('DEMODULATED OUTPUT CONSTELLATION : MEMORY (RAISED COSINE)');
axis([-2 2 -2 2]);
grid on;


figure;
 scatter(real(y_memory_rect_lpf_real), imag(y_memory_rect_lpf_imag), 'filled');
xlabel('In-phase Component');
ylabel('Quadrature Component');
title('DEMODULATED OUTPUT CONSTELLATION : MEMORY (RECTANGULAR)');
axis([-2 2 -2 2]);
grid on;


% specAn23 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn23(y_memory_rc_lpf_real);
% 
% specAn24 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn24(y_memory_rc_lpf_imag);
% 
% 
% specAn25 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn25(y_memory_rect_lpf_real);
% 
% 
% specAn26 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn26(y_memory_rc_lpf_real);
% 
% 
% specAn27 = spectrumAnalyzer("SampleRate", Fs, "Method","Filter bank","AveragingMethod","Exponential","Title", "PSD for transmitter filter o/p");
% specAn27(y_memory_rc_lpf_imag);


%% LINE DECODING
% Define the raised cosine filter as the matched filter
matched_filter = raised_cosine(a, m, n); % Assuming 'a', 'm', and 'n' are defined as in your script

% Normalize the filter to have unit energy
matched_filter = matched_filter / sqrt(sum(abs(matched_filter).^2));
% Convolve demodulated signal with matched filter
filtered_real_rc = conv(y_memory_rc_lpf_real, matched_filter, 'same');
filtered_imag_rc = conv(y_memory_rc_lpf_imag, matched_filter, 'same');

% convolve demodulated rectangular signal with matched filter
filtered_real_rect = conv(y_memory_rc_lpf_real, matched_filter, 'same');
filtered_imag_rect = conv(y_memory_rc_lpf_imag, matched_filter, 'same');


% Decision making to decode bits
decoded_bits_real_rc = zeros(1, length(filtered_real_rc));
threshold = 0;
for i = 1:length(filtered_real_rc)
    if filtered_real_rc(i) < threshold
        decoded_bits_real_rc(i) = -1;
    else
        decoded_bits_real_rc(i) = 1;
    end
end
% figure;
% plot(decoded_bits);


decoded_bits_imag_rc = zeros(1, length(filtered_imag_rc));
threshold = 0;

for i = 1:length(filtered_imag_rc)
    if filtered_imag_rc(i) < threshold
        decoded_bits_imag_rc(i) = -1;
    else
        decoded_bits_imag_rc(i) = 1;
    end
end

decoded_bits_real_rect = zeros(1, length(filtered_real_rect));
threshold = 0;
for i = 1:length(filtered_real_rect)
    if filtered_real_rect(i) < threshold
        decoded_bits_real_rect(i) = -1;
    else
        decoded_bits_real_rect(i) = 1;
    end
end

decoded_bits_imag_rect = zeros(1, length(filtered_imag_rect));
threshold = 0;

for i = 1:length(filtered_imag_rect)
    if filtered_imag_rect(i) < threshold
        decoded_bits_imag_rect(i) = -1;
    else
        decoded_bits_imag_rect(i) = 1;
    end
end
% disp(decoded_bits_imag_rect);

%% DECODING
% final bits 
% 1) For Raised Cosine
Final_decoded_bits_rc = zeros(1, 2 * length(decoded_bits_imag_rc));
for k = 1 : 2:length(Final_decoded_bits_rc)-1
    if (k+3)/2 <= length(decoded_bits_real_rc)
    Final_decoded_bits_rc(k) = decoded_bits_real_rc((k+1)/2);
    Final_decoded_bits_rc(k+1) = decoded_bits_imag_rc((k+3)/2);
    if(Final_decoded_bits_rc(k) == 1 && Final_decoded_bits_rc(k+1) == 1)
        Final_decoded_bits_rc(k) = 0;
        Final_decoded_bits_rc(k+1) = 0;
    end
     if(Final_decoded_bits_rc(k) == 1 && Final_decoded_bits_rc(k+1) == -1)
        Final_decoded_bits_rc(k) = 0;
        Final_decoded_bits_rc(k+1) = 1;
     end
      if(Final_decoded_bits_rc(k) == -1 && Final_decoded_bits_rc(k+1) == 1)
        Final_decoded_bits_rc(k) = 1;
        Final_decoded_bits_rc(k+1) = 0;
      end
       if(Final_decoded_bits_rc(k) == -1 && Final_decoded_bits_rc(k+1) == -1)
        Final_decoded_bits_rc(k) = 1;
        Final_decoded_bits_rc(k+1) = 1;
       end
    end
end


Final_decoded_bits_rect = zeros(1, 2 * length(decoded_bits_imag_rect));
for k = 1 : 2:length(Final_decoded_bits_rect)-1
    if (k+3)/2 <= length(decoded_bits_real_rect)
    Final_decoded_bits_rect(k) = decoded_bits_real_rect((k+1)/2);
    Final_decoded_bits_rect(k+1) = decoded_bits_imag_rect((k+3)/2);
     if(Final_decoded_bits_rc(k) == 1 && Final_decoded_bits_rc(k+1) == 1)
        Final_decoded_bits_rc(k) = 0;
        Final_decoded_bits_rc(k+1) = 0;
    end
     if(Final_decoded_bits_rc(k) == 1 && Final_decoded_bits_rc(k+1) == -1)
        Final_decoded_bits_rc(k) = 0;
        Final_decoded_bits_rc(k+1) = 1;
     end
      if(Final_decoded_bits_rc(k) == -1 && Final_decoded_bits_rc(k+1) == 1)
        Final_decoded_bits_rc(k) = 1;
        Final_decoded_bits_rc(k+1) = 0;
      end
       if(Final_decoded_bits_rc(k) == -1 && Final_decoded_bits_rc(k+1) == -1)
        Final_decoded_bits_rc(k) = 1;
        Final_decoded_bits_rc(k+1) = 1;
       end
    end
end

figure;
stem(Final_decoded_bits_rect,'filled');
xlabel("time");
ylabel("Decoded Bits");
title("DECODED BITS");

% For Final_decoded_bits_rc
binary_vector_rc = reshape(Final_decoded_bits_rc, [], 16); % Reshape into binary matrix
binary_string_rc = char(binary_vector_rc + '0'); % Convert binary matrix to string

% Convert binary string to decimal using base 2
% temp11 = bin2dec(binary_string_rc); % Convert binary to decimal
% temp21 = int16(temp11); % Typecast to int16
% temp41 = double(temp21); % Convert to double
% audio_reconstructed_normalized_rc = temp41 / 32767; % Normalize to [-1, 1]
% audiowrite('reconstructed_audio_rc.wav', audio_reconstructed_normalized_rc, Fs); % Save the reconstructed audio

% For Final_decoded_bits_rect
% binary_vector_rect = reshape(Final_decoded_bits_rect, [], 16); % Reshape into binary matrix
% binary_string_rect = char(binary_vector_rect + '0'); % Convert binary matrix to string

% % Convert binary string to decimal using base 2
% temp1 = bin2dec(binary_string_rect); % Convert binary to decimal
% temp2 = int16(temp1); % Typecast to int16
% temp4 = double(temp2); % Convert to double
% audio_reconstructed_normalized_rect = temp4 / 32767; % Normalize to [-1, 1]
% audiowrite('reconstructed_audio_rect.wav', audio_reconstructed_normalized_rect, Fs); % Save the reconstructed audio



function rc = raised_cosine(a,m,length)
os = floor(length*m);
w = custom_cumsum(ones(os,1))/m;
A= sin(pi*w)./(pi*w);B= cos(pi*a*w);C= 1 - (2*a*w).^2;
zerotest = m/(2*a);
if (~ (zerotest ~= floor(zerotest)))
B(zerotest) = pi*a;
C(zerotest) = 4*a;
end

D = (A.*B)./C;rc = [flipud(D);1;D];
end

function output = custom_cumsum(input)
    % Initialize output vector with the same size as input
    output = zeros(size(input));
    
    % Compute cumulative sum manually
    current_sum = 0;
    for i = 1:length(input)
        current_sum = current_sum + input(i);
        output(i) = current_sum;
    end
end




