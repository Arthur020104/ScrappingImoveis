import tkinter as tk
from tkinter import ttk

# Configuração inicial da janela
root = tk.Tk()
root.title("GitHub-like Interface")
root.geometry("800x600")
root.configure(bg='#444444')

# Estilos personalizados
style = ttk.Style()
style.theme_use('clam')

# Estilo para Botões
style.configure('TButton', 
                background='#21262d', 
                foreground='white', 
                borderwidth=0,
                focuscolor=style.configure(".")["background"])
style.map('TButton', 
          background=[('active', '#30363d'), ('disabled', '#21262d')])

# Estilo para Labels
style.configure('TLabel', 
                background='#0d1117', 
                foreground='white')

# Estilo para Frame
style.configure('TFrame', 
                background='#0d1117')

# Estilo para Notebook
style.configure('TNotebook', 
                background='#0d1117', 
                foreground='white', 
                borderwidth=0)
style.configure('TNotebook.Tab', 
                background='#0d1117', 
                foreground='white', 
                borderwidth=0)
style.map('TNotebook.Tab', 
          background=[('selected', '#444444'), ('active', '#30363d')], 
          foreground=[('selected', 'white'), ('active', 'white')])

# Frame principal
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=0, pady=0)

# Criação do Notebook (abas)
notebook = ttk.Notebook(main_frame)
notebook.pack(fill='both', expand=True)

# Criação das abas
tab1 = ttk.Frame(notebook, style='TFrame')
tab2 = ttk.Frame(notebook, style='TFrame')
tab3 = ttk.Frame(notebook, style='TFrame')

notebook.add(tab1, text='Aba 1')
notebook.add(tab2, text='Aba 2')
notebook.add(tab3, text='Aba 3')

# Função para o botão
def on_button_click(id):
    global label1, label2, label3
    if id == 0:
        label1.config(text="Botão pressionado!")
    elif id == 1:
        label2.config(text="Botão pressionado!")
    elif id == 2:
        label3.config(text="Botão pressionado!")

# Conteúdo da Aba 1
title1 = ttk.Label(tab1, text="Interface GitHub-like - Aba 1", font=('Arial', 24))
title1.pack(pady=10)
button1 = ttk.Button(tab1, text="Pressione-me na Aba 1", command=lambda: on_button_click(0))
button1.pack(pady=20)
label1 = ttk.Label(tab1, text="Aguardando...")
label1.pack(pady=20)

# Conteúdo da Aba 2
title2 = ttk.Label(tab2, text="Interface GitHub-like - Aba 2", font=('Arial', 24))
title2.pack(pady=10)
button2 = ttk.Button(tab2, text="Pressione-me na Aba 2", command=lambda: on_button_click(1))
button2.pack(pady=20)
label2 = ttk.Label(tab2, text="Aguardando...")
label2.pack(pady=20)

# Conteúdo da Aba 3
title3 = ttk.Label(tab3, text="Interface GitHub-like - Aba 3", font=('Arial', 24))
title3.pack(pady=10)
button3 = ttk.Button(tab3, text="Pressione-me na Aba 3", command=lambda: on_button_click(2))
button3.pack(pady=20)
label3 = ttk.Label(tab3, text="Aguardando...")
label3.pack(pady=20)

# Inicialização do loop principal
root.mainloop()
