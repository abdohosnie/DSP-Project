import numpy as np

def generate_sine(amplitude, theta_deg, analog_freq, sampling_freq, duration=1.0):
    t = np.arange(0, duration, 1/sampling_freq)
    theta_rad = np.deg2rad(theta_deg)
    y = amplitude * np.sin(2 * np.pi * analog_freq * t + theta_rad)
    return t, y

def generate_cosine(amplitude, theta_deg, analog_freq, sampling_freq, duration=1.0):
    t = np.arange(0, duration, 1/sampling_freq)
    theta_rad = np.deg2rad(theta_deg)
    y = amplitude * np.cos(2 * np.pi * analog_freq * t + theta_rad)
    return t, y
