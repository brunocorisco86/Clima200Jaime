import argparse
import sqlite3
import pandas as pd
import os
import glob
import re
import matplotlib.pyplot as plt
from functools import reduce
from scipy.stats import mannwhitneyu

# =============================================================================
# Data Processing Classes (from existing src files)
# =============================================================================

class AcompanhamentoLotesProcessor:
    """
    Processes raw 'Acompanhamento de Lotes' data from CSV files.
    """
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.file_processing_map = {
            'ConsumoEnergia': self._process_consumo_energia,
            'ConsumoRacao': self._process_consumo_racao,
            'GMD': self._process_gmd,
            'Mortalidade': self._process_mortalidade,
        }

    def _process_consumo_energia(self, file_path, lote_composto):
        df = pd.read_csv(file_path, sep=',', decimal='.', quotechar='"')
        df = df[['Idade', 'Consumo automático (kwh)']]
        df = df.rename(columns={'Idade': 'idade', 'Consumo automático (kwh)': 'energia_consumo_automatico_kwh'})
        df['lote_composto'] = lote_composto
        return df

    def _process_consumo_racao(self, file_path, lote_composto):
        df = pd.read_csv(file_path, sep=',', decimal='.', quotechar='"')
        df = df[['Idade', 'Ração automática (kg)', 'Referência (kg)']]
        df = df.rename(columns={'Idade': 'idade', 'Ração automática (kg)': 'racao_consumo_g_ave', 'Referência (kg)': 'racao_referencia_g_ave'})
        df['lote_composto'] = lote_composto
        return df

    def _process_gmd(self, file_path, lote_composto):
        df = pd.read_csv(file_path, sep=',', decimal='.', quotechar='"')
        df = df[['Idade', 'GMD automático (g)', 'Referência (g)']]
        df = df.rename(columns={'Idade': 'idade', 'GMD automático (g)': 'gmd_g', 'Referência (g)': 'gmd_referencia_g'})
        df['lote_composto'] = lote_composto
        return df

    def _process_mortalidade(self, file_path, lote_composto):
        df = pd.read_csv(file_path, sep=',', decimal='.', quotechar='"')
        df = df[['Idade', 'Mortalidade (%)', 'Referência (%)']]
        df = df.rename(columns={'Idade': 'idade', 'Mortalidade (%)': 'mortalidade_acumulada_percent', 'Referência (%)': 'mortalidade_referencia_percent'})
        df['lote_composto'] = lote_composto
        return df

    def process_files(self):
        metric_dfs = {}
        for folder_name, process_function in self.file_processing_map.items():
            search_pattern = os.path.join(self.base_directory, '**', folder_name, '*.csv')
            dfs_for_metric = []
            for file_path in glob.glob(search_pattern, recursive=True):
                try:
                    match = re.search(r'(\d+_\d+)', os.path.basename(file_path))
                    if match:
                        lote_composto_short = match.group(1).replace('_', '-')
                        processed_df = process_function(file_path, lote_composto_short)
                        dfs_for_metric.append(processed_df)
                        print(f"Successfully processed {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            if dfs_for_metric:
                metric_dfs[folder_name] = pd.concat(dfs_for_metric, ignore_index=True)
        
        if not metric_dfs:
            return pd.DataFrame()

        # Merge all metric dataframes
        merged_df = reduce(lambda left, right: pd.merge(left, right, on=['lote_composto', 'idade'], how='outer'), metric_dfs.values())
        
        return merged_df

# =============================================================================
# Main Data Manager Class
# =============================================================================

class DataManager:
    """
    Manages the entire data pipeline from raw data to final plots.
    """
    def __init__(self):
        self.project_root = os.path.abspath(os.path.dirname(__file__))
        self.db_path = os.path.join(self.project_root, 'database', 'clima.db')
        self.prod_db_path = os.path.join(self.project_root, 'database', 'clima_prod.db')
        self.raw_iot_dir = os.path.join(self.project_root, 'data', 'raw', 'exportEprodutorIOT')
        self.raw_lotes_dir = os.path.join(self.project_root, 'data', 'raw', 'exportAcompanhamentoLotes')
        self.processed_dir = os.path.join(self.project_root, 'data', 'processed')
        self.sql_dir = os.path.join(self.project_root, 'database', 'sql')
        self.plots_dir = os.path.join(self.project_root, 'plots')
        
    def run_pipeline(self, force_rebuild=False):
        """
        Executes the entire data processing pipeline.
        :param force_rebuild: If True, rebuilds the databases from scratch.
        """
        print("Starting data pipeline...")
        self._populate_main_db(force_rebuild)
        self._execute_sql_scripts()
        self._export_to_prod_csv()
        self._create_prod_db()
        print("Data pipeline finished successfully.")

    def _populate_main_db(self, force_rebuild):
        if force_rebuild and os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Removed existing database: {self.db_path}")

        print("\n--- Populating main database (clima.db) ---")
        conn = sqlite3.connect(self.db_path)
        try:
            # --- Populate eprodutor_iot_data ---
            search_pattern_iot = os.path.join(self.raw_iot_dir, '**', '*.csv')
            is_first_iot = True
            for file_path in glob.glob(search_pattern_iot, recursive=True):
                try:
                    df = pd.read_csv(file_path, sep=';', skiprows=1, decimal=',')
                    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col], errors='ignore')

                    if 'Coletor' in df.columns:
                        df['Coletor'] = df['Coletor'].astype(str).str.extract(r'(\d+)', expand=False).fillna(df['Coletor'])
                    
                    lote_match = re.search(r'lote_(\d+)', file_path)
                    df['Lote'] = lote_match.group(1) if lote_match else None
                    
                    if 'Coletor' in df.columns and 'Lote' in df.columns:
                        df['lote_composto'] = df['Coletor'].astype(str) + '-' + df['Lote'].astype(str)
                    
                    if_exists_iot = 'replace' if is_first_iot else 'append'
                    df.to_sql('eprodutor_iot_data', conn, if_exists=if_exists_iot, index=False)
                    is_first_iot = False
                    print(f"Loaded IoT data from {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"Error processing IoT file {os.path.basename(file_path)}: {e}")

            # --- Populate acompanhamento_lotes_data ---
            print("\nProcessing Acompanhamento de Lotes data...")
            acompanhamento_processor = AcompanhamentoLotesProcessor(self.raw_lotes_dir)
            acompanhamento_df = acompanhamento_processor.process_files()
            if not acompanhamento_df.empty:
                acompanhamento_df.to_sql('acompanhamento_lotes_data', conn, if_exists='replace', index=False)
                print("Successfully loaded Acompanhamento de Lotes data.")

        finally:
            conn.close()

    def _execute_sql_scripts(self):
        print("\n--- Executing SQL scripts ---")
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            sql_files = glob.glob(os.path.join(self.sql_dir, '*.sql'))
            
            # Execute CREATE statements first
            for file_path in sorted(sql_files, key=lambda x: ('create' not in x.lower(), x)):
                 with open(file_path, 'r') as f:
                    sql_script = f.read()
                 try:
                    cursor.executescript(sql_script)
                    print(f"Executed SQL script: {os.path.basename(file_path)}")
                 except sqlite3.Error as e:
                    print(f"Error in script {os.path.basename(file_path)}: {e}")
            conn.commit()
        finally:
            conn.close()

    def _export_to_prod_csv(self):
        print("\n--- Exporting data to production CSVs ---")
        conn = sqlite3.connect(self.db_path)
        try:
            views_to_export = {
                "daily_iot_summary": "daily_iot_summary_prod.csv",
                "lote_performance_summary": "lote_performance_summary_prod.csv",
                "distinct_grandezas": "distinct_grandezas_prod.csv"
            }
            tables_to_export = {
                "acompanhamento_lotes_data": "acompanhamento_lotes_data_prod.csv"
            }
            
            for view, filename in views_to_export.items():
                df = pd.read_sql_query(f"SELECT * FROM {view}", conn)
                df.to_csv(os.path.join(self.processed_dir, filename), index=False)
                print(f"Exported {view} to {filename}")
                
            for table, filename in tables_to_export.items():
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                df.to_csv(os.path.join(self.processed_dir, filename), index=False)
                print(f"Exported {table} to {filename}")

        finally:
            conn.close()

    def _create_prod_db(self):
        print("\n--- Creating production database (clima_prod.db) ---")
        if os.path.exists(self.prod_db_path):
            os.remove(self.prod_db_path)

        conn = sqlite3.connect(self.prod_db_path)
        try:
            prod_csvs = glob.glob(os.path.join(self.processed_dir, '*_prod.csv'))
            for file_path in prod_csvs:
                table_name = os.path.basename(file_path).replace('_prod.csv', '')
                df = pd.read_csv(file_path)
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Loaded {table_name} into production database.")
        finally:
            conn.close()
            
    def _get_available_lots(self):
        """Gets a list of available lot numbers from the production database."""
        conn = sqlite3.connect(self.prod_db_path)
        try:
            df = pd.read_sql_query("SELECT DISTINCT lote_composto FROM daily_iot_summary", conn)
            # Extract lot number from '1282-19' -> '19'
            lots = df['lote_composto'].str.split('-').str[1].unique()
            return sorted(lots)
        finally:
            conn.close()

    def generate_all_plots(self):
        """
        Generates all single-lot and comparison plots for all available lots.
        """
        print("\n--- Generating all plots ---")
        available_lots = self._get_available_lots()
        if not available_lots:
            print("No lots found in the production database to generate plots for.")
            return

        print(f"Found available lots: {available_lots}")

        # Generate single lot plots
        for lot in available_lots:
            self._generate_single_lot_plots(lot)

        # Generate comparison plots for all pairs of lots
        from itertools import combinations
        if len(available_lots) >= 2:
            for lot1, lot2 in combinations(available_lots, 2):
                self._generate_comparison_plots(lot1, lot2)
                
    def _generate_single_lot_plots(self, lot_number):
        print(f"\n--- Generating plots for Lote {lot_number} ---")
        conn = sqlite3.connect(self.prod_db_path)
        try:
            lotes_compostos = [f'1282-{lot_number}', f'1283-{lot_number}']
            grandezas_df = pd.read_sql_query(f"SELECT DISTINCT Grandeza FROM daily_iot_summary WHERE lote_composto IN {tuple(lotes_compostos)}", conn)
            grandezas = grandezas_df['Grandeza'].tolist()

            output_dir = os.path.join(self.plots_dir, f'lote_{lot_number}')
            os.makedirs(output_dir, exist_ok=True)

            for grandeza in grandezas:
                query = f"""
                SELECT idade_lote, lote_composto, average_valor
                FROM daily_iot_summary
                WHERE lote_composto IN {tuple(lotes_compostos)} AND Grandeza = ?
                ORDER BY idade_lote
                """
                df = pd.read_sql_query(query, conn, params=[grandeza])
                if df.empty: continue

                df_agg = df.groupby(['idade_lote', 'lote_composto'])['average_valor'].median().reset_index()
                pivot_df = df_agg.pivot(index='idade_lote', columns='lote_composto', values='average_valor')

                plt.figure(figsize=(12, 6))
                for column in pivot_df.columns:
                    label = f'{column} ' + ('(Novo Equip.)' if '1283' in column else '(Controle)')
                    plt.plot(pivot_df.index, pivot_df[column], label=label)
                
                plt.title(f'Comparativo de {grandeza} (Lote {lot_number})')
                plt.xlabel('Idade da Ave (dias)')
                plt.ylabel(grandeza)
                plt.legend()
                plt.grid(True)
                
                safe_grandeza = re.sub(r'[^a-zA-Z0-9_]', '', grandeza).lower()
                filename = os.path.join(output_dir, f'lote_{lot_number}_comparativo_{safe_grandeza}.png')
                plt.savefig(filename)
                plt.close()
                print(f"Saved plot: {filename}")
        finally:
            conn.close()

    def _generate_comparison_plots(self, lot1, lot2):
        print(f"\n--- Generating comparison plots for Lote {lot1} vs Lote {lot2} ---")
        conn = sqlite3.connect(self.prod_db_path)
        try:
            lotes_compostos = [f'1282-{lot1}', f'1283-{lot1}', f'1282-{lot2}', f'1283-{lot2}']
            grandezas_df = pd.read_sql_query(f"SELECT DISTINCT Grandeza FROM daily_iot_summary WHERE lote_composto IN {tuple(lotes_compostos)}", conn)
            grandezas = grandezas_df['Grandeza'].tolist()

            output_dir = os.path.join(self.plots_dir, 'comparativo_lotes')
            os.makedirs(output_dir, exist_ok=True)

            for grandeza in grandezas:
                query = f"""
                SELECT idade_lote, lote_composto, average_valor
                FROM daily_iot_summary
                WHERE lote_composto IN {tuple(lotes_compostos)} AND Grandeza = ?
                ORDER BY idade_lote
                """
                df = pd.read_sql_query(query, conn, params=[grandeza])
                if df.empty: continue

                df_agg = df.groupby(['idade_lote', 'lote_composto'])['average_valor'].median().reset_index()

                plt.figure(figsize=(14, 7))
                for lote_composto_val, group_df in df_agg.groupby('lote_composto'):
                    label = f'{lote_composto_val} ' + ('(Novo Equip.)' if '1283' in lote_composto_val else '(Controle)')
                    plt.plot(group_df['idade_lote'], group_df['average_valor'], label=label)
                
                plt.title(f'Comparativo de {grandeza} entre Lotes {lot1} e {lot2}')
                plt.xlabel('Idade da Ave (dias)')
                plt.ylabel(grandeza)
                plt.legend()
                plt.grid(True)
                
                safe_grandeza = re.sub(r'[^a-zA-Z0-9_]', '', grandeza).lower()
                filename = os.path.join(output_dir, f'comparativo_lotes_{lot1}_{lot2}_{safe_grandeza}.png')
                plt.savefig(filename)
                plt.close()
                print(f"Saved plot: {filename}")
        finally:
            conn.close()

    def perform_eda(self):
        """
        Performs an Exploratory Data Analysis (EDA) and saves the results to a file.
        """
        print("\n--- Performing Exploratory Data Analysis (EDA) ---")
        conn = sqlite3.connect(self.prod_db_path)
        try:
            available_lots = self._get_available_lots()
            if not available_lots:
                print("No lots found to perform EDA.")
                return

            grandezas_df = pd.read_sql_query("SELECT DISTINCT Grandeza FROM daily_iot_summary", conn)
            grandezas = grandezas_df['Grandeza'].tolist()

            eda_results = "# Análise Descritiva dos Dados (EDA)\n\n"

            for lot in available_lots:
                eda_results += f"## Lote {lot}\n\n"
                lotes_compostos = [f'1282-{lot}', f'1283-{lot}']
                
                for grandeza in grandezas:
                    query = f"""
                    SELECT lote_composto, average_valor
                    FROM daily_iot_summary
                    WHERE lote_composto IN {tuple(lotes_compostos)} AND Grandeza = ?
                    """
                    df = pd.read_sql_query(query, conn, params=[grandeza])
                    if df.empty: continue

                    eda_results += f"### Grandeza: {grandeza}\n\n"
                    for lote_composto_val in df['lote_composto'].unique():
                        stats = df[df['lote_composto'] == lote_composto_val]['average_valor'].describe()
                        eda_results += f"**{lote_composto_val}**:\n\n"
                        eda_results += "```\n"
                        eda_results += stats.to_string()
                        eda_results += "\n```\n\n"
            
            eda_output_path = os.path.join(self.project_root, 'docs', 'analise_descritiva_eda.md')
            with open(eda_output_path, 'w') as f:
                f.write(eda_results)
            print(f"EDA results saved to {eda_output_path}")

        finally:
            conn.close()

    def perform_ab_test(self):
        """
        Performs an A/B test (Mann-Whitney U) for each lot and metric,
        comparing aviaries 1282 (control) and 1283 (experimental).
        Saves the results to a markdown file.
        """
        print("\n--- Performing A/B Test (Mann-Whitney U) ---")
        conn = sqlite3.connect(self.prod_db_path)
        try:
            available_lots = self._get_available_lots()
            if not available_lots:
                print("No lots found to perform A/B test.")
                return

            grandezas_df = pd.read_sql_query("SELECT DISTINCT Grandeza FROM daily_iot_summary", conn)
            grandezas = grandezas_df['Grandeza'].tolist()

            ab_results = "# Análise de Teste A/B (Mann-Whitney U)\n\n"
            ab_results += "Este relatório compara o aviário de controle (1282) com o aviário experimental (1283) para cada lote e grandeza, usando o teste não paramétrico de Mann-Whitney U.\n\n"
            alpha = 0.05

            for lot in available_lots:
                ab_results += f"## Lote {lot}\n\n"
                
                for grandeza in grandezas:
                    ab_results += f"### Grandeza: {grandeza}\n\n"
                    
                    # Fetch data for control (A) and experimental (B) groups
                    query = f"""
                    SELECT lote_composto, average_valor
                    FROM daily_iot_summary
                    WHERE lote_composto IN ('1282-{lot}', '1283-{lot}') AND Grandeza = ?
                    """
                    df = pd.read_sql_query(query, conn, params=[grandeza])
                    
                    group_a = df[df['lote_composto'] == f'1282-{lot}']['average_valor'].dropna()
                    group_b = df[df['lote_composto'] == f'1283-{lot}']['average_valor'].dropna()

                    if len(group_a) < 1 or len(group_b) < 1:
                        ab_results += "Dados insuficientes para realizar o teste.\n\n"
                        continue

                    # Perform Mann-Whitney U test
                    stat, p_value = mannwhitneyu(group_a, group_b, alternative='two-sided')

                    ab_results += f"- **Estatística do teste U:** {stat:.4f}\n"
                    ab_results += f"- **P-valor:** {p_value:.4f}\n"

                    if p_value < alpha:
                        ab_results += "- **Conclusão:** Há uma **diferença estatisticamente significativa** entre os aviários de controle e experimental (p < 0.05).\n"
                    else:
                        ab_results += "- **Conclusão:** Não há evidências de uma diferença estatisticamente significativa entre os aviários (p >= 0.05).\n"
                    
                    ab_results += "\n"

            ab_output_path = os.path.join(self.project_root, 'docs', 'analise_teste_ab.md')
            with open(ab_output_path, 'w') as f:
                f.write(ab_results)
            print(f"A/B test results saved to {ab_output_path}")

        finally:
            conn.close()

    def interpret_results(self):
        """
        Interprets the A/B test results and provides a summary of which aviary is better.
        """
        print("\n--- Interpreting A/B Test Results ---")
        
        conn = sqlite3.connect(self.prod_db_path)
        try:
            available_lots = self._get_available_lots()
            if not available_lots:
                print("No lots found to interpret.")
                return

            grandezas_df = pd.read_sql_query("SELECT DISTINCT Grandeza FROM daily_iot_summary", conn)
            grandezas = grandezas_df['Grandeza'].tolist()

            interpretation_results = "# Análise Comparativa Interpretada\n\n"
            alpha = 0.05

            for lot in available_lots:
                interpretation_results += f"## Lote {lot}\n\n"
                
                for grandeza in grandezas:
                    # Fetch data
                    query = f"""
                    SELECT lote_composto, average_valor
                    FROM daily_iot_summary
                    WHERE lote_composto IN ('1282-{lot}', '1283-{lot}') AND Grandeza = ?
                    """
                    df = pd.read_sql_query(query, conn, params=[grandeza])
                    
                    group_a = df[df['lote_composto'] == f'1282-{lot}']['average_valor'].dropna()
                    group_b = df[df['lote_composto'] == f'1283-{lot}']['average_valor'].dropna()

                    interpretation_results += f"### {grandeza}\n\n"

                    if len(group_a) < 1 or len(group_b) < 1:
                        interpretation_results += "- **Conclusão:** Dados insuficientes para realizar o teste.\n\n"
                        continue

                    # Perform test
                    stat, p_value = mannwhitneyu(group_a, group_b, alternative='two-sided')

                    median_a = group_a.median()
                    median_b = group_b.median()
                    
                    if p_value < alpha:
                        interpretation_results += f"- **Diferença Estatisticamente Significativa:** Sim (p-valor: {p_value:.4f})\n"
                        interpretation_results += f"- **Estatística do teste U:** {stat:.2f}\n"
                        interpretation_results += f"- **Mediana Controle (1282):** {median_a:.2f}\n"
                        interpretation_results += f"- **Mediana Experimental (1283):** {median_b:.2f}\n"
                        if median_a > 0:
                            diff_percent = ((median_b - median_a) / median_a) * 100
                            interpretation_results += f"- **Diferença Percentual:** {diff_percent:.2f}%\n\n"
                        else:
                            interpretation_results += "\n"
                    else:
                        interpretation_results += f"- **Conclusão:** Não há evidências de diferença estatisticamente significativa entre os aviários (p-valor: {p_value:.4f}).\n"
                        interpretation_results += f"  - Mediana Controle (1282): {median_a:.2f}\n"
                        interpretation_results += f"  - Mediana Experimental (1283): {median_b:.2f}\n\n"


            interpretation_output_path = os.path.join(self.project_root, 'docs', 'analise_comparativa_interpretada.md')
            with open(interpretation_output_path, 'w') as f:
                f.write(interpretation_results)
            print(f"Interpretation results saved to {interpretation_output_path}")

        finally:
            conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data Processing and Plotting Pipeline for Aviary Analysis.")
    parser.add_argument('--rebuild-db', action='store_true', help="Force a complete rebuild of the main 'clima.db' from raw data.")
    parser.add_argument('--eda-only', action='store_true', help="Only perform EDA on the existing production database.")
    parser.add_argument('--ab-test-only', action='store_true', help="Only perform A/B testing on the existing production database.")
    parser.add_argument('--interpret-only', action='store_true', help="Only interpret the results on the existing production database.")
    args = parser.parse_args()

    manager = DataManager()
    if args.eda_only:
        manager.perform_eda()
    elif args.ab_test_only:
        manager.perform_ab_test()
    elif args.interpret_only:
        manager.interpret_results()
    else:
        manager.run_pipeline(force_rebuild=args.rebuild_db)
        manager.generate_all_plots()
        manager.perform_eda()
        manager.perform_ab_test()
        manager.interpret_results()
    
    print("\n✅ Done.")
