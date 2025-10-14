import tkinter as tk
import subprocess
import sys
import os
from tkinter import messagebox


# Helper function to run another Python file
def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if os.path.exists(script_path):
        # Launch it using the same Python interpreter
        subprocess.Popen([sys.executable, script_path])
    else:
        tk.messagebox.showerror("Error", f"File not found:\n{script_path}")

# Main menu window
def main_menu():
    root = tk.Tk()
    root.title("DSP Project Main Menu")
    root.geometry("400x300")
    root.config(bg="#222222")

    title_label = tk.Label(root, text="DSP Project", fg="white", bg="#222222", font=("Arial", 20, "bold"))
    title_label.pack(pady=30)

    # Task 1 Button
    btn_task1 = tk.Button(
        root, text="Task 1 - Signal Operations",
        command=lambda: run_script("task1_main.py"),
        font=("Arial", 12), width=25, bg="#4CAF50", fg="white"
    )
    btn_task1.pack(pady=10)

    # Task 2 Button
    btn_task2 = tk.Button(
        root, text="Task 2 - Coming Soon",
        command=lambda: run_script("task2_main.py"),
        font=("Arial", 12), width=25, bg="#2196F3", fg="white"
    )
    btn_task2.pack(pady=10)

    # Exit button
    btn_exit = tk.Button(
        root, text="Exit",
        command=root.destroy,
        font=("Arial", 12), width=25, bg="#f44336", fg="white"
    )
    btn_exit.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
