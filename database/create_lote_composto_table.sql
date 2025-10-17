CREATE TABLE IF NOT EXISTS lote_composto (
    lote_composto TEXT PRIMARY KEY,
    data_alojamento TEXT,
    linhagem TEXT,
    aves_alojadas INTEGER,
    aves_abatidas INTEGER,
    mortalidade_percent REAL,
    idade_abate REAL,
    conversao_ajustada REAL,
    iep INTEGER,
    peso_medio REAL,
    aero_parcial REAL,
    condenacao_efetiva_kg REAL,
    contaminacao_parcial REAL,
    remuneracao_sqr_meter_brl REAL,
    teste_realizado TEXT
);