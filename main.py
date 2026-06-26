import tkinter as tk
from ui.interface import AthletixApp

def main():
    root = tk.Tk()
    app = AthletixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()