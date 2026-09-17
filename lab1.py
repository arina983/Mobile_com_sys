import matplotlib.pyplot as plt
import numpy as np
import wave
#from scipy.signal import decimate
import os
from scipy.io import wavfile
import sys

#1
#t = k*1/sample rate
f = 6
A = 4
t = []
sr = 200 #сколько точек времени на 1 секунду
for k in range(sr):
    t.append(k*(1/sr))
t = np.array(t)

y = A*np.sin(2*np.pi*f*t + np.pi/3)
#4
fs = 12 #3 по т. Котельникова
t_disc = []
for k in range(fs):
    t_disc.append(k*(1/fs))
t_disc = np.array(t_disc)

y_disc = A * np.sin(2 * np.pi * f * t_disc + np.pi/3)
n = len(y_disc)
# fyrie = np.fft.fft(y_disc)
# print(fyrie)
#5
fyrie = []
for x in range(n):
    sum = 0
    for time in range(n):
        sum = sum + y_disc[time]*np.exp(-1j*2*np.pi*x*time/n)
    fyrie.append(sum)
fyrie = np.array(fyrie)
print(fyrie)

print(f"Всего данных: {y_disc.nbytes} байт")
print(f"Один элемент: {y_disc.itemsize} байт")
print('---------------------')

#7
fs_2 = 48
t_disc_2 = []
for k in range(fs_2):
    t_disc_2.append(k*(1/fs_2))
t_disc_2 = np.array(t_disc_2)

y_disc_2 = A * np.sin(2 * np.pi * f * t_disc_2 + np.pi/3)
n_2 = len(y_disc_2)

fyrie_2 = []
for x in range(n_2):
    sum = 0
    for time in range(n_2):
        sum = sum + y_disc_2[time]*np.exp(-1j*2*np.pi*x*time/n_2)
    fyrie_2.append(sum)
fyrie_2 = np.array(fyrie_2)
print(fyrie_2)
print('---------------------------')

plt.figure(figsize=(12, 6), label = 'графики непрерывного сигнала')
plt.plot(t, y, label = 'непрерывный')
#6
plt.plot(t_disc, y_disc, label = 'оцифрованный')
#7
plt.plot(t_disc_2, y_disc_2, label = 'частота дискретизации x4')
plt.xlabel('t')
plt.ylabel('A')
plt.legend()
plt.grid(True)
#9
with wave.open('voice.wav', 'rb') as wav_file:
    Fs = wav_file.getframerate()  #частота дискретизации
    N = wav_file.getnframes() #количество элементов в файле
    duration = N/ Fs
    raw = wav_file.readframes(N) #чтение данных
print(Fs, duration, N)
y_11 = np.frombuffer(raw, dtype =np.int16)
#10
Fs_opr = N/duration
print(f'частота дискретизации(посчитана вручную)', Fs_opr)
#11
#reduced_signal = decimate(y_11, 10)
reduced_signal = y_11[::10]

t_voice_11 = np.arange(len(y_11))/Fs
plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
plt.title('Оригинал голоса')
plt.plot(t_voice_11, y_11)
plt.xlabel('Время, с')
plt.ylabel('Амплитуда')

Fs1 = Fs // 10 #у прореженного новая частота дискретизации
t_voice = np.arange(len(reduced_signal))/Fs1
plt.subplot(2, 1, 2)
plt.title('Прореженный голос')
plt.plot(t_voice, reduced_signal)
plt.xlabel('Время, с')
plt.ylabel('Амплитуда')
plt.tight_layout()

wavfile.write('voice_downsampled.wav', Fs1, reduced_signal.astype(np.int16))
os.system('explorer.exe voice_downsampled.wav')

#12
#для оригинального
n_voice = len(y_11)
# fyrie_voice = []
# for x in range(n_voice):
#     sum = 0
#     for t_voice in range(n_voice):
#         sum = sum + y_11[t_voice]*np.exp(-1j*2*np.pi*x*t_voice/n_voice)
#     fyrie_voice.append(sum)
# fyrie_voice = np.array(fyrie_voice)
# print(fyrie_voice) #комплексная амплитуда надо перевести
fyrie_voice = np.fft.fft(y_11)
f_x = np.arange(n_voice//2)*Fs/n_voice
ampl = np.abs(fyrie_voice[:n_voice//2])/n_voice #делим чтобы амплитуда не зависела от длины сигнала

plt.figure(figsize = (14, 9))
plt.subplot(2, 1, 1)
plt.plot(f_x, ampl)
plt.title('Спектр оригинала голоса')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.grid(True)

#для прореженного
n_voice2 = len(reduced_signal)
# fyrie_voice2 = []
# for x in range(n_voice2):
#     sum = 0
#     for t_voice_11 in range(n_voice2):
#         sum = sum + reduced_signal[t_voice_11]*np.exp(-1j*2*np.pi*x*t_voice_11/n_voice2)
#     fyrie_voice2.append(sum)
# fyrie_voice2 = np.array(fyrie_voice2)
# print(fyrie_voice2)
fyrie_voice2 = np.fft.fft(reduced_signal)

f_x2 = np.arange(n_voice2//2)*Fs1/n_voice2
ampl2 = np.abs(fyrie_voice2[:n_voice2//2])/n_voice2
plt.subplot(2, 1, 2)
plt.plot(f_x2, ampl2)
plt.title('Спектр прореженного голоса')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.grid(True)

#13
def quantize(signal, bits):
    levels = 2 ** bits - 1
    s_min = np.min(signal)
    s_max = np.max(signal)
    signal_norm = (signal - s_min) / (s_max - s_min) * levels
    signal_quant = np.round(signal_norm) # округляем до целых чисел (квантование)
    return signal_quant
signal = y.copy()

fig13, axes13 = plt.subplots(5, 1, figsize=(12, 12))

spectrum_orig = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(signal), d=1 / fs)
half = len(freqs) // 2

axes13[0].plot(freqs[:half], np.abs(spectrum_orig[:half]) / len(signal), 'r', label='без квантования')
axes13[0].set_title('Спектр исходной синусоиды (без квантования)')
axes13[0].set_xlabel('Частота, Гц')
axes13[0].set_ylabel('Амплитуда')
axes13[0].grid(True)
axes13[0].legend()

print("Средние ошибки квантования:")
i = 1
for bits in [3, 4, 5, 6]:
    y_q = quantize(signal, bits)
    error = np.mean(np.abs(signal - y_q))
    print(f"{bits} бит, средняя ошибка = {error:.3f}")
    spectrum_q = np.fft.fft(y_q)

    axes13[i].plot(freqs[:half], np.abs(spectrum_q[:half]) / len(y_q), label=f'{bits} бит')
    axes13[i].set_title(f'Спектр после квантования ({bits} бит)')
    axes13[i].set_xlabel('Частота, Гц')
    axes13[i].set_ylabel('Амплитуда')
    axes13[i].grid(True)
    axes13[i].legend()
    i += 1

plt.tight_layout()
plt.show()