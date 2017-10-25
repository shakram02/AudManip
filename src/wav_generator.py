import numpy as np
import wave
import sys
import matplotlib.pyplot as plt


def main():
    fs = 44100  # sample rate, should be 2*fmax
    duration = 10  # duration in seconds
    freq = 400  # in Hertz

    time = np.arange(fs * duration) * (freq / fs)  # why f/fs?
    signal = (np.sin(2 * np.pi * time)).astype(np.float32)

    plt.plot(time, signal)
    plt.show()

    wav_file = wave.open('../results/singal_{}_hz.wav'.format(freq), 'w')

    sample_size = int(sys.getsizeof(signal) / (duration * fs))
    wav_file.setnchannels(1)
    wav_file.setsampwidth(sample_size)
    wav_file.setframerate(fs)
    wav_file.setnframes(fs * duration)

    wav_file.writeframesraw(signal)
    wav_file.close()

    pass


if __name__ == "__main__":
    main()
