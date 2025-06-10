import tkinter as tk
from tkinter import scrolledtext

class OutputBox:
    def __init__(self, parent: tk.Widget, height=20, width=100):
        self.text = scrolledtext.ScrolledText(parent, height=height, width=width, font=("Courier", 10), wrap="word", state="disabled")
        self.text.grid()

    def append(self, message: str):
        self.text.configure(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")

    def widget(self) -> tk.Widget:
        return self.text
