# Interface de Processamento de Dados

Este projeto consiste em uma interface gráfica desenvolvida para fazer scrapping de informações imobiliárias de Uberlândia.

## Funcionalidades

A interface possui três abas distintas:

1. **Prefeitura**
2. **DMAE**
3. **Área Territorial**

### Prefeitura

Campos:
- Código Inicial
- Código Final
- Registros por Lote
- Lotes Concorrentes
- Atualizar base de dados (checkbox)
- Selecionar Pasta
- Processar Dados da Prefeitura (botão)

Formato do CSV gerado:
```
codigo,endereco,codigo_completo,codigo_reduzido
10101010200160000,"RUA URANO, 13",IMO: 00.01.0101.01.02.0016.0000,61
```
![Interface Prefeitura](./Images/Prefeitura.png)
### DMAE

Campos:
- Código Inicial
- Código Final
- Registros por Lote
- Lotes Concorrentes
- Atualizar base de dados (checkbox)
- Selecionar Pasta
- Processar Dados do DMAE (botão)

Formato do CSV gerado:
```
Cod_Reduzido,Insc_Cadastral,Imovel_Endereco,Bairro,Quadra,Lote,Area Territorial,Area Predial,Testada,Cod_Prefeitura,Contribuinte_CPF,Contribuinte_Nome,Contribuinte_Endereco,Contribuinte_CEP,Bairro_Contribuinte
187,00 01 0101 01 07 0002 0002,"AVENIDA CONSTELACAO, 52 - FUNDOS",PRESIDENTE ROOSEVELT,116B,0017,0,0,0,297342,600.079.901-20,ELIANA ROSA DA SILVA,"AVENIDA CONSTELACAO, 52",38.401-127,PRESIDENTE ROOSEVELT - UBERLANDIA/MG
```
![Interface DMAE](./Images/Dmae.png)
### Área Territorial

Campos:
- Código Inicial
- Código Final
- Registros por Lote
- Lotes Concorrentes
- Atualizar base de dados (checkbox)
- Selecionar Pasta
- Processar Dados da Área Territorial (botão)

Formato do CSV gerado:
```
Cod_Reduzido,Insc_Cadastral,Imovel_Endereco,Bairro,Quadra,Lote,AreaTerritorial,AreaPredial,Testada_y,Cod_Prefeitura,Contribuinte_CPF,Contribuinte_Nome,Contribuinte_Endereco,Contribuinte_CEP,Bairro_Contribuinte,CEPImovel
15,00 01 0101 01 01 0005 0004,"RUA ESTRELA DALVA, 254",JARDIM BRASILIA,0064,0005,"4,477375","32,340000","12,000000",152669,159.899.926-53,DEVANIDES DE OLIVEIRA,"RUA URANO, 100",38.401-372,JARDIM BRASILIA - UBERLANDIA/MG,38401372.0
```
![Interface Area Territorial](./Images/AreaTerritorial.png)
