import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import os

# ===== Helper functions =====

def quantize_signal(signal, levels):
    """Quantize the input signal to the given number of levels."""
    x_min, x_max = np.min(signal), np.max(signal)
    q_levels = np.linspace(x_min, x_max, levels)
    q_signal = np.zeros_like(signal)

    for i in range(len(signal)):
        idx = np.argmin(np.abs(q_levels - signal[i]))
        q_signal[i] = q_levels[idx]

    quant_error = signal - q_signal
    return q_signal, quant_error


def load_signal_from_path(file_path):
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"Signal file not found:\n{file_path}")
        return None, None

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        N = int(lines[0].strip())
        indices, values = [], []

        for line in lines[1:N + 1]:
            parts = line.strip().split()
            if len(parts) == 2:
                indices.append(float(parts[0]))
                values.append(float(parts[1]))

        indices = np.array(indices)
        values = np.array(values)

        # Plot the loaded signal
        plt.figure(figsize=(8, 4))
        plt.plot(indices, values, color="blue", label="Original Signal")
        plt.title("Loaded Signal")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        return indices, values

    except Exception as e:
        messagebox.showerror("Error", f"Error reading file:\n{e}")
        return None, None


# ===== Main GUI =====

def task3_main():
    root = tk.Tk()
    root.title("Task 3 - Quantization")
    root.geometry("320x220")
    root.config(bg="#440000")

    file_path = "D:/Study/Level3/DSP/DSP-Tasks-master/DSP-Tasks/files/Task3.txt"

    indices, values = load_signal_from_path(file_path)
    if values is None:
        root.destroy()
        return

    def perform_quantization():
        """Triggered after entering levels and pressing the button."""
        try:
            levels = int(levels_entry.get())
            if levels <= 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of quantization levels.")
            return

        q_values, q_error = quantize_signal(values, levels)

        # Plot quantized signal and quantization error
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 1, 1)
        plt.plot(indices, values, label="Original Signal", color="blue")
        plt.step(indices, q_values, label="Quantized Signal", color="orange", where="mid")
        plt.title("Original vs Quantized Signal")
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(indices, q_error, label="Quantization Error", color="red")
        plt.title("Quantization Error")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    # ===== GUI Layout =====
    label = tk.Label(root, text="Enter Quantization Levels", bg="#440000", fg="white", font=("Arial", 12))
    label.pack(pady=15)

    levels_entry = tk.Entry(root, font=("Arial", 12))
    levels_entry.pack(pady=5)

    quant_btn = tk.Button(
        root, text="Quantize Signal",
        bg="#FFA500", fg="black", font=("Arial", 12),
        command=perform_quantization
    )
    quant_btn.pack(pady=10)

    exit_btn = tk.Button(
        root, text="Exit",
        bg="red", fg="white", font=("Arial", 12),
        command=root.destroy
    )
    exit_btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    task3_main()
