import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from signal_operations import *
import importlib.util, ast, types, sys

from signal_operations import (
    ShiftSignalByConst
)



# --- Safe loader for test_functions.py (ignores top-level code) ---
def safe_import_test_functions(path="test_functions.py"):
    with open(path, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    new_body = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom))]
    tree.body = new_body
    compiled = compile(tree, path, "exec")

    module = types.ModuleType("test_functions")
    sys.modules["test_functions"] = module
    exec(compiled, module.__dict__)
    return module

test_functions = safe_import_test_functions()

# --- Globals ---
signal1 = None
signal2 = None

# --- Helper plotting function ---
def plot_signal(indices, samples, title, color='b'):
    plt.figure()

    # Matplotlib expects short color codes for formats, not full color names
    color_map = {
        'blue': 'b',
        'red': 'r',
        'green': 'g',
        'orange': 'orange',  # allow full color name, handle separately
    }

    fmt_color = color_map.get(color, color)  # fallback to original if not mapped

    # Use proper color arguments (not concatenation)
    plt.stem(indices, samples, linefmt=fmt_color, markerfmt='o', basefmt='gray')
    plt.setp(plt.gca().lines, color=color)  # ensure full color names still work

    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()


# --- GUI functions ---
def load_signal(num):
    global signal1, signal2
    file_path = filedialog.askopenfilename(title=f"Select Signal {num} File", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    try:
        sig = read_signal(file_path)
        if num == 1:
            signal1 = sig
        else:
            signal2 = sig
        messagebox.showinfo("Loaded", f"Signal {num} loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Signal {num}:\n{e}")

def display_signals():
    global signal1, signal2
    if not signal1 and not signal2:
        messagebox.showwarning("Warning", "No signals loaded yet!")
        return

    plt.figure()

    if signal1:
        plt.stem(signal1[0], signal1[1], linefmt='b-', markerfmt='bo', basefmt='gray', label="Signal 1")
    if signal2:
        plt.stem(signal2[0], signal2[1], linefmt='orange', markerfmt='o', basefmt='gray', label="Signal 2")

    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.title("Loaded Signals")
    plt.legend()
    plt.grid(True)
    plt.show()


def perform_addition():
    global signal1, signal2
    if not signal1 or not signal2:
        messagebox.showwarning("Warning", "Please load both signals first!")
        return
    indices, samples = add_signals(signal1, signal2)
    plot_signal(indices, samples, "Addition Result", color='green')
    try:
        test_functions.AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", indices, samples)
    except Exception as e:
        print(f"⚠️ Add test failed: {e}")

def perform_subtraction():
    global signal1, signal2
    if not signal1 or not signal2:
        messagebox.showwarning("Warning", "Please load both signals first!")
        return
    indices, samples = subtract_signals(signal1, signal2)
    plot_signal(indices, samples, "Subtraction Result", color='green')
    try:
        test_functions.SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", indices, samples)
    except Exception as e:
        print(f"⚠️ Sub test failed: {e}")

def perform_multiplication():
    global signal1
    if not signal1:
        messagebox.showwarning("Warning", "Please load Signal 1 first!")
        return
    const = simpledialog.askfloat("Multiply", "Enter constant value:")
    if const is None:
        return
    indices, samples = multiply_signal(signal1[0], signal1[1], const)
    plot_signal(indices, samples, f"Signal * {const}", color='green')
    try:
        test_functions.MultiplySignalByConst(const, indices, samples)
    except Exception as e:
        print(f"⚠️ Multiply test failed: {e}")

def perform_shift():
    if signal1:
        k = simpledialog.askinteger("Shift Signal", "Enter the shift value (positive or negative):")
        if k is not None:
            indices, samples = ShiftSignalByConst(signal1[0], signal1[1], k)
            plot_signal(indices, samples, "Shifted Signal")
            messagebox.showinfo("Shift", f"Signal shifted by {k}")
    else:
        messagebox.showerror("Error", "Please load a signal first.")


def perform_fold():
    global signal1
    if not signal1:
        messagebox.showwarning("Warning", "Please load Signal 1 first!")
        return
    indices, samples = fold_signal(signal1[0], signal1[1])
    plot_signal(indices, samples, "Folded Signal", color='green')
    try:
        test_functions.Folding(indices, samples)
    except Exception as e:
        print(f"⚠️ Fold test failed: {e}")

# --- GUI Layout ---
root = tk.Tk()
root.title("Task 1")
root.geometry("400x460")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="DSP Signal Operations", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(frame, text="Load Signal 1", command=lambda: load_signal(1), width=25).pack(pady=5)
tk.Button(frame, text="Load Signal 2", command=lambda: load_signal(2), width=25).pack(pady=5)
tk.Button(frame, text="Display Signals", command=display_signals, width=25).pack(pady=5)

tk.Button(frame, text="Add Signals", command=perform_addition, width=25).pack(pady=5)
tk.Button(frame, text="Subtract Signals", command=perform_subtraction, width=25).pack(pady=5)
tk.Button(frame, text="Multiply Signal", command=perform_multiplication, width=25).pack(pady=5)
tk.Button(frame, text="Shift Signal", command=perform_shift, width=25).pack(pady=5)
tk.Button(frame, text="Fold Signal", command=perform_fold, width=25).pack(pady=5)
tk.Button(frame, text="Exit", command=root.destroy, width=25, bg="red", fg="white").pack(pady=10)

root.mainloop()
