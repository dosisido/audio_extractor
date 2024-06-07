import tkinter as tk
from tkinter import filedialog

from typing import Tuple


def get_file_path(file_types: Tuple[Tuple[str, str]] =(("All files", "*.*"),)):
    # Create a Tkinter root widget
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Open a file dialog and ask the user to select a file
    file_path = filedialog.askopenfilename(
        filetypes=file_types,
        title="Select a file"
    )
    
    # Destroy the root widget after the file dialog is closed
    
    root.destroy()
    return file_path