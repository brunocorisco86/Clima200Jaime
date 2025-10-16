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

A estrutura de pastas para os dados brutos (`/data/raw`) foi organizada da seguinte forma, considerando que os arquivos de "Sensores" contêm dados de ambos os aviários e são separados por tipo de grandeza e intervalo de 15 dias. A estrutura completa do projeto é:

```
/home/brunoconter/Code/Git/Clima200JaimeBasso/
├── data/
│   └── raw/
│       ├── Amonia/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       ├── Temperatura/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       ├── Consumo_Silo/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       ├── Pressao_Diferencial/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       ├── Umidade_Relativa/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       ├── Corrente_Eletrica/
│       │   ├── 2025-08-19_2025-09-02/
│       │   ├── 2025-09-03_2025-09-17/
│       │   └── 2025-09-18_2025-10-02/
│       └── Energia_Eletrica/
│           ├── 2025-08-19_2025-09-02/
│           ├── 2025-09-03_2025-09-17/
│           └── 2025-09-18_2025-10-02/
├── database/
│   ├── clima.db
│   ├── create_dados_lotes_table.sql
│   ├── create_lote_composto_table.sql
│   ├── insert_lote_composto_data.sql
│   └── sql/
│       ├── create_dados_lotes_table.sql
│       ├── create_lote_composto_table.sql
│       └── insert_lote_composto_data.sql
└── src/
    ├── create_db.py
    ├── process_exports.py
    └── utils/
        └── logger.py
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