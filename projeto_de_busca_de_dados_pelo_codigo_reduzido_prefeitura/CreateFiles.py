import pandas as pd

# Specify the path to your Excel file
excel_file = "Dados PMU 2013.xlsx"

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file, sheet_name='Dados PMU 2013')

# Get unique values from the "Codigo" column
unique_codigos = df['Codigo'].unique().tolist()
print(f'Tamanho da lista de codigos: {len(unique_codigos)}')
# Read unique codigo_reduzido from the combined.csv file
combined_file = "combined.csv"
df_combined = pd.read_csv(combined_file)
unique_codigo_reduzido = df_combined['codigo_reduzido'].unique().tolist()

print(f'Tamanho da lista de codigo_reduzido: {len(unique_codigo_reduzido)}')
# Remove common elements from unique_codigos and unique_codigo_reduzido
unique_codigos = list(set(unique_codigos) - set(unique_codigo_reduzido))
print(f'Tamanho da lista de codigos: {len(unique_codigos)}')
# Divide the list into 4 other lists
n = len(unique_codigos)
chunk_size1 = int(n * 0.30)
chunk_size2 = int(n * 0.30)
chunk_size3 = n - chunk_size1 - chunk_size2

list_of_lists = [unique_codigos[:chunk_size1], unique_codigos[chunk_size1:chunk_size1+chunk_size2], unique_codigos[chunk_size1+chunk_size2:]]
number_list = 0
for lista in list_of_lists:
    
    un = []
    for i in lista:
        un.append(str(i).replace(".0", ""))
    # Write unique codigos to a txt file
    with open(f'unique_codigos{number_list}.txt', 'w') as file:
        for codigo in un:
            file.write(codigo + '\n')
    number_list += 1

# Read unique codigos from the txt file
#with open('unique_codigos.txt', 'r') as file:
#    unique_codigos_from_file = [line.strip() for line in file]
"""
# Print the list of unique codigos
print(ls)
ls = unique_codigos_from_file

print(ls)
print(get_cod_completo.get_property_number_and_adress(unique_codigos_from_file))

# Print the list of unique codigos
#print(unique_codigos[0:500])
#ls = []
#for i in unique_codigos[0:500]:
  #  ls.append(str(int(i)))
#print(ls)
#print(get_cod_completo.get_property_number_and_adress(ls))
"""