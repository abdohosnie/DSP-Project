import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from signal_generation import generate_sine, generate_cosine


# ----------------- Globals -----------------
signals = []        # list of (t, y, type)
fig = None
ax = None
canvas = None


# ----------------- Plot Functions -----------------
def plot_signals(mode):
    if not signals:
        messagebox.showwarning("No signals", "Generate at least one signal first!")
        return

    ax.clear()
    ax.grid(True)
    ax.set_title(f"Generated Signals ({mode} view)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    for i, (t, y, typ) in enumerate(signals):
        label = f"{typ.capitalize()} #{i+1}"
        if mode == 'discrete':
            ax.stem(t, y, basefmt=" ", markerfmt='o', label=label)
        else:
            ax.plot(t, y, label=label)

    ax.legend()
    canvas.draw()


def clear_plot():
    signals.clear()
    ax.clear()
    ax.grid(True)
    ax.set_title("Generated Signals")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    canvas.draw()


# ----------------- Generation -----------------
def generate_signal(signal_type):
    try:
        A = simpledialog.askfloat("Input", "Enter amplitude A:")
        theta = simpledialog.askfloat("Input", "Enter phase shift θ (degrees):")
        f = simpledialog.askfloat("Input", "Enter analog frequency f (Hz):")
        Fs = simpledialog.askfloat("Input", "Enter sampling frequency Fs (Hz):")
        duration = simpledialog.askfloat("Input", "Enter duration (seconds):", initialvalue=1.0)

        if None in [A, theta, f, Fs]:
            return

        # Nyquist theorem check
        if Fs < 2 * f:
            messagebox.showwarning("Warning", "Sampling frequency violates Nyquist theorem (Fs < 2f)!")

        if signal_type == "sine":
            t, y = generate_sine(A, theta, f, Fs, duration)
        else:
            t, y = generate_cosine(A, theta, f, Fs, duration)

        signals.append((t, y, signal_type))
        messagebox.showinfo("Success", f"{signal_type.capitalize()} wave generated successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Task 2 - Signal Generation")
root.geometry("850x600")

# --- Menu bar ---
menubar = Menu(root)
signal_menu = Menu(menubar, tearoff=0)
signal_menu.add_command(label="Generate Sine Wave", command=lambda: generate_signal("sine"))
signal_menu.add_command(label="Generate Cosine Wave", command=lambda: generate_signal("cosine"))
menubar.add_cascade(label="Signal Generation", menu=signal_menu)
root.config(menu=menubar)

# --- Control buttons ---
control_frame = tk.Frame(root, pady=10)
control_frame.pack()

tk.Button(control_frame, text="Display Discrete", command=lambda: plot_signals('discrete'),
          bg="#2196F3", fg="white", width=18).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="Display Continuous", command=lambda: plot_signals('continuous'),
          bg="#4CAF50", fg="white", width=18).grid(row=0, column=1, padx=5)
tk.Button(control_frame, text="Clear Plot", command=clear_plot,
          bg="red", fg="white", width=18).grid(row=0, column=2, padx=5)

# --- Matplotlib Figure ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title("Generated Signals")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()
