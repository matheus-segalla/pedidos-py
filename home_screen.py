from tkinter import Tk, Button, Label
import subprocess

class TelaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Tela Principal")
        self.master.geometry("600x400")

        self.label = Label(self.master, text="Tela Principal")
        self.label.pack()

        self.btn_opcao1 = Button(self.master, text="PRODUTOS", command=self.abrir_tela_opcao1, width=25, height=5)
        self.btn_opcao1.pack(side="left", padx=10)

        self.btn_opcao2 = Button(self.master, text="PEDIDOS", command=self.abrir_tela_opcao2, width=25, height=5)
        self.btn_opcao2.pack(side="left", padx=10)

        self.btn_opcao3 = Button(self.master, text="CLIENTES", command=self.abrir_tela_opcao3, width=25, height=5)
        self.btn_opcao3.pack(side="left", padx=10)

    def abrir_tela_opcao1(self):
       self.label.config(text="Opção 1 selecionada")
       subprocess.run(["python", "main.py"])
        
    def abrir_tela_opcao2(self):
        self.label.config(text="Opção 2 selecionada")
        subprocess.run(["python", "pedidos.py"])
        
    def processar_pedido(self, pedido):
        print(f"Pedido recebido: {pedido}")
        
    def abrir_tela_opcao3(self):
        self.label.config(text="Opção 3 selecionada")


if __name__ == '__main__':
    root = Tk()
    app = TelaPrincipal(root)
    root.mainloop()
