import pandas as pd
import os
from .prefeitura import request_new_prefeitura_data
from projeto_de_busca_de_dados_pelo_codigo_completo_dmae.main import process_chunks as process_dmae_chunks

script_dir = os.path.dirname(__file__)
arr_keys = ['Insc_Cadastral', 'Imovel_Endereco', 'Bairro', 'Quadra', 'Lote', 'Area Territorial',
                        'Area Predial', 'Testada', 'Cod_Prefeitura', 'Contribuinte_CPF', 'Contribuinte_Nome',
                        'Contribuinte_Endereco', 'Contribuinte_CEP', 'Bairro_Contribuinte']
def request_new_dmae_data(start_code: int, end_code: int, records_per_chunk: int, concurrent_chunks: int, delete_file=True):
    """
    Processa e compara dados novos com dados existentes, atualizando e 
    acrescentando conforme necessário.

    Args:
        start_code (int): Código inicial para busca de dados.
        end_code (int): Código final para busca de dados.
        records_per_chunk (int): Número de registros por lote.
        concurrent_chunks (int): Número de lotes concorrentes.

    Returns:
        None or new_file(PATH)
        new_file (str): Caminho para o arquivo CSV com os novos dados. É retornado quando delete_file=False.
    """
    try:
        # Processa e obtém os novos dados da prefeitura e do DMAE
        new_file_pref_cod, status = request_new_prefeitura_data(start_code=start_code, end_code=end_code, records_per_chunk=records_per_chunk, concurrent_chunks=concurrent_chunks, delete_file=False)
        if not new_file_pref_cod:
            return None, status
        new_file = process_dmae_chunks(file_path=new_file_pref_cod, save_number=records_per_chunk, concurrent_chunks=concurrent_chunks)
        new_data = pd.read_csv(new_file)
        
        # Lê os dados atuais do arquivo CSV existente
        current_data_path = os.path.join(script_dir, '..', 'BaseDeDados', 'Informacao_baseada_em_codigo_completo', 'Base.csv')
        current_data = pd.read_csv(current_data_path)
        
        # Concatena os DataFrames atual e novo
        concatenated_df = pd.concat([current_data, new_data], ignore_index=True)

        # Remove duplicatas com base na coluna 'Cod_Reduzido', mantendo a última ocorrência
        concatenated_df.drop_duplicates(subset=['Cod_Reduzido'], keep='last', inplace=True)

        # Verifica e atualiza registros existentes onde 'Cod_Reduzido' é igual e outros campos são diferentes
        for idx, row in new_data.iterrows():
            mask = concatenated_df['Cod_Reduzido'] == row['Cod_Reduzido']
            if mask.any():
                current_row = concatenated_df.loc[mask].iloc[0]
                if any(
                    current_row[col] != row[col] for col in arr_keys
                ):
                    concatenated_df.loc[mask, arr_keys] = row[arr_keys].values

        # Salva o DataFrame atualizado de volta no arquivo CSV
        concatenated_df.to_csv(current_data_path, index=False)
        os.remove(new_file_pref_cod)# Remove o arquivo temporário da prefeitura
        if(delete_file):
            os.remove(new_file)
            return None
        else:
            return new_file, f"Dados processado e salvos em "
    except Exception as e:
        print(f"Erro ao processar os dados do Dmae: {e}")
        return None, f"Erro ao processar os dados do Dmae: {e}"
        

if __name__ == '__main__':
    request_new_dmae_data(start_code=1, end_code=130, records_per_chunk=50, concurrent_chunks=5, delete_file=False)
