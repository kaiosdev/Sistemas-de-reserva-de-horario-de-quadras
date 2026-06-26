import tkinter as tk
from ui.interface import AthletixApp

def main():
    # Inicializa a janela principal do Tkinter
    root = tk.Tk()
    
    # Instancia a classe que desenha a interface passando a janela root
    app = AthletixApp(root)
    
    # Inicia o loop de eventos para manter a tela aberta
    root.mainloop()

if __name__ == "__main__":
    main()