import tkinter as tk
from app.Localization import __

class CredentialForm(tk.Frame):
    def __init__(self, master: tk.Widget, keys: list[str], **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.entries: dict[str, tk.Entry] = {}

        for i, key in enumerate(keys):
            label = tk.Label(self, text=__(f"fields.{key}"), anchor="w", bg="white")
            label.grid(row=i, column=0, sticky="w")
            entry = tk.Entry(self, show="*" if "password" in key else "", font=("Arial", 10))

            # Set default IMAP port
            if key == "port":
                entry.insert(0, "993")

            entry.grid(row=i, column=1, sticky="ew", padx=5, ipady=2)
            self.entries[key] = entry

        self.grid_columnconfigure(1, weight=1)

    def get_config(self) -> dict[str, str]:
        return {k: entry.get() for k, entry in self.entries.items()}
