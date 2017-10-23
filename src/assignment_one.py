from scipy.io.wavfile import read, write
from scipy.signal import resample
import numpy as np
import matplotlib.pyplot as plt
from src.utils import bin_search_index, create_time_axis

TARGET_SAMPLE_RATE = 8000


def resample_at(sound_data, src_sample_rate, out_sample_rate):
    """
    Calculates the number of points in a resampled audio file
    :param sound_data: Source file
    :param src_sample_rate: Intput sampling rate
    :param out_sample_rate: Desired output sampling rate
    :return: Number of data points that should be present
    """

    len_seconds = len(sound_data) / src_sample_rate
    sample_count = int(out_sample_rate * len_seconds)
    data = resample(sound_data, sample_count).tolist()

    # FIXME: why do we have to divide by sample count?
    return np.array([x / sample_count for x in data])


def quantize(sound_data: np.ndarray, levels):
    min_val, max_val = sound_data.min(), sound_data.max()
    delta = (max_val - min_val) / levels
    quantization_values = [(i + 1) * delta for i in range(levels)]

    quantized = []

    for sample in sound_data:

        # Find the quantization level that's just lower than the sample
        level_index = bin_search_index(quantization_values, sample)

        # # Approximate the sample to the best quantization level # #
        # The value is on the boundaries of the quantization levels, just add it as is
        if level_index == 0 or level_index == levels - 1:
            quantized.append(quantization_values[level_index])
            continue

        # Find the nearer quantization level
        # Note that the quantization values are sorted, so accesing level_index, and level_index+1
        # gives us the values that the sample are bound between
        lower_level = quantization_values[level_index]
        higher_level = quantization_values[level_index + 1]
        diff_low = abs(sample - lower_level)
        diff_high = abs(sample - higher_level)

        if diff_high > diff_low:
            # Closer to the lower level
            quantized.append(lower_level)
        else:
            # Closer to the higher level
            quantized.append(higher_level)

    return np.array(quantized)


def main():
    base_path = "../assets/"
    result_path = "../results/"
    from os import path

    rate, sound_file = read(path.join(base_path, "woman1_wb.wav"))
    resampled_data = resample_at(sound_file, rate, TARGET_SAMPLE_RATE)
    quantized = quantize(resampled_data, 256)

    plt.plot(create_time_axis(sound_file, TARGET_SAMPLE_RATE), sound_file)
    # plt.savefig(path.join(result_path, "original"))
    plt.show()

    write(path.join(base_path, "woman1_wb_quantized.wav"), TARGET_SAMPLE_RATE, quantized)


if __name__ == "__main__":
    main()
