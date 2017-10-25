from pydub import AudioSegment, playback
from scipy.fftpack import rfft, irfft, fftfreq
import os
import pylab as plt
import numpy as np
import wave
import sys


def main():
    # time = np.linspace(0, 10, 2000)
    # signal = np.cos(5 * np.pi * time) + np.cos(7 * np.pi * time)
    #
    # W = fftfreq(signal.size, d=time[1] - time[0])
    # f_signal = rfft(signal)
    #
    # # If our original signal time was in seconds, this is now in Hz
    # cut_f_signal = f_signal.copy()
    # cut_f_signal[(W < 6)] = 0
    #
    # cut_signal = irfft(cut_f_signal)
    # plt.subplot(221)
    # plt.plot(time, signal)
    # plt.subplot(222)
    # plt.plot(W, f_signal)
    # plt.xlim(0, 20)
    # plt.subplot(224)
    # plt.plot(W, cut_f_signal)
    # plt.xlim(0, 10)
    # plt.subplot(223)
    # plt.plot(time, cut_signal)
    # plt.show()

    file_path = input("Enter full path of the file: ")
    file_name, file_extension = os.path.splitext(file_path)

    file_extension = file_extension[1:]  # Remove the '.' in the file extension
    print("Will process:", os.path.basename(file_name))

    audio = AudioSegment.from_file(file_path, file_extension)

    audio += 20

    converted = file_name + "-converted" + ".mp3"
    audio.export(converted)
    pass


if __name__ == "__main__":
    main()
