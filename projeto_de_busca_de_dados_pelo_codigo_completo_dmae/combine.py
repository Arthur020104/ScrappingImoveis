import pandas as pd
# List of input CSV files
input_files = []
#input_files = [f'alldata/output_{i}.csv'for i in range(0, 13)]
input_files.append("combined_output.csv")
input_files.append("combined_output1.csv")
# Output CSV file
output_file = 'DadosComCodigosCompletos.csv'

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Concatenate the data from input CSV files
for file in input_files:
    try:
        data = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file}")
        continue
    combined_data = pd.concat([combined_data, data], ignore_index=True)
    combined_data = combined_data.drop_duplicates(keep='first')

# Write the combined data to the output CSV file
combined_data.to_csv(output_file, index=False)
combined_data.to_excel('DadosComCodigosCompletos.xlsx', index=False)
# Count the number of occurrences of each codigo_completo
codigo_counts = combined_data['Insc_Cadastral'].value_counts()

# Print the number of unique codigo_completo values
print(f"Number of unique codigo_completo values: {len(codigo_counts)}")
print(f"Combined data saved to {output_file} and combined1.xlsx")