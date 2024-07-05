import os
import shutil
import tempfile
import time
def deleteFilesInFolderAndFolder(folder_path):
    for _ in range(2):
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(folder_path)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(3)
    return False

def clear_temp_folders():
    # Obtém o diretório temporário do sistema
    temp_dir = tempfile.gettempdir()
    
    # Itera por todos os arquivos e pastas dentro do diretório temporário
    arquivos_nao_deletados = 0
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        
        try:
            # Se for um arquivo, remove
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # Se for um diretório, remove recursivamente
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            arquivos_nao_deletados += 1
    print(f"Arquivos não deletados: {arquivos_nao_deletados}")