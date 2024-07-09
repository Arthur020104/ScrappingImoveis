import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
from .get_cod_completo import get_property_number_and_adress
import threading  # Importa o módulo threading para executar threads
import time  # Importa o módulo time para medir o tempo
import tqdm  # Importa tqdm para criar uma barra de progresso
import os

def process_chunks(start_code: int, end_code: int, records_per_chunk: int, concurrent_chunks: int):
    """Processa chunks de códigos em paralelo.

    Args:
        start_code (int): Número inicial da faixa dos códigos a serem buscados na prefeitura
        end_code (int): Número final da faixa dos códigos a serem buscados na prefeitura
        records_per_chunk (int): Número de dados a serem salvos/processados por chunk
        concurrent_chunks (int): Número de chunks processados simultaneamente
    
    Returns:
        str: Caminho para o arquivo combined_output.csv
    """
    start_time = time.time()
    
    # Define a faixa de códigos únicos a partir dos parâmetros inicial e final
    code_range = range(start_code, end_code + 1)  # Inclui end_code na faixa

    # Calcula o tamanho desejado dos chunks com base no número de dados a serem salvos por chunk
    chunk_size = records_per_chunk // concurrent_chunks

    # Calcula o número de chunks que serão processados
    total_chunks = max(len(code_range) // chunk_size, concurrent_chunks)

    # Função que será chamada em cada thread para processar um chunk
    def process_chunk(chunk, result_list):
        # Chama a função get_property_number_and_adress do módulo get_cod_completo
        # e adiciona os resultados na lista result_list
        result_list.extend(get_property_number_and_adress(chunk))

    # Ajusta o tamanho dos chunks para garantir o tamanho desejado
    chunk_size = (len(code_range) // total_chunks) + (1 if len(code_range) % total_chunks != 0 else 0)
    chunks = [list(code_range[i:i + chunk_size]) for i in range(0, len(code_range), chunk_size)]

    # Lista para armazenar objetos de thread
    threads = []

    # Lista para armazenar todos os resultados
    all_results = []
    latest_chunk_index = 0
    progress_bar = tqdm.tqdm(range(len(chunks)), desc="Progress", unit="chunks")
    script_dir = os.path.dirname(__file__)
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
        df.to_csv(os.path.join(script_dir, 'combined_output.csv'), index=False)
        #print(f"CSV file created.\n{100 * '*'}")
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

    combined_df = pd.DataFrame()  # Cria um DataFrame vazio para combinar os resultados
    time.sleep(2)

    files = [os.path.join(script_dir, f"output_{i}.csv") for i in range(0, latest_chunk_index + 1)]
    for file in files:
        # Lê o arquivo CSV em um DataFrame
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"File {file} is empty.")
            os.remove(file)
            break
        
        # Adiciona o DataFrame ao DataFrame combinado
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        os.remove(file)

    # Escreve o DataFrame combinado em um novo arquivo CSV
    combined_df.to_csv(os.path.join(script_dir, 'combined_output.csv'), index=False)
    print(f"CSV file created.\n{100 * '*'}")
    print("Combined CSV file created: combined_output.csv")
    return os.path.abspath(os.path.join(script_dir, 'combined_output.csv'))

if __name__ == '__main__':
    process_chunks(1, 200, 100, 10)
