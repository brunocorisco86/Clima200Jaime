CREATE TABLE IF NOT EXISTS acompanhamento_lotes_data (
    lote_composto TEXT NOT NULL,
    Grandeza TEXT NOT NULL,
    Idade INTEGER,
    Data TEXT,
    -- Columns for ConsumoEnergia
    Referencia_kwh REAL,
    Consumo_automatico_kwh REAL,
    Relacao_auto TEXT,
    Consumo_manual_kwh REAL,
    Relacao_manual TEXT,
    -- Columns for Mortalidade
    Mortalidade_un INTEGER,
    Mortalidade_percent REAL,
    Referencia_percent REAL,
    Relacao_mortalidade TEXT -- Renamed from "Relação" to avoid conflict
);