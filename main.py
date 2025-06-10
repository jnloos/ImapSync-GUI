import os
import sys
import tkinter as tk
from app.Localization import Localization
from app.ImapSyncWindow import ImapSyncWindow

def main():
    # Load translations
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    Localization.load(lang)

    # Load window
    root = tk.Tk()
    ImapSyncWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()