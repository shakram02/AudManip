import wave


def trim(sound_file: wave.Wave_read, ratio, new_file_path):
    """
    Creates a new trimmed file out of the given one
    :param sound_file: Source file
    :param ratio: The ratio by which the function trims
    :param new_file_path: Path to the output file
    """
    frame_count = sound_file.getnframes()
    target_frame_count = int(frame_count * ratio)

    new_frames = sound_file.readframes(target_frame_count)
    new_file = wave.open(new_file_path, 'w')
    new_file.setparams(sound_file.getparams())
    new_file.writeframes(new_frames)
    new_file.close()


def main():
    file_path = input("Enter the path of the target file: ")
    ratio = float(input("Enter the ratio of the new file time to the old one: "))
    new_path = input("Enter the path of the new file:")
    sound_file = wave.open(file_path, 'r')
    trim(sound_file, ratio, new_path)


if __name__ == "__main__":
    main()
