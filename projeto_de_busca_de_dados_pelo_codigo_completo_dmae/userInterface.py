import streamlit as st
import pandas as pd
import os
from main import process_chunks  # Certifique-se de que o nome do arquivo e a função sejam corretos

def main():
    st.title("Processar Dados DMAE")

    # Input do usuário para número de threads
    num_threads = st.number_input("Número de threads", min_value=1, value=60, step=1)

    # Input do usuário para o arquivo de entrada
    input_file = st.file_uploader("Arquivo com códigos completos", type=["csv"])

    # Input do usuário para número de dados processados por salvamento
    num_saves = st.number_input("Número de dados processados por salvamento", min_value=1, value=1000, step=1)

    def process_and_display():
        if input_file is not None:
            # Cria o diretório 'uploads' se ele não existir
            if not os.path.exists("uploads"):
                os.makedirs("uploads")

            file_path = os.path.join("uploads", input_file.name)
            with open(file_path, "wb") as f:
                f.write(input_file.read())

            # Exibe mensagem de processamento
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text("Processando...")

            # Processa os dados e atualiza a barra de progresso
            combined_output_path = process_chunks(file_path, num_saves, num_threads)
            progress_bar.progress(100)

            # Atualiza o status após o processamento ser concluído
            status_text.text("Sucesso no processamento dos dados")
            st.success("Sucesso no processamento dos dados")

            # Exibe o link para download do arquivo combinado
            st.markdown(f"[Baixar arquivo combinado]({combined_output_path})")

            # Remove o arquivo de upload após o processamento
            os.remove(file_path)
        else:
            st.warning("Por favor, faça upload de um arquivo de entrada.")

    # Botão para iniciar o processamento dos dados
    if st.button("Processar Dados"):
        process_and_display()

if __name__ == "__main__":
    main()
