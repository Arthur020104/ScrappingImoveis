import pandas as pd
import os
from .prefeitura import resquest_new_prefeitura_data
from projeto_de_busca_de_dados_pelo_codigo_completo_dmae.main import process_chunks as process_dmae_chunks

script_dir = os.path.dirname(__file__)

def resquest_new_dmae_data(start_code:int, end_code:int, records_per_chunk:int, concurrent_chunks:int):
    """
    Processa e compara dados novos com dados existentes, atualizando e 
    acrescentando conforme necessário.

    Args:
        start_code (int): Código inicial para busca de dados.
        end_code (int): Código final para busca de dados.
        records_per_chunk (int): Número de registros por lote.
        concurrent_chunks (int): Número de lotes concorrentes.

    Returns:
        None
    """
    # Processa e obtém os novos dados da prefeitura e do DMAE
    new_file_pref_cod = resquest_new_prefeitura_data(start_code=start_code, end_code=end_code, records_per_chunk=records_per_chunk, concurrent_chunks=concurrent_chunks, delete_file=False)
    new_file = process_dmae_chunks(file_path=new_file_pref_cod, save_number=records_per_chunk, concurrent_chunks=concurrent_chunks)
    new_data = pd.read_csv(new_file)
    
    # Lê os dados atuais do arquivo CSV existente
    current_data = pd.read_csv(os.path.join(script_dir, '..', 'BaseDeDados', 'Informacao_baseada_em_codigo_completo', 'Base.csv'))
    try:
        # Faz a mesclagem dos DataFrames atual e novo com base na coluna 'Cod_Reduzido'
        merged_df = pd.merge(current_data, new_data, on='Cod_Reduzido', how='outer', suffixes=('_old', '_new'))

        # Atualiza os registros existentes com novos dados onde 'Cod_Reduzido' for igual e outros campos forem diferentes
        update_mask = (
            (merged_df['Insc_Cadastral_old'] != merged_df['Insc_Cadastral_new']) |
            (merged_df['Imovel_Endereco_old'] != merged_df['Imovel_Endereco_new']) |
            (merged_df['Bairro_old'] != merged_df['Bairro_new']) |
            (merged_df['Quadra_old'] != merged_df['Quadra_new']) |
            (merged_df['Lote_old'] != merged_df['Lote_new']) |
            (merged_df['Area Territorial_old'] != merged_df['Area Territorial_new']) |
            (merged_df['Area Predial_old'] != merged_df['Area Predial_new']) |
            (merged_df['Testada_old'] != merged_df['Testada_new']) |
            (merged_df['Cod_Prefeitura_old'] != merged_df['Cod_Prefeitura_new']) |
            (merged_df['Contribuinte_CPF_old'] != merged_df['Contribuinte_CPF_new']) |
            (merged_df['Contribuinte_Nome_old'] != merged_df['Contribuinte_Nome_new']) |
            (merged_df['Contribuinte_Endereco_old'] != merged_df['Contribuinte_Endereco_new']) |
            (merged_df['Contribuinte_CEP_old'] != merged_df['Contribuinte_CEP_new']) |
            (merged_df['Bairro_Contribuinte_old'] != merged_df['Bairro_Contribuinte_new'])
        )

        # Atualiza os registros nos dados atuais
        columns_to_update = [
            'Insc_Cadastral', 'Imovel_Endereco', 'Bairro', 'Quadra', 'Lote',
            'Area Territorial', 'Area Predial', 'Testada', 'Cod_Prefeitura', 'Contribuinte_CPF',
            'Contribuinte_Nome', 'Contribuinte_Endereco', 'Contribuinte_CEP', 'Bairro_Contribuinte'
        ]
        for column in columns_to_update:
            merged_df.loc[update_mask, f'{column}_old'] = merged_df.loc[update_mask, f'{column}_new']

        # Renomeia as colunas para os nomes originais
        merged_df.rename(columns={f'{col}_old': col for col in columns_to_update}, inplace=True)

        # Remove as colunas desnecessárias dos novos dados
        merged_df.drop(columns=[f'{col}_new' for col in columns_to_update], inplace=True)

        # Remove as linhas duplicadas
        merged_df.drop_duplicates(subset=['Cod_Reduzido'], inplace=True)

        # Salva o DataFrame atualizado de volta no arquivo CSV
        merged_df.to_csv(os.path.join(script_dir, '..', 'BaseDeDados', 'Informacao_baseada_em_codigo_completo', 'Base.csv'), index=False)
    except:
        pass
if __name__ == '__main__':
    resquest_new_dmae_data(start_code=1, end_code=130, records_per_chunk=50, concurrent_chunks=5)