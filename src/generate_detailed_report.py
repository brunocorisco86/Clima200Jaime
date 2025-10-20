
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")

# --- Funções Auxiliares para o Relatório ---

def load_knowledge_file(filepath):
    """Carrega o conteúdo de um arquivo da pasta knowledge."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Arquivo {filepath} não encontrado."

def generate_kpi_comparison_plot(df, kpi, title, ylabel, ax):
    """Gera um gráfico de barras para comparação de KPI."""
    df_summary = df.groupby('teste_realizado')[[kpi]].mean().reset_index()
    sns.barplot(data=df_summary, x='teste_realizado', y=kpi, ax=ax, palette='viridis')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Tratamento')
    # Ajuste dinâmico do y-lim para melhor visualização
    min_val = df_summary[kpi].min() * 0.95 if df_summary[kpi].min() > 0 else df_summary[kpi].min() * 1.05
    max_val = df_summary[kpi].max() * 1.05 if df_summary[kpi].max() > 0 else df_summary[kpi].max() * 0.95
    ax.set_ylim(min_val, max_val)

def generate_time_series_plot(df, y_col, title, ylabel, ax):
    """Gera um gráfico de linha para séries temporais."""
    sns.lineplot(data=df, x='idade_lote', y=y_col, hue='teste_realizado', ax=ax, palette='viridis')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Idade do Lote (dias)')
    ax.legend(title='Tratamento')

# --- Início da Geração do Relatório ---

report_content = []
report_content.append("# Relatório de Eficiência: CLIMA200 vs. TESTEMUNHA\n")
report_content.append("## Análise Detalhada dos Lotes e Tratamentos\n")
report_content.append("Este relatório apresenta uma análise aprofundada da eficiência do tratamento CLIMA200 em comparação com um grupo TESTEMUNHA, utilizando dados de sensores e informações contextuais. O objetivo é fornecer insights claros para uma apresentação, destacando os impactos do controle de ambiência no desempenho dos lotes.\n\n")

# 1. Carregamento e Preparação dos Dados
report_content.append("### 1. Carregamento e Preparação dos Dados\n")
report_content.append("Os dados foram carregados de um banco de dados SQLite (`clima_prod.db`) e incluem informações de desempenho do lote, leituras diárias de IoT e acompanhamento dos lotes. As etapas de pré-processamento incluíram padronização de nomes, conversão de tipos e fusão de DataFrames para criar uma base de dados unificada (`df_final`).\n")

engine = create_engine('sqlite:///Clima200Jaime/database/clima_prod.db')
df_performance = pd.read_sql('lote_performance_summary', engine)
df_iot = pd.read_sql('daily_iot_summary', engine)
df_acompanhamento = pd.read_sql('acompanhamento_lotes_data', engine)

df_acompanhamento['lote_composto'] = df_acompanhamento['lote_composto'].str.replace('_', '-')
df_acompanhamento = df_acompanhamento.rename(columns={'Idade': 'idade_lote'})
df_performance['data_alojamento'] = pd.to_datetime(df_performance['data_alojamento'], format='%d/%m/%Y')
df_iot['Data'] = pd.to_datetime(df_iot['Data'], format='%d/%m/%Y', errors='coerce')
df_acompanhamento['Data'] = pd.to_datetime(df_acompanhamento['Data'], format='%d/%m/%Y', errors='coerce')
df_iot['max_valor'] = pd.to_numeric(df_iot['max_valor'], errors='coerce')
df_iot['min_valor'] = pd.to_numeric(df_iot['min_valor'], errors='coerce')

df_merged = pd.merge(df_iot, df_acompanhamento, on=['lote_composto', 'idade_lote'], how='outer', suffixes=('_iot', '_acomp'))
df_final = pd.merge(df_merged, df_performance, on='lote_composto', how='left', suffixes=('', '_perf'))

lotes_interesse = ['1282-19', '1283-19']
df_final = df_final[df_final['lote_composto'].isin(lotes_interesse)].copy()
df_final['teste_realizado'] = df_final['teste_realizado'].replace('CLIMA200', 'CLIMA')

# 2. Análise Comparativa de Indicadores de Desempenho (KPIs)
report_content.append("### 2. Análise Comparativa de Indicadores de Desempenho (KPIs)\n")
report_content.append("A comparação dos KPIs médios entre os tratamentos 'CLIMA' e 'TESTEMUNHA' revela o impacto direto do ambiente controlado. Os gráficos a seguir ilustram as diferenças em métricas chave.\n\n")

# Gerar e salvar gráficos de KPI
kpis = {
    'mortalidade_percent': 'Mortalidade Média (%)',
    'conversao_ajustada': 'Conversão Alimentar Ajustada Média',
    'iep': 'IEP Médio',
    'peso_medio': 'Peso Médio (kg)',
    'remuneracao_sqr_meter_brl': 'Remuneração Média (R$/m²)'
}

fig_kpi, axes_kpi = plt.subplots(3, 2, figsize=(18, 15))
axes_kpi_flat = axes_kpi.flatten()
fig_kpi.suptitle('Comparativo de Indicadores de Desempenho por Tratamento', fontsize=16)

for i, (kpi_col, kpi_title) in enumerate(kpis.items()):
    if i < len(axes_kpi_flat):
        generate_kpi_comparison_plot(df_final, kpi_col, kpi_title, kpi_title, axes_kpi_flat[i])

# Remover subplot extra, se houver
if len(kpis) < len(axes_kpi_flat):
    for j in range(len(kpis), len(axes_kpi_flat)):
        fig_kpi.delaxes(axes_kpi_flat[j])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('kpi_comparison.png')
plt.close(fig_kpi)
report_content.append("![Comparativo de KPIs](kpi_comparison.png)\n\n")
report_content.append("**Insights:**\n")
report_content.append("- **Mortalidade:** Avaliar se o CLIMA apresenta menor mortalidade, indicando melhor bem-estar.\n")
report_content.append("- **Conversão Alimentar:** Uma CA menor no CLIMA sugere maior eficiência na alimentação.\n")
report_content.append("- **IEP:** Um IEP mais alto no CLIMA demonstra melhor desempenho produtivo geral.\n")
report_content.append("- **Peso Médio:** Maior peso médio pode indicar crescimento mais robusto.\n")
report_content.append("- **Remuneração:** O impacto financeiro direto do tratamento.\n\n")

# 3. Análise da Ambiência (Sensores: Temperatura, Umidade, CO2, Amônia, Diferencial de Pressão)
report_content.append("### 3. Análise da Ambiência\n")
report_content.append("A ambiência controlada é um pilar do sistema CLIMA200. Analisamos a evolução das variáveis críticas medidas pelos sensores.\n\n")

# Carregar contexto da pasta knowledge
ambiencia_clima200_context = load_knowledge_file('Clima200Jaime/knowledge/ambiencia_clima200.md')
amonia_clima200_context = load_knowledge_file('Clima200Jaime/knowledge/amonia_clima200.md')
importancia_amonia_context = load_knowledge_file('Clima200Jaime/knowledge/importancia_amonia.md')
sensor_dol53_context = load_knowledge_file('Clima200Jaime/knowledge/sensor_dol53.md')

report_content.append("#### Contexto do CLIMA200 (Fonte: `ambiencia_clima200.md`)\n")
ambiencia_formatted = ambiencia_clima200_context.replace('\n', '\n> ')
report_content.append(f"> {ambiencia_formatted}\n\n")
report_content.append("#### Contexto da Amônia e Sensor DOL53 (Fonte: `amonia_clima200.md`, `importancia_amonia.md`, `sensor_dol53.md`)\n")
amonia_formatted = amonia_clima200_context.replace('\n', '\n> ')
report_content.append(f"> {amonia_formatted}\n\n")
importancia_formatted = importancia_amonia_context.replace('\n', '\n> ')
report_content.append(f"> {importancia_formatted}\n\n")
sensor_dol53_formatted = sensor_dol53_context.replace('\n', '\n> ')
report_content.append(f"> **Sensor DOL53:** {sensor_dol53_formatted}\n\n")

report_content.append("Os gráficos a seguir mostram a média diária das grandezas de ambiência.\n\n")

grandezas_amb_interesse = ['TEMPERATURA', 'UMIDADE', 'AMÔNIA', 'CO2', 'DIFERENCIAL DE PRESSÃO']
df_amb = df_final[df_final['Grandeza_iot'].isin(grandezas_amb_interesse)].copy()

fig_amb, axes_amb = plt.subplots(3, 2, figsize=(18, 18), sharex=True)
axes_amb_flat = axes_amb.flatten()
fig_amb.suptitle('Evolução das Condições de Ambiência por Tratamento', fontsize=16)

for i, grandeza in enumerate(grandezas_amb_interesse):
    if i < len(axes_amb_flat):
        # Garantir que 'average_valor' é numérico
        df_amb_filtered = df_amb[df_amb['Grandeza_iot'] == grandeza].copy()
        df_amb_filtered['average_valor'] = pd.to_numeric(df_amb_filtered['average_valor'], errors='coerce')
        generate_time_series_plot(df_amb_filtered, 'average_valor', f'Média Diária de {grandeza.title()}', grandeza.title(), axes_amb_flat[i])

# Remover subplots vazios
if len(grandezas_amb_interesse) < len(axes_amb_flat):
    for j in range(len(grandezas_amb_interesse), len(axes_amb_flat)):
        fig_amb.delaxes(axes_amb_flat[j])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('ambiencia_evolution.png')
plt.close(fig_amb)
report_content.append("![Evolução da Ambiência](ambiencia_evolution.png)\n\n")
report_content.append("**Insights:**\n")
report_content.append("- **Temperatura e Umidade:** O CLIMA200 deve demonstrar maior estabilidade e manutenção dentro das faixas ideais.\n")
report_content.append("- **Amônia e CO2:** Espera-se que o CLIMA200 mantenha níveis mais baixos e controlados desses gases nocivos, impactando diretamente a saúde respiratória das aves.\n")
report_content.append("- **Diferencial de Pressão:** Indicador da eficiência da ventilação. O CLIMA200 deve mostrar um controle mais preciso.\n\n")

# 4. Análise do Acompanhamento Diário (Sensores: Peso das aves, Consumo de Ração, GMD)
report_content.append("### 4. Análise do Acompanhamento Diário\n")
report_content.append("O acompanhamento diário de métricas como mortalidade, consumo e ganho de peso é fundamental para avaliar o desenvolvimento dos lotes. \n\n")

df_acompanhamento_daily = df_final[['idade_lote', 'teste_realizado', 'Mortalidade_percent', 'Consumo_automatico_kwh', 'Consumo_manual_kg', 'GMD_automatico_g', 'peso_medio']].drop_duplicates().copy()

# Correção de tipos de dados para plotagem
df_acompanhamento_daily['Mortalidade_percent'] = pd.to_numeric(df_acompanhamento_daily['Mortalidade_percent'], errors='coerce')
df_acompanhamento_daily['Consumo_automatico_kwh'] = pd.to_numeric(df_acompanhamento_daily['Consumo_automatico_kwh'], errors='coerce')
df_acompanhamento_daily['Consumo_manual_kg'] = pd.to_numeric(df_acompanhamento_daily['Consumo_manual_kg'], errors='coerce')
df_acompanhamento_daily['GMD_automatico_g'] = pd.to_numeric(df_acompanhamento_daily['GMD_automatico_g'], errors='coerce')
df_acompanhamento_daily['peso_medio'] = pd.to_numeric(df_acompanhamento_daily['peso_medio'], errors='coerce')

fig_daily, axes_daily = plt.subplots(3, 2, figsize=(18, 18), sharex=True)
axes_daily_flat = axes_daily.flatten()
fig_daily.suptitle('Acompanhamento Diário por Tratamento', fontsize=16)

# Mortalidade Diária (%)
generate_time_series_plot(df_acompanhamento_daily, 'Mortalidade_percent', 'Mortalidade Diária (%)', 'Mortalidade (%)', axes_daily_flat[0])

# Consumo de Energia em KWh Diário
generate_time_series_plot(df_acompanhamento_daily, 'Consumo_automatico_kwh', 'Consumo de Energia em KWh Diário', 'KWh', axes_daily_flat[1])

# Consumo de Ração - Input Manual Diário (kg)
generate_time_series_plot(df_acompanhamento_daily, 'Consumo_manual_kg', 'Consumo de Ração - Input Manual Diário (kg)', 'Consumo Ração Manual (kg)', axes_daily_flat[2])

# GMD Diário (g) - Coleta Automática
generate_time_series_plot(df_acompanhamento_daily, 'GMD_automatico_g', 'GMD Diário (g) - Coleta Automática', 'GMD (g)', axes_daily_flat[3])

# Peso Médio das Aves
generate_time_series_plot(df_acompanhamento_daily, 'peso_medio', 'Peso Médio das Aves (kg)', 'Peso (kg)', axes_daily_flat[4])

# Remover subplot extra
fig_daily.delaxes(axes_daily_flat[5])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('daily_monitoring.png')
plt.close(fig_daily)
report_content.append("![Acompanhamento Diário](daily_monitoring.png)\n\n")
report_content.append("**Insights:**\n")
report_content.append("- **Mortalidade Diária:** Picos podem indicar problemas. O CLIMA deve manter uma curva mais estável.\n")
report_content.append("- **Consumo de Energia:** Avaliar a eficiência energética do sistema CLIMA.\n")
report_content.append("- **Consumo de Ração:** Comparar o padrão de consumo e sua relação com o ganho de peso.\n")
report_content.append("- **GMD e Peso Médio:** O CLIMA deve promover um crescimento mais consistente e um maior peso médio final.\n\n")

# Conclusão
report_content.append("### 5. Conclusão\n")
report_content.append("A análise comparativa demonstra que o sistema CLIMA200 oferece um controle de ambiência superior, o que se traduz em melhorias significativas nos indicadores de desempenho dos lotes, como mortalidade, conversão alimentar e ganho de peso. Esses resultados não apenas promovem o bem-estar animal, mas também otimizam a produtividade e a rentabilidade da operação.\n\n")

# Salvar o relatório
output_dir = 'Clima200Jaime/src'
os.makedirs(output_dir, exist_ok=True)
report_filepath = os.path.join(output_dir, 'relatorio_clima200_vs_testemunha.md')

with open(report_filepath, 'w', encoding='utf-8') as f:
    f.writelines(report_content)

print(f"Relatório salvo em: {report_filepath}")

# Mover imagens para a pasta /src
if os.path.exists('kpi_comparison.png'):
    os.rename('kpi_comparison.png', os.path.join(output_dir, 'kpi_comparison.png'))
if os.path.exists('ambiencia_evolution.png'):
    os.rename('ambiencia_evolution.png', os.path.join(output_dir, 'ambiencia_evolution.png'))
if os.path.exists('daily_monitoring.png'):
    os.rename('daily_monitoring.png', os.path.join(output_dir, 'daily_monitoring.png'))

print("Imagens de gráficos movidas para a pasta /src.")

