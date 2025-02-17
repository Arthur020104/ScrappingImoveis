import pandas as pd
from .download import download_pdf 
from .infoExtract import read_pdf, extract_info  
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
import time
from .helper_pdf import clear_temp_folders


def initialize_directories():
    """
    Inicializa os diretórios necessários para o processamento.
    Cria o diretório 'temp' se ele não existir.
    """
    if not os.path.exists("temp"):
        os.makedirs("temp")


def read_original_dataframe(filepath):
    df = pd.read_csv(filepath)
    df = df.drop_duplicates(subset='Insc_Cadastral')
    return df


def wait_before_start(n=3):
    """
    Aguarda alguns segundos antes de iniciar o processamento.

    Args:
        n (int): Número de segundos para aguardar.
    """
    for i in range(n):
        print(f"Aguardando {n - i} segundos...")
        time.sleep(1)
    print("Iniciando")


def process_item(item):
    """
    Processa um único item baixando o PDF e extraindo informações.

    Args:
        item (dict): Dicionário contendo 'index' e 'Insc_Cadastral'.

    Returns:
        tuple or None: Índice e informações extraídas, ou None em caso de falha.
    """
    number = item["Insc_Cadastral"].replace(' ', '')
    try:
        response = download_pdf(number)
    except Exception as e:
        print(f"Erro ao baixar PDF para {number}: {e}")
        return None

    if response:
        file_path = f"temp/{number}/{number}.pdf"
        pages_content = read_pdf(file_path)
        if pages_content:
            info = extract_info(pages_content[0][pages_content[0].find("IMÓVEL:"):])
            info['Insc_Cadastral'] = item["Insc_Cadastral"]
            return item['index'], info
    return None


def save_and_clear(df, cycle_number):
    """
    Salva o DataFrame em arquivos CSV e Excel, depois limpa-o.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        cycle_number (int): Número do ciclo para salvar.
    """
    df.to_csv(f"temp/BaseConsolidada_cycle{cycle_number}.csv", index=False)
    df.to_excel(f"temp/BaseConsolidada_cycle{cycle_number}.xlsx", index=False)
    df.drop(df.index, inplace=True)


def process_dataframe_chunks(df_original, save_number, concurrent_threads):
    """
    Processa o DataFrame original em pedaços, salvando os resultados em ciclos.

    Args:
        df_original (pd.DataFrame): DataFrame original a ser processado.
        save_number (int): Número de registros por pedaço.
        concurrent_threads (int): Número de threads simultâneas.

    Returns:
        int: Último ciclo processado.
    """
    num_chunks = len(df_original) // save_number + (len(df_original) % save_number > 0)
    last_cycle = -1

    for cycle in range(num_chunks):
        start_time_cycle = time.time()
        print(f"Iniciando ciclo {cycle + 1}")
        start_index = cycle * save_number
        end_index = min((cycle + 1) * save_number, len(df_original))
        df_chunk = df_original.iloc[start_index:end_index]

        all_results = []

        with ThreadPoolExecutor(max_workers=concurrent_threads) as executor:
            futures = {executor.submit(process_item, {"index": index, "Insc_Cadastral": row["Insc_Cadastral"]}): index for index, row in df_chunk.iterrows()}

            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    _, info = result
                    all_results.append(info)
        last_cycle += 1
        save_cycle_results(all_results, last_cycle)
        #combined_df = combine_csv_files(last_cycle)
        #merge_and_save_intermediate_dataframe(combined_df, df_original, cycle)

        #clear_temp_folders()
        end_time_cycle = time.time()
        print(f"Ciclo {cycle + 1} concluído em {end_time_cycle - start_time_cycle:.2f} segundos")

    return last_cycle


def save_cycle_results(results, cycle):
    """
    Salva os resultados de um ciclo em arquivos CSV e Excel.

    Args:
        results (list): Lista de resultados a serem salvos.
        cycle (int): Número do ciclo para salvar.
    """
    df = pd.DataFrame(results)
    csv_filename = f'temp/BaseConsolidada_output_{cycle}.csv'
    #excel_filename = f'temp/BaseConsolidada_output_{cycle}.xlsx'
    df.to_csv(csv_filename, index=False)
    # df.to_excel(excel_filename, index=False)
    print(f"Arquivo CSV criado: {csv_filename}")
    #print(f"Arquivo Excel criado: {excel_filename}")


def combine_csv_files(last_cycle):
    """
    Combina arquivos CSV de todos os ciclos em um único DataFrame.

    Args:
        last_cycle (int): Último ciclo processado.

    Returns:
        pd.DataFrame: DataFrame combinado.
    """
    combined_df = pd.concat([pd.read_csv(f"temp/BaseConsolidada_output_{i}.csv") for i in range(last_cycle + 1)])
    for i in range(last_cycle + 1):
        os.remove(f"temp/BaseConsolidada_output_{i}.csv")
    combined_df.to_csv("temp/BaseConsolidada_combined.csv", index=False)
    print("Arquivo CSV combinado criado: temp/BaseConsolidada_combined.csv")
    return combined_df


def merge_and_save_intermediate_dataframe(combined_df, df_original, cycle):
    """
    Faz o merge do DataFrame combinado com o DataFrame original e salva o resultado.

    Args:
        combined_df (pd.DataFrame): DataFrame combinado.
        df_original (pd.DataFrame): DataFrame original.
        cycle (int or str): Número do ciclo ou "final" para o ciclo final.
    """
    merged_df = pd.merge(combined_df, df_original, on="Insc_Cadastral", how="outer", suffixes=('_new', '_original'))

    selected_columns = [
        'Cod_Reduzido', 'Insc_Cadastral', 'Imovel_Endereco', 'Bairro', 'Quadra', 'Lote',
        'AreaTerritorial', 'AreaPredial', 'Testada_y', 'Cod_Prefeitura', 'Contribuinte_CPF',
        'Contribuinte_Nome', 'Contribuinte_Endereco', 'Contribuinte_CEP', 'Bairro_Contribuinte'
    ]

    for col in selected_columns:
        col_new = f'{col}_new'
        col_original = f'{col}_original'
        if col_new in merged_df.columns and col_original in merged_df.columns:
            merged_df[col] = merged_df[col_new].combine_first(merged_df[col_original])
        elif col_new in merged_df.columns:
            merged_df[col] = merged_df[col_new]
        elif col_original in merged_df.columns:
            merged_df[col] = merged_df[col_original]

    final_columns = [
        'Cod_Reduzido', 'Insc_Cadastral', 'Imovel_Endereco', 'Bairro', 'Quadra', 'Lote',
        'AreaTerritorial', 'AreaPredial', 'Testada_y', 'Cod_Prefeitura', 'Contribuinte_CPF',
        'Contribuinte_Nome', 'Contribuinte_Endereco', 'Contribuinte_CEP', 'Bairro_Contribuinte', 'CEPImovel'
    ]
    final_columns = [col for col in final_columns if col in merged_df.columns]

    final_df = merged_df[final_columns]
    final_df.to_csv(f"temp/Final_Combined_cycle{cycle}.csv", index=False)
    #final_df.to_excel(f"temp/Final_Combined_cycle{cycle}.xlsx", index=False)
    print(f"Arquivo CSV final combinado para o ciclo {cycle} criado: temp/Final_Combined_cycle{cycle}.csv")
    # O retorno deve ser o caminho absoluto do novo arquivo
    return os.path.abspath(f"temp/Final_Combined_cycle{cycle}.csv")


def process_chunk_pdf(csv_filepath, concurrent_threads):
    """
    Coordena a execução de todas as etapas do processamento de pedaços de PDFs.

    Args:
        csv_filepath (str): Caminho para o arquivo CSV a ser processado.
        concurrent_threads (int): Número de threads simultâneas a serem usadas.
    """
    start_time = time.time()
    
    # Inicializa os diretórios necessários
    initialize_directories()
    
    # Lê o DataFrame original a partir do CSV
    df_original = read_original_dataframe(csv_filepath)
    
    # Aguarda alguns segundos antes de iniciar o processamento
    wait_before_start()
    
    # Processa os pedaços do DataFrame original usando threads simultâneas
    last_cycle = process_dataframe_chunks(df_original, concurrent_threads, concurrent_threads)
    
    # Combina os arquivos CSV gerados em um único DataFrame
    combined_df = combine_csv_files(last_cycle)
    
    # Faz o merge do DataFrame combinado com o DataFrame original e salva o resultado
    path = merge_and_save_intermediate_dataframe(combined_df, df_original, "final")
    clear_temp_folders()
    # Calcula e imprime o tempo total de execução
    time_taken = time.time() - start_time
    print(f"Tempo total: {time_taken:.2f} segundos")
    return path


if __name__ == "__main__":
    # Exemplo de chamada para a função process_chunk_pdf
    process_chunk_pdf("C:/Users/arthu/OneDrive/Desktop/Repo/Integracao/scrape_pdf/Base.csv", 15)
