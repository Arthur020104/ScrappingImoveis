import streamlit as st
from main import process_chunks as process_file
import os

def main():
    header_image = 'C:/Users/arthu/OneDrive/Desktop/Repo/background.png'
    st.write('\n\n\n')

    # Create a layout with two columns (adjust the ratios as needed)
    col1, col2 = st.columns([25,70])
    with col2:
        st.image(header_image, width=277)
    st.title("Processar dados Prefeitura de Uberlândia")

    # Create the 'temp' directory if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Input fields for initial number, end number, save number, and num concurrent chunks
    inicial_num = st.number_input("Número inicial da faixa dos códigos", value=1, step=1)
    end_num = st.number_input("Número final da faixa dos códigos", value=100, step=1)
    save_number = st.number_input("Número de dados processados por salvamento", value=1000, step=1)
    num_concurrent_chunks = st.number_input("Quantidade de threads", value=5, step=1)

    # Process file button
    if st.button("Process File"):
        # Call the process_file function with the input parameters
        process_file(inicial_num, end_num, save_number, num_concurrent_chunks)

        # Show a success message
        st.success("File processing completed successfully")

if __name__ == "__main__":
    main()
