import sys
import tkinter as tk
from Localization import Localization
from ImapSyncWindow import ImapSyncWindow


def main():
    # Load localization
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    Localization.load(lang)

    # Load window
    root = tk.Tk()
    ImapSyncWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()