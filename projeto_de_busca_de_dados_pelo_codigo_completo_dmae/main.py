import pandas as pd
from .data import get_info_by_complete_property_code
import threading
import time
import tqdm
import os

def process_chunks(file_path: str, save_number: int, concurrent_chunks: int,receving_file:bool, complete_code_list:list):
    """
    Processa chunks de códigos de propriedades em paralelo.

    Args:
        file_path (str): Caminho para o arquivo CSV contendo os códigos de propriedade.
        save_number (int): Número de registros a serem salvos por chunk.
        concurrent_chunks (int): Número de chunks processados simultaneamente.
        receving_file (bool): Se a função está recebendo um arquivo ou não.
        complete_code_list (list): Lista com todos os códigos completos. Só é necessário se receving_file=True.
    Returns:
        combined_output.csv: Arquivo CSV combinado contendo todos os resultados.(PATH)
    """
    start_time = time.time()
    unique_codigos_from_file = []
    # Lê os códigos únicos do arquivo CSV
    if receving_file:
        df = pd.read_csv(file_path)
        unique_codigos_from_file = df["codigo_completo"].unique()

        # Limpa os dados para a consulta
        cleaned_codes = [
            str(code).replace(".", "").replace(" ", "").replace("-", "").replace("IMO:", "")
            for code in unique_codigos_from_file
        ]
        unique_codigos_from_file = cleaned_codes
    else:
        unique_codigos_from_file = complete_code_list
    #print(f"Number of unique codes: {len(unique_codigos_from_file)}")

    # Calcula o tamanho desejado dos chunks
    desired_chunk_size = save_number / concurrent_chunks

    # Calcula o número de chunks que serão processados simultaneamente
    total_chunks = int(len(unique_codigos_from_file) / desired_chunk_size)
    total_chunks = max(total_chunks, concurrent_chunks)
    #print(f"Number of chunks: {total_chunks}")

    # Função que será chamada em cada thread
    def process_chunk(chunk, result_list):
        result_list.extend(get_info_by_complete_property_code(chunk, 2, 5))

    # Ajusta o tamanho dos chunks para garantir o tamanho desejado
    chunk_size = int(len(unique_codigos_from_file) / total_chunks)
    chunk_size = chunk_size + 1 if len(unique_codigos_from_file) % total_chunks != 0 else chunk_size
    chunks = [
        unique_codigos_from_file[i:i + chunk_size]
        for i in range(0, len(unique_codigos_from_file), chunk_size)
    ]

    # Lista para armazenar resultados
    all_results = []
    latest_chunk_index = 0
    progress_bar = tqdm.tqdm(range(len(chunks)), desc="Progress", unit="chunks")
    
    # Obtém o diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Processa os chunks em grupos de concurrent_chunks
        for i in range(0, len(chunks), concurrent_chunks):
            progress_bar.set_postfix({"Progress": f"{i}/{len(chunks)}"})
            current_chunks = chunks[i:i + concurrent_chunks]
            
            # Lista para armazenar objetos de thread do grupo atual de chunks
            current_threads = []
            
            # Cria e inicia threads para o grupo atual de chunks
            for chunk in current_chunks:
                thread = threading.Thread(target=process_chunk, args=(chunk, all_results))
                current_threads.append(thread)
                thread.start()
            
            # Espera que todas as threads do grupo atual terminem
            for thread in current_threads:
                thread.join()

            # Salva os resultados em um arquivo CSV após cada grupo de chunks
            value = 0 if i == 0 else int(i / concurrent_chunks)
            
            csv_filename = os.path.join(script_dir, f'output_{value}.csv')
            excel_filename = os.path.join(script_dir, f'output_{value}.xlsx')
            
            df = pd.DataFrame(all_results)
            df.to_csv(csv_filename, index=False)
           # df.to_excel(excel_filename, index=False)
            
            print(f"CSV file created: {csv_filename}")
            #print(f"Excel file created: {excel_filename}")
            
            latest_chunk_index = value
            # Limpa a lista de resultados para as próximas iterações
            all_results = []
            progress_bar.update(concurrent_chunks)
    except Exception as e:
        # Tratamento de exceções, salva resultados parciais se ocorrer um erro
        print(f"An error occurred: {e}")
        #print(f"{100 * '*'}\nProcessing the remaining chunks...")
        df = pd.DataFrame(all_results)
        combined_output_path = os.path.join(script_dir, 'combined_output.csv')
        df.to_csv(combined_output_path, index=False)
        print(f"CSV file created.\n{100 * '*'}")
        return

    # Salva os dados restantes se houver algum
    if len(all_results) > 0:
        i += concurrent_chunks
        value = 0 if i == 0 else int(i / concurrent_chunks)
            
        csv_filename = os.path.join(script_dir, f'output_{value}.csv')
        
        df = pd.DataFrame(all_results)
        df.to_csv(csv_filename, index=False)
        
        #print(f"CSV file created: {csv_filename}")
        
        latest_chunk_index = value
        all_results = []

    # Combina todos os arquivos CSV em um único arquivo
    combined_df = pd.DataFrame()  # Cria um DataFrame vazio para combinar os resultados
    time.sleep(2)

    files = [os.path.join(script_dir, f"output_{i}.csv") for i in range(0, latest_chunk_index + 1)]
    for file in files:
        # Lê o arquivo CSV em um DataFrame
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            #print(f"File {file} is empty.")
            os.remove(file)
            continue
        except:
            os.remove(file)
            continue
        
        # Adiciona o DataFrame ao DataFrame combinado
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        os.remove(file)

    # Escreve o DataFrame combinado em um novo arquivo CSV
    combined_output_path = os.path.join(script_dir, 'combined_output.csv')
    combined_df.to_csv(combined_output_path, index=False)
    print(f"CSV file created.\n{100 * '*'}")
    print(f"Combined CSV file created: {combined_output_path}")
    time_taken = time.time() - start_time
    print(f"Time taken: {time_taken:.2f} seconds")
    return os.path.abspath(combined_output_path)

if __name__ == '__main__':
    process_chunks('C:/Users/arthu/OneDrive/Desktop/Repo/projeto_de_busca_de_dados_pelo_codigo_completo_dmae/combined_output.csv', 1000, 60)
