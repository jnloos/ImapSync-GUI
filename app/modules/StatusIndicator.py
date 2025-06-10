import tkinter as tk

class StatusIndicator:
    COLORS = {
        'neutral': '#cccccc',
        'success': '#0A9B31',
        'failure': '#FF0000',
    }

    def __init__(self, parent: tk.Widget, row: int, column: int, **grid_options):
        self.dot = tk.Label(parent, text='\u25CF', fg=self.COLORS['neutral'], bg=parent.cget('bg'))
        self.dot.grid(row=row, column=column, **grid_options)

    def set_status(self, status: str) -> None:
        color = self.COLORS.get(status, self.COLORS['neutral'])
        self.dot.config(fg=color)

