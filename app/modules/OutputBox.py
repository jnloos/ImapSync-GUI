import tkinter as tk
import threading
from queue import Empty, Queue
from tkinter import scrolledtext

class OutputBox:
    def __init__(self, parent: tk.Widget, height=20, width=100, max_lines=5000):
        self.text = scrolledtext.ScrolledText(parent, height=height, width=width, font=("Courier", 10), wrap="word", state="disabled")
        self.text.grid()
        self.max_lines = max_lines
        self._pending_messages: Queue[str] = Queue()
        self._flush_scheduled = False
        self._flush_lock = threading.Lock()

    def append(self, message: str):
        self._pending_messages.put(message)
        self.__schedule_flush()

    def __schedule_flush(self):
        with self._flush_lock:
            if self._flush_scheduled:
                return
            self._flush_scheduled = True
        self.text.after(0, self.__flush)

    def __flush(self):
        chunks: list[str] = []
        while True:
            try:
                chunks.append(self._pending_messages.get_nowait())
            except Empty:
                break

        if chunks:
            self.text.configure(state="normal")
            self.text.insert(tk.END, "\n".join(chunks) + "\n")
            self.__trim_if_needed()
            self.text.see(tk.END)
            self.text.configure(state="disabled")

        with self._flush_lock:
            self._flush_scheduled = False
            if not self._pending_messages.empty():
                self._flush_scheduled = True
                self.text.after(0, self.__flush)

    def __trim_if_needed(self):
        total_lines = int(self.text.index("end-1c").split(".")[0])
        if total_lines <= self.max_lines:
            return
        lines_to_remove = total_lines - self.max_lines
        self.text.delete("1.0", f"{lines_to_remove + 1}.0")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")
        while True:
            try:
                self._pending_messages.get_nowait()
            except Empty:
                break

    def widget(self) -> tk.Widget:
        return self.text
