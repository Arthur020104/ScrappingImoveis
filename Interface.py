import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
import os
from helper.prefeitura import request_new_prefeitura_data
from helper.dmae import request_new_dmae_data
from tkinter import filedialog

class GitHubLikeInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub-like Interface")
        self.root.geometry("800x600")
        self.root.configure(bg='#444444')

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
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

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        self.tab1 = ttk.Frame(notebook, style='TFrame')
        self.tab2 = ttk.Frame(notebook, style='TFrame')
        self.tab3 = ttk.Frame(notebook, style='TFrame')

        notebook.add(self.tab1, text='Aba 1 Prefeitura')
        notebook.add(self.tab2, text='Aba 2 Dmae')
        notebook.add(self.tab3, text='Aba 3')

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        title1 = ttk.Label(self.tab1, text="Interface GitHub-like - Aba 1 Prefeitura", font=('Arial', 24))
        title1.pack(pady=10)

        self.entry_start_code_pref = ttk.Entry(self.tab1)
        self.entry_start_code_pref.pack(pady=5)
        self.entry_start_code_pref.insert(0, "Código Inicial")

        self.entry_end_code_pref = ttk.Entry(self.tab1)
        self.entry_end_code_pref.pack(pady=5)
        self.entry_end_code_pref.insert(0, "Código Final")

        self.entry_records_per_chunk_pref = ttk.Entry(self.tab1)
        self.entry_records_per_chunk_pref.pack(pady=5)
        self.entry_records_per_chunk_pref.insert(0, "Registros por Lote")

        self.entry_concurrent_chunks_pref = ttk.Entry(self.tab1)
        self.entry_concurrent_chunks_pref.pack(pady=5)
        self.entry_concurrent_chunks_pref.insert(0, "Lotes Concorrentes")

        self.update_base_var_pref = tk.BooleanVar()
        self.update_base_checkbutton_pref = ttk.Checkbutton(self.tab1, text="Atualizar base de dados", variable=self.update_base_var_pref, command=self.toggle_base_path_entry_pref)
        self.update_base_checkbutton_pref.pack(pady=10)

        self.entry_base_path_pref = ttk.Entry(self.tab1, state='disabled')
        self.entry_base_path_pref.insert(0, "Caminho personalizado para a base de dados")
        
        self.button_browse_pref = ttk.Button(self.tab1, text="Selecionar Pasta", command=self.browse_directory_pref)
        self.button_browse_pref.pack(pady=5)

        self.toggle_base_path_entry_pref()
        self.button_pref = ttk.Button(self.tab1, text="Processar Dados da Prefeitura", command=self.threaded_request_data_from_prefeitura)
        self.button_pref.pack(pady=20)

    def setup_tab2(self):
        title2 = ttk.Label(self.tab2, text="Interface GitHub-like - Aba 2 Dmae", font=('Arial', 24))
        title2.pack(pady=10)

        self.entry_start_code_dmae = ttk.Entry(self.tab2)
        self.entry_start_code_dmae.pack(pady=5)
        self.entry_start_code_dmae.insert(0, "Código Inicial")

        self.entry_end_code_dmae = ttk.Entry(self.tab2)
        self.entry_end_code_dmae.pack(pady=5)
        self.entry_end_code_dmae.insert(0, "Código Final")

        self.entry_records_per_chunk_dmae = ttk.Entry(self.tab2)
        self.entry_records_per_chunk_dmae.pack(pady=5)
        self.entry_records_per_chunk_dmae.insert(0, "Registros por Lote")

        self.entry_concurrent_chunks_dmae = ttk.Entry(self.tab2)
        self.entry_concurrent_chunks_dmae.pack(pady=5)
        self.entry_concurrent_chunks_dmae.insert(0, "Lotes Concorrentes")

        self.update_base_var_dmae = tk.BooleanVar()
        self.update_base_checkbutton_dmae = ttk.Checkbutton(self.tab2, text="Atualizar base de dados", variable=self.update_base_var_dmae, command=self.toggle_base_path_entry_dmae)
        self.update_base_checkbutton_dmae.pack(pady=10)

        self.entry_base_path_dmae = ttk.Entry(self.tab2, state='disabled')
        self.entry_base_path_dmae.insert(0, "Caminho personalizado para a base de dados")
    
        
        self.button_browse_dmae = ttk.Button(self.tab2, text="Selecionar Pasta", command=self.browse_directory_dmae)
        self.button_browse_dmae.pack(pady=5)

        self.toggle_base_path_entry_dmae()
        self.button_dmae = ttk.Button(self.tab2, text="Processar Dados do DMAE", command=self.threaded_request_data_from_dmae)
        self.button_dmae.pack(pady=20)

    def toggle_base_path_entry_pref(self):
        if self.update_base_var_pref.get():
            self.entry_base_path_pref.pack_forget()
            self.button_browse_pref.pack_forget()
        else:
            self.entry_base_path_pref.pack(pady=5)
            self.button_browse_pref.pack(pady=5)

    def toggle_base_path_entry_dmae(self):
        if self.update_base_var_dmae.get():
            self.entry_base_path_dmae.pack_forget()
            self.button_browse_dmae.pack_forget()
        else:
            self.entry_base_path_dmae.pack(pady=5)
            self.button_browse_dmae.pack(pady=5)

    def browse_directory_pref(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_base_path_pref.config(state='normal')
            self.entry_base_path_pref.delete(0, tk.END)
            self.entry_base_path_pref.insert(0, directory)
            self.entry_base_path_pref.config(state='disabled')

    def browse_directory_dmae(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_base_path_dmae.config(state='normal')
            self.entry_base_path_dmae.delete(0, tk.END)
            self.entry_base_path_dmae.insert(0, directory)
            self.entry_base_path_dmae.config(state='disabled')

    def setup_tab3(self):
        title3 = ttk.Label(self.tab3, text="Interface GitHub-like - Aba 3", font=('Arial', 24))
        title3.pack(pady=10)
        button3 = ttk.Button(self.tab3, text="Pressione-me na Aba 3", command=lambda: self.on_button_click(2))
        button3.pack(pady=20)
        self.label3 = ttk.Label(self.tab3, text="Aguardando...")
        self.label3.pack(pady=20)

    def on_button_click(self, id):
        if id == 0:
            pass
            #print("Botão pressionado!")
        elif id == 1:
            pass
            #print("Botão pressionado!")
        elif id == 2:
            self.label3.config(text="Botão pressionado!")
    
    def request_data_from_prefeitura(self):
        try:
            start_code = int(self.entry_start_code_pref.get())
            end_code = int(self.entry_end_code_pref.get())
            records_per_chunk = int(self.entry_records_per_chunk_pref.get())
            concurrent_chunks = int(self.entry_concurrent_chunks_pref.get())
            if self.update_base_var_pref.get():
                request_new_prefeitura_data(start_code, end_code, records_per_chunk, concurrent_chunks,True)
                print("Dados da Prefeitura processados e base atualizada com sucesso!")
            else:
                base_path = self.entry_base_path_pref.get()
                new_file = request_new_prefeitura_data(start_code, end_code, records_per_chunk, concurrent_chunks,False)
                name_file = 'prefeitura' + os.path.basename(new_file)
                new_path = os.path.join(base_path, name_file)
                check_if_exist(new_path)
                os.rename(new_file, new_path)
                print(f"Dados da Prefeitura processados e salvos em {base_path}")
        except Exception as e:
            print(f"Erro: {e}")

    def request_data_from_dmae(self):
        try:
            start_code = int(self.entry_start_code_dmae.get())
            end_code = int(self.entry_end_code_dmae.get())
            records_per_chunk = int(self.entry_records_per_chunk_dmae.get())
            concurrent_chunks = int(self.entry_concurrent_chunks_dmae.get())
            if self.update_base_var_dmae.get():
                request_new_dmae_data(start_code, end_code, records_per_chunk, concurrent_chunks)
                print("Dados do DMAE processados e base atualizada com sucesso!")
            else:
                base_path_dmae = self.entry_base_path_dmae.get()
                new_file = request_new_dmae_data(start_code, end_code, records_per_chunk, concurrent_chunks,False)
                #movendo o arquivo para o path desejado
                #1 pegar o nome do arquivo
                name_file = 'dmae' + os.path.basename(new_file)
                #2 mover o arquivo
                new_path = os.path.join(base_path_dmae, name_file)
                check_if_exist(new_path)
                os.rename(new_file, new_path)
                print(f"Dados do DMAE processados e salvos em {base_path_dmae}")
        except Exception as e:
            print(f"Erro: {e}")

    def threaded_request_data_from_prefeitura(self):
        threading.Thread(target=self.request_data_from_prefeitura).start()

    def threaded_request_data_from_dmae(self):
        threading.Thread(target=self.request_data_from_dmae).start()
def check_if_exist(destination):
    if os.path.exists(destination):
        os.remove(destination)
if __name__ == '__main__':
    root = tk.Tk()
    app = GitHubLikeInterface(root)
    app.toggle_base_path_entry_dmae()
    app.toggle_base_path_entry_pref()
    root.mainloop()
