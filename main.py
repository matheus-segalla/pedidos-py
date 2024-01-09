from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

def Database():
    global conn, cursor
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                   "nomeproduto TEXT, lote TEXT, quantidade TEXT, preco TEXT,undidademedida TEXT)")


def Create():
    if  NOMEPRODUTO.get() == "" or LOTE.get() == "" or QUANTIDADE.get() == ""\
            or PRECO.get() == ""or UNIDADEMEDIDA.get() == "":
        txt_result.config(text="Por favor, completa o formulário!", fg="red")


    else:
        Database()
        cursor.execute("INSERT INTO `member` (nomeproduto, lote, quantidade, preco,undidademedida) VALUES(?, ?, ?, ?, ?)", (str(NOMEPRODUTO.get()),
                                                                                                          str(LOTE.get()), str(QUANTIDADE.get()), str(PRECO.get()),str(UNIDADEMEDIDA.get()),))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM `member` ORDER BY `nomeproduto` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4],data[5]))
        conn.commit()
        NOMEPRODUTO.set("")
        LOTE.set("")
        QUANTIDADE.set("")
        PRECO.set("")
        UNIDADEMEDIDA.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Produto criado!", fg="green")
def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `member` ORDER BY `nomeproduto` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5]))
    cursor.close()
    conn.close()
    txt_result.config(text="Dados Utilizados", fg="blue")
def Update():
    Database()

    tree.delete(*tree.get_children())
    cursor.execute("UPDATE `member` SET `nomeproduto` = ?, `lote` = ?, `quantidade` =?,  `preco` = ?,  `undidademedida` = ? WHERE `mem_id` = ?", (str(NOMEPRODUTO.get()),
                                                                                                                                             str(LOTE.get()), str(QUANTIDADE.get()), str(PRECO.get()), str(UNIDADEMEDIDA.get()), int(mem_id)))
    conn.commit()
    cursor.execute("SELECT * FROM `member` ORDER BY `nomeproduto` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5]))
    cursor.close()
    conn.close()
    NOMEPRODUTO.set("")
    LOTE.set("")
    QUANTIDADE.set("")
    PRECO.set("")
    UNIDADEMEDIDA.set("")
    btn_create.config(state=NORMAL)
    btn_read.config(state=NORMAL)
    btn_update.config(state=DISABLED)
    btn_delete.config(state=NORMAL)
    txt_result.config(text="Actualizar os dados com sucesso", fg="green")
def OnSelected(event):
    global mem_id;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    NOMEPRODUTO.set("")
    LOTE.set("")
    QUANTIDADE.set("")
    PRECO.set("")
    UNIDADEMEDIDA.set("")
    NOMEPRODUTO.set(selecteditem[1])
    LOTE.set(selecteditem[2])
    QUANTIDADE.set(selecteditem[3])
    PRECO.set(selecteditem[4])
    UNIDADEMEDIDA.set(selecteditem[5])
    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)
def Delete():
    if not tree.selection():
       txt_result.config(text="Por favor, selecione um produto!", fg="red")
    else:
        result = tkMessageBox.askquestion('Eliminar Produto', 'Deseja eliminar produto?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Produto eliminado", fg="blue")


def Exit():
    result = tkMessageBox.askquestion('Inventário', 'Deseja sair da aplicação?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
        
root = Tk()
root.title("Inventário")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 900
height = 500
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)

Top = Frame(root, width=900, height=50, bd=8, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=300, height=500, bd=8, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=8, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=100, bd=8, relief="raise")
Buttons.pack(side=BOTTOM)
txt_titulo = Label(Top, width=900, font=('arial', 24), text = "Inventário")
txt_titulo.pack()
txt_nomeproduto = Label(Forms, text="Nome do Produto :", font=('arial', 16), bd=15)
txt_nomeproduto.grid(row=0, sticky="e")
txt_Lote = Label(Forms, text="Número de Lote:", font=('arial', 16), bd=15)
txt_Lote.grid(row=1, sticky="e")
txt_quantidade = Label(Forms, text="Quantidade:", font=('arial', 16), bd=15)
txt_quantidade.grid(row=2, sticky="e")
txt_preco = Label(Forms, text="Preço:", font=('arial', 16), bd=15)
txt_preco.grid(row=3, sticky="e")
txt_unidademedida = Label(Forms, text="Unidade de Medida:", font=('arial', 16), bd=15)
txt_unidademedida.grid(row=4, sticky="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)
NOMEPRODUTO = StringVar()
LOTE = StringVar()
QUANTIDADE = DoubleVar()
PRECO = DoubleVar()
UNIDADEMEDIDA = StringVar()


nomeproduto = Entry(Forms, textvariable=NOMEPRODUTO, width=30)
nomeproduto.grid(row=0, column=1)
lote = Entry(Forms, textvariable=LOTE, width=30)
lote.grid(row=1, column=1)
quantidade = Entry(Forms, textvariable=QUANTIDADE, width=30,justify='center')
quantidade.grid(row=2, column=1)
preco = Entry(Forms, textvariable=PRECO, width=30,justify='center')
preco.grid(row=3, column=1)
unidademedida = Entry(Forms, textvariable=UNIDADEMEDIDA, width=30)
unidademedida.grid(row=4, column=1)

btn_create = Button(Buttons, width=10, text="Criar", command=Create)
btn_create.pack(side=LEFT)
#
btn_read = Button(Buttons, width=10, text="Read", command=Read)
btn_read.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="Update", command=Update, state=DISABLED)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Delete",command=Delete)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Exit", command=Exit)
btn_exit.pack(side=LEFT)
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("MemberID", "Nomeproduto", "Lote", "Quantidade", "Preco", "Unidademedida"),
                    selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Nomeproduto', text="Nome do Produto", anchor=W)
tree.heading('Lote', text="Lote", anchor=W)
tree.heading('Quantidade', text="Quantidade", anchor=W)
tree.heading('Preco', text="Preço", anchor=W)
tree.heading('Unidademedida', text="Unidade Medida", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=150)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)
if __name__ == '__main__':
    root.mainloop()