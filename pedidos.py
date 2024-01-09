from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3

def Database():
    global conn, cursor
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, DATA TEXT, "
        "HORA TEXT, FUNCIONARIO TEXT, TAREFA TEXT)")
def DisplayForm():
    root = Tk()
    root.geometry("900x300")
    root.resizable(0,0)
    root.title("Gestão")
    global tree
    global SEARCH
    global data,hora,funcionario,tarefa
    SEARCH = StringVar()
    data = StringVar()
    hora = StringVar()
    funcionario = StringVar()
    tarefa = StringVar()
    TopViewForm = Frame(root, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LFrom = Frame(root, width="350",bg="#15244C")
    LFrom.pack(side=LEFT, fill=Y)
    LeftViewForm = Frame(root, width=500,bg="#0B4670")
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(root, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Sistema de Gestão", font=('verdana', 18), width=600,bg="cyan")
    lbl_text.pack(fill=X)
    Label(LFrom, text="Data  ", font=("Arial", 12),bg="#15244C",fg="white").pack(side=TOP)
    Entry(LFrom,font=("Arial",10,"bold"),textvariable=data).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Hora ", font=("Arial", 12),bg="#15244C",fg="white").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=hora).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="funcionario ", font=("Arial", 12),bg="#15244C",fg="white").pack(side=TOP)
    funcionario.set("Selecionar o Funcionário")
    content={' Ana Maria ','Zulmira','Inês'}
    OptionMenu(LFrom,funcionario,*content).pack(side=TOP, padx=10, fill=X)

    Label(LFrom, text="Tarefa ", font=("Arial", 12),bg="#15244C",fg="white").pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=tarefa).pack(side=TOP, padx=10, fill=X)
    Button(LFrom,text="Submeter",font=("Arial", 10, "bold"),bg="#15244C",fg="white",command=adicionar).pack(side=TOP, padx=10,pady=5, fill=X)

    lbl_txtsearch = Label(LeftViewForm, text="Digite o Funcionário", font=('verdana', 10),bg="#0B4670")
    lbl_txtsearch.pack()
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)

    btn_search = Button(LeftViewForm, text="Pesquisa",bg="cyan", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_view = Button(LeftViewForm, text="Ver tudo",bg="cyan",command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_Limpar = Button(LeftViewForm, text="Limpar",bg="cyan",command=limpar)
    btn_Limpar.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_apagar = Button(LeftViewForm, text="Apagar",bg="cyan",command=apagar)
    btn_apagar.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Student Id", "Data", "Hora", "Funcionario","Tarefa"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Student Id', text="Id", anchor=W)
    tree.heading('Data', text="Data", anchor=W)
    tree.heading('Hora', text="Hora", anchor=W)
    tree.heading('Funcionario', text="Funcionário", anchor=W)
    tree.heading('Tarefa', text="Tarefa", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()
def SearchRecord():
    Database()
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION WHERE FUNCIONARIO LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
def adicionar():
    Database()
    vdata=data.get()
    vhora=hora.get()
    vfuncionario=funcionario.get()
    vtarefa=tarefa.get()
    if vdata=='' or vhora==''or vfuncionario=='' or vtarefa=='':
        tkMessageBox.showinfo("Atenção","Preencha os espaços vazios!!!")
    else:
        conn.execute('INSERT INTO REGISTRATION (DATA,HORA,FUNCIONARIO,TAREFA) \
             VALUES (?,?,?,?)',(vdata,vhora,vfuncionario,vtarefa));
        conn.commit()

        tkMessageBox.showinfo("Sucesso","Alunos adicionado com Sucesso")
        DisplayData()
        conn.close()
def apagar():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Atenção","Selecione o aluno a eliminar ")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Deseja apagar o registo do aluno?',
                                          icon="warning")
        if result == 'yes':
             curItem = tree.focus()
             contents = (tree.item(curItem))
             selecteditem = contents['values']
             tree.delete(curItem)
             cursor=conn.execute("DELETE FROM REGISTRATION WHERE RID = %d" % selecteditem[0])
             conn.commit()
             cursor.close()
             conn.close()

        conn.close()
def limpar():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")
    data.set("")
    hora.set("")
    funcionario.set("Digite o Funcionário")
    tarefa.set("")

def DisplayData():
    Database()
    tree.delete(*tree.get_children())
    cursor=conn.execute("SELECT * FROM REGISTRATION")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
        tree.bind("<Double-1>",OnDoubleClick)
    cursor.close()
    conn.close()
def OnDoubleClick(self):
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    data.set(selecteditem[1])
    hora.set(selecteditem[2])
    funcionario.set(selecteditem[3])
    tarefa.set(selecteditem[4])
DisplayForm()
if __name__=='__main__':
    mainloop()