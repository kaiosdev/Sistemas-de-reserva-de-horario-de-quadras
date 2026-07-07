import tkinter as tk
from ui.interface import AthletixApp

def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    app = AthletixApp(root)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()