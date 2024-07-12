import tkinter as tk
from tkinter import ttk, filedialog
import threading
import os
from helper.prefeitura import request_new_prefeitura_data
from helper.dmae import request_new_dmae_data
from helper.territorial import request_new_pdf_data
from PIL import Image, ImageTk
class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface")
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

        notebook.add(self.tab1, text='PREFEITURA')
        notebook.add(self.tab2, text='DMAE')
        notebook.add(self.tab3, text='TERRITORIAL')

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        title1 = ttk.Label(self.tab1, text="Interface - Prefeitura", font=('Arial', 24))
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
        
        self.status_prefeitura = tk.StringVar()
        self.status_prefeitura.set("Status: ")
        self.status_label_prefeitura = ttk.Label(self.tab1, textvariable=self.status_prefeitura, font=('Arial', 10))
        self.status_label_prefeitura.pack(pady=10)
        
        self.button_pref = ttk.Button(self.tab1, text="Processar Dados da Prefeitura", command=self.threaded_request_data_from_prefeitura)
        self.button_pref.pack(pady=20)
        self.toggle_base_path_entry_pref()

    def setup_tab2(self):
        title2 = ttk.Label(self.tab2, text="Interface - Dmae", font=('Arial', 24))
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

        self.status_text_dmae = tk.StringVar()
        self.status_text_dmae.set("Status: ")
        self.status_label_dmae = ttk.Label(self.tab2, textvariable=self.status_text_dmae, font=('Arial', 10))
        self.status_label_dmae.pack(pady=10)
        
        self.update_base_var_dmae = tk.BooleanVar()
        self.update_base_checkbutton_dmae = ttk.Checkbutton(self.tab2, text="Atualizar base de dados", variable=self.update_base_var_dmae, command=self.toggle_base_path_entry_dmae)
        self.update_base_checkbutton_dmae.pack(pady=10)
        
        
        self.entry_base_path_dmae = ttk.Entry(self.tab2, state='disabled')
        self.entry_base_path_dmae.insert(0, "Caminho personalizado para a base de dados")
    
        
        self.button_browse_dmae = ttk.Button(self.tab2, text="Selecionar Pasta", command=self.browse_directory_dmae)
        self.button_browse_dmae.pack(pady=5)

        self.button_dmae = ttk.Button(self.tab2, text="Processar Dados do DMAE", command=self.threaded_request_data_from_dmae)
        self.button_dmae.pack(pady=20)
        self.toggle_base_path_entry_dmae()

    def toggle_base_path_entry_pref(self):
        if self.update_base_var_pref.get():
            self.button_pref.pack_forget()
            self.status_label_prefeitura.pack_forget()
            self.entry_base_path_pref.pack_forget()
            self.button_browse_pref.pack_forget()
            self.button_pref.pack(pady=5)
            self.status_label_prefeitura.pack(pady=10)
        else:
            self.button_pref.pack_forget()
            self.status_label_prefeitura.pack_forget()
            self.button_browse_pref.pack(pady=5)
            self.entry_base_path_pref.pack(pady=5)
            self.button_pref.pack(pady=5)
            self.status_label_prefeitura.pack(pady=10)

    def toggle_base_path_entry_dmae(self):
        if self.update_base_var_dmae.get():
            self.button_dmae.pack_forget()
            self.status_label_dmae.pack_forget()
            self.entry_base_path_dmae.pack_forget()
            self.button_browse_dmae.pack_forget()
            self.button_dmae.pack(pady=5)
            self.status_label_dmae.pack(pady=10)
        else:
            self.button_dmae.pack_forget()
            self.status_label_dmae.pack_forget()
            self.entry_base_path_dmae.pack(pady=5)
            self.button_browse_dmae.pack(pady=5)
            self.button_dmae.pack(pady=5)
            self.status_label_dmae.pack(pady=10)

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
    def browse_directory_pdf(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_base_path_pdf.config(state='normal')
            self.entry_base_path_pdf.delete(0, tk.END)
            self.entry_base_path_pdf.insert(0, directory)
            self.entry_base_path_pdf.config(state='disabled')
    def setup_tab3(self):
        title3 = ttk.Label(self.tab3, text="Interface - AREA TERRITORIAL", font=('Arial', 24))
        title3.pack(pady=10)

        self.entry_start_code_pdf = ttk.Entry(self.tab3)
        self.entry_start_code_pdf.pack(pady=5)
        self.entry_start_code_pdf.insert(0, "Código Inicial")

        self.entry_end_code_pdf = ttk.Entry(self.tab3)
        self.entry_end_code_pdf.pack(pady=5)
        self.entry_end_code_pdf.insert(0, "Código Final")

        self.entry_records_per_chunk_pdf = ttk.Entry(self.tab3)
        self.entry_records_per_chunk_pdf.pack(pady=5)
        self.entry_records_per_chunk_pdf.insert(0, "Registros por Lote")

        self.entry_concurrent_chunks_pdf = ttk.Entry(self.tab3)
        self.entry_concurrent_chunks_pdf.pack(pady=5)
        self.entry_concurrent_chunks_pdf.insert(0, "Lotes Concorrentes")

        self.update_base_var_pdf = tk.BooleanVar()
        self.update_base_checkbutton_pdf = ttk.Checkbutton(self.tab3, text="Atualizar base de dados", variable=self.update_base_var_pdf, command=self.toggle_base_path_entry_pdf)
        self.update_base_checkbutton_pdf.pack(pady=10)

        self.entry_base_path_pdf = ttk.Entry(self.tab3, state='disabled')
        self.entry_base_path_pdf.insert(0, "Caminho personalizado para a base de dados")
    
        
        self.button_browse_pdf = ttk.Button(self.tab3, text="Selecionar Pasta", command=self.browse_directory_pdf)
        self.button_browse_pdf.pack(pady=5)

        self.status_text_territorial = tk.StringVar()
        self.status_text_territorial.set("Status: ")
        self.status_label_territorial = ttk.Label(self.tab3, textvariable=self.status_text_territorial, font=('Arial', 10))
        self.status_label_territorial.pack(pady=10)
        
        self.button_pdf = ttk.Button(self.tab3, text="Processar Dados de Area territorial", command=self.threaded_request_data_from_pdf)
        self.button_pdf.pack(pady=20)
        self.toggle_base_path_entry_pdf()
    def toggle_base_path_entry_pdf(self):
        if self.update_base_var_pdf.get():
            self.button_pdf.pack_forget()
            self.status_label_territorial.pack_forget()
            self.entry_base_path_pdf.pack_forget()
            self.button_browse_pdf.pack_forget()
            self.button_pdf.pack(pady=5)
            self.status_label_territorial.pack(pady=10)
        else:
            self.button_pdf.pack_forget()
            self.status_label_territorial.pack_forget()
            self.button_browse_pdf.pack(pady=5)
            self.entry_base_path_pdf.pack(pady=5)
            self.button_pdf.pack(pady=5)
            self.status_label_territorial.pack(pady=10)
    def request_data_from_prefeitura(self):
        try:
            start_code = int(self.entry_start_code_pref.get())
            end_code = int(self.entry_end_code_pref.get())
            records_per_chunk = int(self.entry_records_per_chunk_pref.get())
            concurrent_chunks = int(self.entry_concurrent_chunks_pref.get())
            if self.update_base_var_pref.get():
                request_new_prefeitura_data(start_code, end_code, records_per_chunk, concurrent_chunks,True)
                self.status_prefeitura.set("Status: Dados da Prefeitura processados e base atualizada com sucesso!")
            else:
                base_path = self.entry_base_path_pref.get()
                new_file, status = request_new_prefeitura_data(start_code, end_code, records_per_chunk, concurrent_chunks,False)
                if not new_file:
                    self.status_prefeitura.set(f"Status: {status}")
                name_file = 'prefeitura' + os.path.basename(new_file)
                new_path = os.path.join(base_path, name_file)
                check_if_exist(new_path)
                os.rename(new_file, new_path)
                result = f"Dados da Prefeitura processados e salvos em {base_path}"
                self.status_prefeitura.set(f"Status: {result}")
        except Exception as e:
            result = f"Erro: {e}"
            self.status_prefeitura.set(f"Status: {result}")

    def request_data_from_dmae(self):
        try:
            start_code = int(self.entry_start_code_dmae.get())
            end_code = int(self.entry_end_code_dmae.get())
            records_per_chunk = int(self.entry_records_per_chunk_dmae.get())
            concurrent_chunks = int(self.entry_concurrent_chunks_dmae.get())
            if self.update_base_var_dmae.get():
                request_new_dmae_data(start_code, end_code, records_per_chunk, concurrent_chunks)
                result = "Dados do DMAE processados e base atualizada com sucesso!"
                self.status_text_dmae.set(f"Status: {result}")
                print(result)
            else:
                base_path_dmae = self.entry_base_path_dmae.get()
                new_file, status = request_new_dmae_data(start_code, end_code, records_per_chunk, concurrent_chunks,False)
                if not new_file:
                    #atualiza o textfield de status com a mensagem de erro
                    self.status_text_dmae.set(f"Status: {status}")
                    return
                #movendo o arquivo para o path desejado
                #1 pegar o nome do arquivo
                name_file = 'dmae' + os.path.basename(new_file)
                #2 mover o arquivo
                new_path = os.path.join(base_path_dmae, name_file)
                check_if_exist(new_path)
                os.rename(new_file, new_path)
                result = f"Dados do DMAE processados e salvos em {base_path_dmae}"
                print(result)
                self.status_text_dmae.set(f"Status: {result}")
                #Atualiza o textfield de status com a mensagem de sucesso
        except Exception as e:
            result = f"Erro processando os dados do DMAE: {e}"
            print(result)
            self.status_text_dmae.set(f"Status: {result}")
            #atualiza o textfield de status com a mensagem de erro
            return
    def request_data_from_pdf(self):
        try:
            start_code = int(self.entry_start_code_pdf.get())
            end_code = int(self.entry_end_code_pdf.get())
            records_per_chunk = int(self.entry_records_per_chunk_pdf.get())
            concurrent_chunks = int(self.entry_concurrent_chunks_pdf.get())
            if self.update_base_var_pdf.get():
                request_new_pdf_data(start_code, end_code, records_per_chunk, concurrent_chunks)
                self.status_text_territorial.set("Status: Dados do PDF processados e base atualizada com sucesso!")
            else:
                base_path_pdf = self.entry_base_path_pdf.get()
                new_file, status = request_new_pdf_data(start_code, end_code, records_per_chunk, concurrent_chunks,False)
                if not new_file:
                    self.status_text_territorial.set(f"Status: {status}")
                    return
                #movendo o arquivo para o path desejado
                #1 pegar o nome do arquivo
                name_file = 'PDF' + os.path.basename(new_file)
                #2 mover o arquivo
                new_path = os.path.join(base_path_pdf, name_file)
                check_if_exist(new_path)
                os.rename(new_file, new_path)
                result = f"Dados do PDF processados e salvos em {base_path_pdf}"
                self.status_text_territorial.set(f"Status: {result}")
        except Exception as e:
            result = f"Erro: {e}"
            self.status_text_territorial.set(f"Status: {result}")
    def threaded_request_data_from_pdf(self):
        self.status_text_territorial.set("Status: Processando dados da area territorial...")
        threading.Thread(target=self.request_data_from_pdf).start()
    def threaded_request_data_from_prefeitura(self):
        self.status_prefeitura.set("Status: Processando dados da prefeitura...")
        threading.Thread(target=self.request_data_from_prefeitura).start()

    def threaded_request_data_from_dmae(self):
        self.status_text_dmae.set("Status: Processando dados do DMAE...")
        threading.Thread(target=self.request_data_from_dmae).start()
def check_if_exist(destination):
    if os.path.exists(destination):
        os.remove(destination)
if __name__ == '__main__':
    root = tk.Tk()
    
    img = Image.open("letter-g.png")
    photo = ImageTk.PhotoImage(img)

    root.iconphoto(True, photo)

    app = Interface(root)
    app.toggle_base_path_entry_dmae()
    app.toggle_base_path_entry_pref()
    
    root.mainloop()