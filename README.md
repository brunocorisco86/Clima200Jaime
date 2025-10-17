# Análise de Dados do Teste Clima200 (Jaime Basso)

Este repositório foi criado para organizar e processar os dados do teste do equipamento Clima200 da Vencomatic, realizado na granja de frangos de corte do proprietário Jaime Basso.

## Contexto do Teste

*   **Aviário Instalado (Clima200):** 1283
*   **Aviário Testemunha:** 1282
*   **Plataforma de Extração:** eProdutor (extração de 15 em 15 dias)
*   **Datas:**
    *   Pré-Alojamento: 19/08/2025
    *   Alojamento: 20/08/2025
    *   Abate: 01/10/2025
*   **Dados Coletados:** Amônia, Temperatura, Consumo Silo (Máximo), Pressão Diferencial, Umidade Relativa, Corrente Elétrica, Energia Elétrica do Dia (Máximo).

## Estrutura de Pastas

A estrutura de pastas foi organizada para separar os dados brutos de acordo com sua origem e tipo.

```
/home/brunoconter/Code/Git/Clima200JaimeBasso/
├───README.md
├───.git/...
├───data/
│   └───raw/
│       ├───exportAcompanhamentoLotes/
│       │   ├───export_consumo_energia_1282_19.csv
│       │   ├───export_consumo_energia_1283_19.csv
│       │   ├───export_consumo_racao_1282_19.csv
│       │   ├───export_consumo_racao_1283_19.csv
│       │   ├───export_mortalidade_1282_19.csv
│       │   └───export_mortalidade_1283_19.csv
│       └───exportEprodutorIOT/
│           ├───Amonia/
│           │   └───lote_19/
│           │       ├───AmoniaSensores_lote_19.csv
│           │       ├───AmoniaSensores2_lote_19.csv
│           │       └───AmoniaSensores3_lote_19.csv
│           ├───Consumo_Silo/
│           │   └───lote_19/
│           │       ├───ConsumoSiloSensores_lote_19.csv
│           │       ├───ConsumoSiloSensores2_lote_19.csv
│           │       └───ConsumoSiloSensores3_lote_19.csv
│           ├───Corrente_Eletrica/
│           │   └───lote_19/
│           │       ├───CorrenteEletricaSensores_lote_19.csv
│           │       ├───CorrenteEletricaSensores2_lote_19.csv
│           │       └───CorrenteEletricaSensores3_lote_19.csv
│           ├───Energia_Eletrica/
│           │   └───lote_19/
│           │       ├───EnergiaEletricaSensores_lote_19.csv
│           │       ├───EnergiaEletricaSensores2_lote_19.csv
│           │       └───EnergiaEletricaSensores3_lote_19.csv
│           ├───Pressao_Diferencial/
│           │   └───lote_19/
│           │       ├───PressaoDiferencialSensores_lote_19.csv
│           │       ├───PressaoDiferencialSensores2_lote_19.csv
│           │       └───PressaoDiferencialSensores3_lote_19.csv
│           ├───Temperatura/
│           │   └───lote_19/
│           │       ├───TemperaturaSensores_lote_19.csv
│           │       ├───TemperaturaSensores2_lote_19.csv
│           │       └───TemperaturaSensores3_lote_19.csv
│           └───Umidade_Relativa/
│               └───lote_19/
│                   ├───UmidadeRelativaSensores_lote_19.csv
│                   ├───UmidadeRelativaSensores2_lote_19.csv
│                   └───UmidadeRelativaSensores3_lote_19.csv
├───database/
│   ├───clima.db
│   ├───create_dados_lotes_table.sql
│   ├───create_lote_composto_table.sql
│   ├───insert_lote_composto_data.sql
│   └───sql/
│       ├───create_amonia_table.sql
│       ├───create_dados_lotes_table.sql
│       ├───create_lote_composto_table.sql
│       └───insert_lote_composto_data.sql
├───docs/
│   └───DATAS DATA ALOJAMENTO.txt
└───src/
    ├───create_db.py
    ├───process_amonia_data.py
    ├───process_exports.py
    └───utils/
        └───logger.py
```

## Tipos de Arquivos CSV Identificados

1.  **Arquivos `Exports_Acompanhamento_Lotes` (ex: `export_consumo_energia_1283.csv`):**
    *   **Delimitador:** Vírgula (`,`)
    *   **Estrutura:** Já separados por aviário (indicado no nome do arquivo, ex: `_1283` ou `_1282`).
    *   **Exemplo de cabeçalho:** `"Idade","Data","Referência (kwh)","Consumo automático (kwh)","Relação","Consumo manual (kwh)","Relação"`

2.  **Arquivos "Sensores" (ex: `Sensores.csv`, `Sensores(1).csv`, `Sensores(2).csv`):**
    *   **Delimitador:** Ponto e vírgula (`;`)
    *   **Estrutura:** Contêm dados combinados para ambos os aviários.
    *   **Exemplo de cabeçalho:** `Grandeza;Coletor;Dispositivo;ID longa;ID curta;Canal;Local;Valor;Data;Hora;`

## Status Atual e Próximos Passos

1.  **Clarificação Urgente:** Como diferenciar os dados do `Aviário 1283` e `Aviário 1282` dentro dos arquivos "Sensores"? O campo `Coletor` mostra `CTRONICS 1284`, que não corresponde diretamente aos números dos aviários. É necessário um mapeamento ou outra coluna para essa distinção.

2.  **Criação e População do Banco de Dados:**
    *   O script `src/create_db.py` foi criado para inicializar o banco de dados SQLite (`clima.db`) na pasta `/database/` e criar as tabelas necessárias (`dados_lotes` e `lote_composto`).
    *   Os arquivos SQL em `database/sql/` (`create_dados_lotes_table.sql`, `create_lote_composto_table.sql`, `insert_lote_composto_data.sql`) são utilizados por `create_db.py` para definir a estrutura das tabelas e popular dados iniciais.

3.  **Processamento de Dados de Exportação:**
    *   O script `src/process_exports.py` foi desenvolvido para ler e processar os arquivos CSV da pasta `Exports_Acompanhamento_Lotes`.
    *   Este script é responsável por extrair os dados relevantes e inseri-los na tabela `dados_lotes` do banco de dados.

4.  **Configuração de Logging:** O arquivo `src/utils/logger.py` já foi criado para facilitar o registro de eventos e erros durante o processamento dos dados.