from scipy.io.wavfile import read, write
from scipy.signal import resample
import numpy as np
import matplotlib.pyplot as plt
from src.utils import bin_search_index, create_time_axis
from os import path

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
    error_pwr2 = 0
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
            error_pwr2 += (diff_low ** 2)
        else:
            # Closer to the higher level
            quantized.append(higher_level)
            error_pwr2 += (diff_high ** 2)

    return np.array(quantized), error_pwr2


def q_3(sound_data, base_path):
    import src.comapanders

    uniform_quantized, err_pwr2 = quantize(sound_data, 256)
    sample_count = len(sound_data)
    print("Uniform mean err:", err_pwr2 / sample_count, " Using 256 levels")

    for (a_lvls, m_lvls) in [(10, 10), (87.6, 255), (1000, 1000)]:
        a_law_compander = src.comapanders.ALawCompander(a_lvls)
        a_law_signal, a_law_sq_err = a_law_compander.encode(sound_data)

        m_law_compander = src.comapanders.MLawCompander(m_lvls)
        m_law_signal, m_law_sq_err = m_law_compander.encode(sound_data)
        print("A-Law mean err:", a_law_sq_err / sample_count, " at A:", a_lvls)
        print("M-Law mean err:", m_law_sq_err / sample_count, " at M:", m_lvls)

        # write(path.join(base_path, "woman1_wb_quantized.wav"), TARGET_SAMPLE_RATE, uniform_quantized)


def main():
    base_path = "../assets/"
    result_path = "../results/"

    rate, sound_file = read(path.join(base_path, "woman1_wb.wav"))
    resampled_data = resample_at(sound_file, rate, TARGET_SAMPLE_RATE)
    q_3(resampled_data, base_path)

    plt.plot(create_time_axis(sound_file, TARGET_SAMPLE_RATE), sound_file)
    # plt.savefig(path.join(result_path, "original"))
    plt.show()


if __name__ == "__main__":
    main()
