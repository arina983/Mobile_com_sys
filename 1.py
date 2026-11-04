import numpy as np
import sounddevice as sd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

Fs = 1600
amp = 0.3

notes = {
    'G1': 392.00,
    'Eb1': 311.13,
    'Bb1': 466.16,
    'D2': 587.32,
    'Eb2': 622.26,
    'Gb2': 739.98,
    'G2': 784.00,
    'rest': 0
}

def note(name, duration):
    freq = notes[name]
    num_samples = int(Fs * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)

    if name == 'rest':
        return np.zeros(num_samples)

    wave = amp * np.sin(2 * np.pi * freq * t)

    fade_len = min(1000, num_samples // 4)
    fade = np.ones(num_samples)
    fade[-fade_len:] = np.linspace(1.0, 0.0, fade_len)

    return wave * fade

melody_data = [
    # Фраза 1
    ('G1', 0.5), ('G1', 0.5), ('G1', 0.5),('Eb1', 0.375), ('Bb1', 0.125),
    ('G1', 0.5), ('Eb1', 0.375), ('Bb1', 0.125), ('G1', 1.0), ('rest', 0.25),

    # Фраза 2
    ('D2', 0.5), ('D2', 0.5), ('D2', 0.5), ('Eb2', 0.375), ('Bb1', 0.125),
    ('Gb2', 0.5), ('Eb1', 0.375), ('Bb1', 0.125), ('G1', 1.0), ('rest', 0.25),

    # Повтор фразы 1
    ('G1', 0.5), ('G1', 0.5), ('G1', 0.5), ('Eb1', 0.375), ('Bb1', 0.125),
    ('G1', 0.5), ('Eb1', 0.375), ('Bb1', 0.125),('G1', 1.0), ('rest', 0.25),

    # Повтор фразы 2
    ('D2', 0.5), ('D2', 0.5), ('D2', 0.5), ('Eb2', 0.375), ('Bb1', 0.125),
    ('Gb2', 0.5), ('Eb1', 0.375), ('Bb1', 0.125), ('G1', 1.0),
]

song = np.concatenate([note(name, d) for name, d in melody_data])
sd.play(song, Fs)
sd.wait()

n = len(song)
fyrie = np.fft.fft(song)
freq = np.arange(n // 2) * Fs / n
amplitude = 2 * np.abs(fyrie[:n // 2]) / n

plt.figure(figsize=(14, 6))
plt.plot(freq, amplitude)
plt.title('Спектр сигнала (мелодия)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.xlim(0, 1600)
plt.grid(True)

plt.savefig('spectrum.png', dpi=150, bbox_inches='tight')   # сохраняем
print("График сохранён в spectrum.png")