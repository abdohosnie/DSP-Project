import matplotlib.pyplot as plt
import numpy as np

def read_signal(file_name):
    """
    Reads a signal file in the following format:
        <signal_type>
        <is_periodic>
        <num_samples>
        <index> <amplitude>
        ...
    """
    indices = []
    values = []
    with open(file_name, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]  # remove empty lines

    # Parse header
    if len(lines) < 3:
        raise ValueError(f"File {file_name} is incomplete or formatted incorrectly.")

    signal_type = int(lines[0])
    is_periodic = int(lines[1])
    num_samples = int(lines[2])

    # Parse samples
    for line in lines[3:]:
        parts = line.split()
        if len(parts) == 2:
            index, value = parts
            indices.append(int(index))
            values.append(float(value))

    # Check consistency
    if len(indices) != num_samples:
        print(f"⚠️ Warning: File {file_name} expected {num_samples} samples, but found {len(indices)}.")

    return indices, values


def plot_signal(indices, values, title="Signal"):
    plt.stem(indices, values, linefmt='g-', markerfmt='go', basefmt='k')  # Green for result
    plt.xlabel("n (sample index)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()

def display_signal(signal):
    indices = [sample[0] for sample in signal]
    values = [sample[1] for sample in signal]

    plt.figure()
    plt.stem(indices, values, use_line_collection=True)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.title('Signal Display')
    plt.grid(True)
    plt.show()


def add_signals(sig1, sig2):
    i1, x1 = sig1
    i2, x2 = sig2

    if not i1 or not i2:
        raise ValueError("One of the input signals is empty. Make sure both files contain data.")

    # create a combined index range
    min_index = min(min(i1), min(i2))
    max_index = max(max(i1), max(i2))
    new_indices = list(range(min_index, max_index + 1))

    y1 = np.zeros(len(new_indices))
    y2 = np.zeros(len(new_indices))

    for i, idx in enumerate(new_indices):
        if idx in i1:
            y1[i] = x1[i1.index(idx)]
        if idx in i2:
            y2[i] = x2[i2.index(idx)]

    result = y1 + y2
    return new_indices, list(result)


def multiply_signal(indices, samples, const):
    new_samples = [x * const for x in samples]
    return indices, new_samples


def subtract_signals(sig1, sig2):
    i2, x2 = multiply_signal(sig2[0], sig2[1], -1)
    return add_signals(sig1, (i2, x2))


def ShiftSignalByConst(indices, samples, k):
    shifted_indices = [i + k for i in indices]
    return shifted_indices, samples


def fold_signal(indices, samples):
    folded_indices = [-i for i in indices[::-1]]
    folded_samples = samples[::-1]
    return folded_indices, folded_samples


