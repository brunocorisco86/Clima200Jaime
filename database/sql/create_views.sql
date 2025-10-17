-- View for daily IoT data summary
CREATE VIEW IF NOT EXISTS daily_iot_summary AS
SELECT
    eis.lote_composto,
    eis.Grandeza,
    eis.Local,
    eis.Data,
    AVG(eis.Valor) AS average_valor,
    MAX(eis.Valor) AS max_valor,
    MIN(eis.Valor) AS min_valor,
    SQRT(AVG(eis.Valor*eis.Valor) - AVG(eis.Valor)*AVG(eis.Valor)) AS std_valor,
    (MAX(eis.Valor) - MIN(eis.Valor)) AS amplitude_valor,
    CAST(julianday(SUBSTR(eis.Data, 7, 4) || '-' || SUBSTR(eis.Data, 4, 2) || '-' || SUBSTR(eis.Data, 1, 2)) - 
         julianday(SUBSTR(lp.data_alojamento, 7, 4) || '-' || SUBSTR(lp.data_alojamento, 4, 2) || '-' || SUBSTR(lp.data_alojamento, 1, 2)) AS INTEGER) AS idade_lote,
    lp.teste_realizado -- New column
FROM
    eprodutor_iot_data eis
JOIN
    lote_composto lp ON eis.lote_composto = lp.lote_composto
GROUP BY
    eis.lote_composto, eis.Grandeza, eis.Local, eis.Data, lp.data_alojamento, lp.teste_realizado; -- Added to GROUP BY

-- View for combined lote performance and average sensor data
CREATE VIEW IF NOT EXISTS lote_performance_summary AS
SELECT
    lp.lote_composto,
    lp.data_alojamento,
    lp.linhagem,
    lp.aves_alojadas,
    lp.aves_abatidas,
    lp.mortalidade_percent,
    lp.idade_abate,
    lp.conversao_ajustada,
    lp.iep,
    lp.peso_medio,
    lp.aero_parcial,
    lp.condenacao_efetiva_kg,
    lp.contaminacao_parcial,
    lp.remuneracao_sqr_meter_brl,
    lp.teste_realizado
FROM
    lote_composto lp
LEFT JOIN
    eprodutor_iot_data eis ON lp.lote_composto = eis.lote_composto
GROUP BY
    lp.lote_composto, lp.data_alojamento, lp.linhagem, lp.aves_alojadas, lp.aves_abatidas,
    lp.mortalidade_percent, lp.idade_abate, lp.conversao_ajustada, lp.iep, lp.peso_medio,
    lp.aero_parcial, lp.condenacao_efetiva_kg, lp.contaminacao_parcial, lp.remuneracao_sqr_meter_brl,
    lp.teste_realizado;

-- View for distinct Grandeza values
CREATE VIEW IF NOT EXISTS distinct_grandezas AS
SELECT DISTINCT Grandeza
FROM eprodutor_iot_data;