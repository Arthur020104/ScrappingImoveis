import pandas as pd
import os
from projeto_de_busca_de_dados_pelo_codigo_reduzido_prefeitura.main import process_chunks as process_prefeitura_chunks

script_dir = os.path.dirname(__file__)

def request_new_prefeitura_data(start_code: int, end_code: int, records_per_chunk: int, concurrent_chunks: int, delete_file=True):
    """
    Processa e compara dados novos com dados existentes, atualizando e 
    acrescentando conforme necessário.

    Args:
        start_code (int): Código inicial para busca de dados.
        end_code (int): Código final para busca de dados.
        records_per_chunk (int): Número de registros por lote.
        concurrent_chunks (int): Número de lotes concorrentes.
        delete_file (bool): Deletar arquivo após a execução.
    Returns:
        None or new_file
        new_file (str): Caminho para o arquivo CSV com os novos dados. É retornado quando delete_file=False.
    """
    try:
        # Processa e obtém os novos dados
        new_file = process_prefeitura_chunks(start_code=start_code, end_code=end_code, records_per_chunk=records_per_chunk, concurrent_chunks=concurrent_chunks)
        new_data = pd.read_csv(new_file)
        
        # Limpeza dos novos dados
        print(f'\n\n{new_data}\n\n')
        new_data['codigo'] = new_data['codigo'].astype(str)
        new_data['codigo_reduzido'] = new_data['codigo_reduzido'].astype(str)
        new_data['endereco'] = new_data['endereco'].astype(str)
        new_data['codigo_completo'] = new_data['codigo_completo'].astype(str)
        new_data.drop_duplicates(subset=['codigo'], inplace=True)
        new_data.dropna(subset=['codigo'], inplace=True)
        print(f'\n\n{new_data}\n\n')

        # Lê os dados atuais do arquivo CSV existente
        current_data = pd.read_csv(os.path.join(script_dir, '..', 'BaseDeDados', 'CodigosCompletos', 'Base.csv'))

        # Concatena os DataFrames atual e novo
        concatenated_df = pd.concat([current_data, new_data], ignore_index=True)

        # Remove duplicatas com base na coluna 'codigo', mantendo a última ocorrência
        concatenated_df.drop_duplicates(subset=['codigo'], keep='last', inplace=True)

        # Verifica e atualiza registros existentes onde 'codigo_reduzido' é igual e outros campos são diferentes
        for idx, row in new_data.iterrows():
            mask = concatenated_df['codigo'] == row['codigo']
            if mask.any():
                current_row = concatenated_df.loc[mask].iloc[0]
                if (current_row['codigo_reduzido'] == row['codigo_reduzido'] and 
                    (current_row['endereco'] != row['endereco'] or current_row['codigo_completo'] != row['codigo_completo'])):
                    concatenated_df.loc[mask, ['endereco', 'codigo_completo']] = row[['endereco', 'codigo_completo']].values

        # Salva o DataFrame atualizado de volta no arquivo CSV
        concatenated_df.to_csv(os.path.join(script_dir, '..', 'BaseDeDados', 'CodigosCompletos', 'Base.csv'), index=False)
        
        if delete_file:
            os.remove(new_file)
            return None
        else:
            return new_file

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        return None

# Chamada de exemplo para a função
# request_new_prefeitura_data(start_code=1000, end_code=2000, records_per_chunk=100, concurrent_chunks=5)


# Exemplo de uso da função:
if __name__ == '__main__':
    request_new_prefeitura_data(420000, 420100, 5000, 10)
