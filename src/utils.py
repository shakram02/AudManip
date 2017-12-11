import numpy as np
from scipy.signal import resample


def bin_search_index(sorted_array, value, base_index=None):
    """
    Finds the quantization level closest to the given value and
    returns its INDEX in the input array
    :param sorted_array: Array of available quantization levels
    :param value: Value of the current sample
    :param base_index: Base index used with recursion
    :return: INDEX of the quantization level closest to the sample
    """

    if base_index is None:
        base_index = 0

    mid_len = len(sorted_array) // 2
    full_len = len(sorted_array)

    array_min, array_max, array_mid = sorted_array[0], sorted_array[-1], sorted_array[mid_len]

    if value >= array_max:
        return base_index + (full_len - 1)

    if value <= array_min:
        return base_index

    if value == array_mid:
        return base_index + mid_len

    if full_len == 1:
        return base_index

        # do binary search
    if value < array_mid:
        # Search the lower half
        return bin_search_index(sorted_array[:mid_len], value, base_index)

    if value > array_mid:
        # Search the upper half
        return bin_search_index(sorted_array[mid_len:], base_index + mid_len)


def create_time_axis(sound_data, sample_rate):
    return [i / sample_rate for i in range(len(sound_data))]


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
