import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Helper function to run another Python file
def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print("Running:", script_path)   # 👈 ADD THIS LINE
    if os.path.exists(script_path):
        subprocess.Popen([sys.executable, script_path])
    else:
        print("File not found:", script_path)


# Main menu window
def main_menu():
    root = tk.Tk()
    root.title("DSP Project Main Menu")
    root.geometry("400x350")
    root.config(bg="#222222")

    title_label = tk.Label(
        root,
        text="DSP Project",
        fg="white",
        bg="#222222",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=30)

    # Task 1 Button
    btn_task1 = tk.Button(
        root,
        text="Task 1 - Signal Operations",
        command=lambda: run_script("task1_main.py"),
        font=("Arial", 12),
        width=25,
        bg="#4CAF50",
        fg="white"
    )
    btn_task1.pack(pady=10)

    # Task 2 Button
    btn_task2 = tk.Button(
        root,
        text="Task 2 - Signal Generation",
        command=lambda: run_script("task2_main.py"),
        font=("Arial", 12),
        width=25,
        bg="#2196F3",
        fg="white"
    )
    btn_task2.pack(pady=10)

    # Task 3 Button (Quantization)
    btn_task3 = tk.Button(
        root,
        text="Task 3 - Quantization",
        command=lambda: run_script("task3_main.py"),
        font=("Arial", 12),
        width=25,
        bg="#FF9800",
        fg="white"
    )
    btn_task3.pack(pady=10)

    # Exit Button
    btn_exit = tk.Button(
        root,
        text="Exit",
        command=root.destroy,
        font=("Arial", 12),
        width=25,
        bg="#f44336",
        fg="white"
    )
    btn_exit.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
