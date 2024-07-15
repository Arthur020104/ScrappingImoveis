import pandas as pd
import os
from scrape_pdf.main import process_chunk_pdf
from .dmae import request_new_dmae_data
from .partes import primeira_parte, segunda_parte, terceira_parte, quarta_parte

script_dir = os.path.dirname(__file__)
arr_keys_new = ["Cod_Reduzido", "Insc_Cadastral", "Imovel_Endereco", "Bairro", "Quadra", "Lote", "Area Territorial", "Area Predial", "Testada", "Cod_Prefeitura", "Contribuinte_CPF", "Contribuinte_Nome", "Contribuinte_Endereco", "Contribuinte_CEP", "Bairro_Contribuinte", "CEPImovel"]
arr_keys_old = ["Insc_Cadastral", "CEPImovel", "AreaTerritorial", "Testada_y", "AreaPredial", "Cod_Reduzido", "Imovel_Endereco", "Bairro", "Quadra", "Lote", "Cod_Prefeitura", "Contribuinte_CPF", "Contribuinte_Nome", "Contribuinte_Endereco", "Contribuinte_CEP", "Bairro_Contribuinte"]

def request_new_pdf_data(start_code, end_code: int, records_per_chunk: int, concurrent_chunks: int, parte:int ,delete_file=True, is_using_complete_code=False):
    """
    Processa e compara dados novos com dados existentes, atualizando e 
    acrescentando conforme necessário.

    Args:
        start_code(int,str): Código inicial para busca de dados. Pode ser um código completo, quando is_using_complete_code=True. Exemplo pode ser '00 03 0102 15 10 0001 0009' ou um codigo simples 10
        end_code (int): Código final para busca de dados. Pode ser um int que não será processado, mas sim será usado como range, basicamente start_code + i for i in range(end_code).
        records_per_chunk (int): Número de registros por lote.
        concurrent_chunks (int): Número de lotes concorrentes.
        is_using_complete_code (bool): Se estiver recebendo um codigo completo e quer achar outros imoveis a partir dele
        parte (int): parte a ser mudada do codigo completo usa o range. Se for 1 e codigo inicial '00 03 0102 15 10 0001 0009' os codigos serao ['00030102151000010009', '00030102151000010010', '00030102151000010011', '00030102151000010012', '00030102151000010013', '00030102151000010014', '00030102151000010015', '00030102151000010016', '00030102151000010017', '00030102151000010018']
    Returns:
        None or new_file(PATH)
        new_file (str): Caminho para o arquivo CSV com os novos dados. É retornado quando delete_file=False.
    """
    try:
        if is_using_complete_code:
            start_code = str(start_code)
            start_code = start_code.replace(' ','')
            complete_number = start_code
            mix = int(complete_number[4:])
            fixed_pattern = f'{complete_number[:5]}'
            parte = parte  # Exemplo, poderia ser um parâmetro
            range_num = end_code 
            # Initialize lists and dictionaries
            numbers_list = []
            all_info = {}
            list_dict = []
            formatted_numbers = []
            # Process data based on user inputs
            try:
                if parte == 1:
                    primeira_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num)
                elif parte == 2:
                    segunda_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num)
                elif parte == 3:
                    terceira_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num)
                elif parte == 4:
                    quarta_parte(mix, numbers_list, formatted_numbers, fixed_pattern, range_num)
            except Exception as e:
                return None, f"Erro no processamento alternativo: {e}"
        # Processa e obtém os novos dados da prefeitura e do DMAE
        new_file_dmae_cod, status = request_new_dmae_data(start_code=start_code, end_code=end_code, records_per_chunk=records_per_chunk, concurrent_chunks=concurrent_chunks, delete_file=False, receving_list=is_using_complete_code, complete_code_list=formatted_numbers)
        if not new_file_dmae_cod:
            return None, status
        new_file = process_chunk_pdf(csv_filepath=new_file_dmae_cod, concurrent_threads=concurrent_chunks)
        new_data = pd.read_csv(new_file)
        # Verifica se o caminho do arquivo CSV atual existe
        current_data_path = os.path.join(script_dir, '..', 'BaseDeDados', 'AreaTerritorial', 'Base.csv')
        if not os.path.exists(current_data_path):
            raise FileNotFoundError(f"Arquivo {current_data_path} não encontrado.")

        # Lê os dados atuais do arquivo CSV existente
        current_data = pd.read_csv(current_data_path)

        # Concatena os DataFrames atual e novo
        concatenated_df = pd.concat([current_data, new_data], ignore_index=True)

        # Remove duplicatas com base na coluna 'Insc_Cadastral', mantendo a última ocorrência
        concatenated_df.drop_duplicates(subset=['Insc_Cadastral'], keep='last', inplace=True)
        
        # Verifica e atualiza registros existentes onde 'Insc_Cadastral' é igual e outros campos são diferentes
        for idx, row in new_data.iterrows():
            mask = concatenated_df['Insc_Cadastral'] == row['Insc_Cadastral']
            if mask.any():
                current_row = concatenated_df.loc[mask].iloc[0]
                if any(current_row[col] != row[col] for col in arr_keys_old):
                    concatenated_df.loc[mask, arr_keys_old] = row[arr_keys_old].values

        # Salva o DataFrame atualizado de volta no arquivo CSV
        concatenated_df.to_csv(current_data_path, index=False)
        os.remove(new_file_dmae_cod)  # Remove o arquivo temporário do dmae
        if delete_file:
            os.remove(new_file)
            return None
        else:
            return new_file, f"Dados processado e salvos em "
    except Exception as e:
        return None, f"Erro ao processar os dados de Area Territorial: {e}"

if __name__ == '__main__':
    request_new_pdf_data(start_code='00 03 0102 15 10 0001 0009', end_code=10, records_per_chunk=50, concurrent_chunks=5, parte=1, delete_file=False, is_using_complete_code=True)
