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
