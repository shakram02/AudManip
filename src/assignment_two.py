import struct
import sys
from os import path

from bitarray import bitarray
from scipy.io.wavfile import read

from src.comapanders import MLawCompander
from src.utils import resample_at

FRAMING_BITS = bitarray('1111010000')  # As in PDF
SAMPLES_PER_FRAME = 10
NUM_USERS = 6
COMPANDING_COEFF = 10
TARGET_SAMPLE_RATE = 8000
M_LAW_COMPANDER = MLawCompander(COMPANDING_COEFF)


def main():
    base_path = "../assets/"

    rate, sound_file = read(path.join(base_path, "woman1_wb.wav"))
    resampled_data = resample_at(sound_file, rate, TARGET_SAMPLE_RATE)

    bit_streams = create_user_frames(resampled_data)
    tx_packets = create_packets_from_frames(bit_streams)
    rx_data = decode_packets(tx_packets)

    for user in sorted(rx_data.keys()):
        sound = rx_data[user]
        # TODO play sound


def pick_sample(sound_signal, sample_width=8):
    """
    Creates a sample from a given bitstream
    :param sound_signal: Array of bits containing voice data
    :param sample_width: width of the sample
    :return: the sample and the remaining items in the bit stream
    """
    sample = sound_signal[:sample_width]
    sound_signal = sound_signal[sample_width:]
    return sample, sound_signal


# Each frame consists of a sample from each
# user and True framing bit at the beginning of the frame
def make_frame(sound_sample: bitarray, sample_index):
    """
    Makes a frame given sample bits and user index
    :param sound_sample: bit array containing the sample
    :param sample_index: Index of the current sample in the frame
    :return: the frame containing sound sample and framing bit
    """
    return sound_sample.insert(FRAMING_BITS[sample_index])


def unwrap_and_check_frame(frame: bitarray, sample_index):
    """
    Takes the sound data out of the frame and verifies that the framing bit is correct
    :param frame: sound frame conainting a sample preceeded by a framing bit
    :param sample_index: index of the sample in the frame
    :return: Verification and sound sample
    """
    sound_sample = frame[1:]
    framing_bit = frame[0]
    return (framing_bit == FRAMING_BITS[sample_index]), sound_sample


def to_bit_stream(sound_file):
    bit_stream = None
    for sound_value in sound_file:
        if bit_stream is None:
            bit_stream = bitarray(sound_value)
        else:
            bit_stream += bitarray(sound_value)

    return bit_stream


def create_user_frames(user_sound_data):
    """
    Creates the framed samples for all users
    :param user_sound_data: raw sound data of all users
    :return: Every user and their framed samples
    """
    # Convert the file to a bitstream
    bit_stream = to_bit_stream(user_sound_data)

    sound_files = []
    out_data = {}

    for i in range(NUM_USERS):
        sound_files[i] = bit_stream

    while len(sound_files) != 0:
        # Take a frame from each user until the users are finished
        for i in range(NUM_USERS):

            if len(sound_files[i]) == 0:
                del (sound_files[i])

            # Get a sample, quantize it put it in the output buffer
            sample, sound_files[i] = pick_sample(sound_files[i])

            # Convert bits to integer
            sample_val = struct.unpack("<L", sample)[0]
            companded = M_LAW_COMPANDER.encode(sample_val)
            bits_companded = bitarray(companded)
            frame = make_frame(bits_companded, i)

            # Add the output frame to the out table
            # the output table contains a list of frames of all sampled data of users
            if out_data[i] is None:
                out_data[i] = [frame]
            else:
                # Add the new frame to the list
                out_data[i] += frame

    return out_data


def create_packets_from_frames(user_frames_table):
    """
    Create packets from all user frames
    U1: [ 1 2 3 4 ]
    U2: [ 1 2 3 4 ]
    U3: [ 1 2 3 4 ]

    Packet: [U1-1 U2-1 U3-1 ...etc]
    :param user_frames_table: Hashtable contianing user framed samples
    :return: List containing packets of the given data
    """
    data_packets = []  # All packets

    while len(user_frames_table) != 0:

        packet = []  # Packets for this loop
        for key in sorted(user_frames_table):
            user_frames = user_frames_table[key]
            if len(user_frames == 0):
                del user_frames_table[key]
                continue

            frame = user_frames.pop(0)
            packet += frame

        data_packets.append(packet)

    return data_packets


def decode_packets(frames):
    rx_data = {}
    user_rx_sample_index = {}  # Contains the processed number of smaples for each user

    for i, frame in enumerate(frames):
        user_index = i % NUM_USERS

        # Get the index of the sample to know which framing bit to use
        if user_rx_sample_index[user_index] is not None:
            sample_index_for_user = user_rx_sample_index[user_index]
        else:
            # Create a new entry in the hash table
            sample_index_for_user = 0
            user_rx_sample_index[user_index] = 0

        # Check the frame and extract sound data
        is_valid, sound_sample = unwrap_and_check_frame(frame, sample_index_for_user % SAMPLES_PER_FRAME)
        expanded_sample = M_LAW_COMPANDER.decode(sound_sample)

        if not is_valid:
            print("Invalid frame", file=sys.stderr)
            continue  # TODO

        # Put the
        if user_index in rx_data:
            rx_data[user_index] += expanded_sample
        else:
            rx_data[user_index] = [expanded_sample]

        # Increment processed sample count for user
        user_rx_sample_index[user_index] += 1

    return rx_data


if __name__ == "__main__":
    main()
