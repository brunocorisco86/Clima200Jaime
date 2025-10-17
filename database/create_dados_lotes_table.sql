CREATE TABLE IF NOT EXISTS dados_lotes (
    lote_composto TEXT NOT NULL,
    idade INTEGER NOT NULL,
    data TEXT NOT NULL,
    energia_referencia_kwh REAL,
    energia_consumo_automatico_kwh REAL,
    peso_referencia_g REAL,
    peso_automatico_g_ave REAL,
    racao_referencia_kg REAL,
    racao_automatica_kg REAL,
    racao_manual_kg REAL,
    mortalidade_un INTEGER,
    mortalidade_percent REAL,
    mortalidade_referencia_percent REAL,
    PRIMARY KEY(lote_composto, idade)
);
