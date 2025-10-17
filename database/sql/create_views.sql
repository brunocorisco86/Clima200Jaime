-- View for daily IoT data summary
CREATE VIEW IF NOT EXISTS daily_iot_summary AS
SELECT
    lote_composto,
    Grandeza,
    Local,
    Data,
    AVG(Valor) AS average_valor
FROM
    eprodutor_iot_data
GROUP BY
    lote_composto, Grandeza, Local, Data;

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
    lp.teste_realizado,
    AVG(CASE WHEN eis.Grandeza = 'UMIDADE' THEN eis.Valor ELSE NULL END) AS avg_umidade,
    AVG(CASE WHEN eis.Grandeza = 'TEMPERATURA' THEN eis.Valor ELSE NULL END) AS avg_temperatura,
    AVG(CASE WHEN eis.Grandeza = 'AMONIA' THEN eis.Valor ELSE NULL END) AS avg_amonia,
    AVG(CASE WHEN eis.Grandeza = 'CORRENTE' THEN eis.Valor ELSE NULL END) AS avg_corrente,
    AVG(CASE WHEN eis.Grandeza = 'ENERGIA' THEN eis.Valor ELSE NULL END) AS avg_energia,
    AVG(CASE WHEN eis.Grandeza = 'PRESSAO' THEN eis.Valor ELSE NULL END) AS avg_pressao
FROM
    lote_composto lp
LEFT JOIN
    eprodutor_iot_data eis ON lp.lote_composto = eis.lote_composto
GROUP BY
    lp.lote_composto, lp.data_alojamento, lp.linhagem, lp.aves_alojadas, lp.aves_abatidas,
    lp.mortalidade_percent, lp.idade_abate, lp.conversao_ajustada, lp.iep, lp.peso_medio,
    lp.aero_parcial, lp.condenacao_efetiva_kg, lp.contaminacao_parcial, lp.remuneracao_sqr_meter_brl,
    lp.teste_realizado;
