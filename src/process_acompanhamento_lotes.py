import pandas as pd
import glob
import os
import re

class AcompanhamentoLotesProcessor:
    def __init__(self, csv_directory):
        self.csv_directory = csv_directory
        self.column_mappings = {
            "ConsumoEnergia": {
                "Referência (kwh)": "Referencia_kwh",
                "Consumo automático (kwh)": "Consumo_automatico_kwh",
                "Relação": "Relacao_auto",
                "Consumo manual (kwh)": "Consumo_manual_kwh",
                "Relação.1": "Relacao_manual"
            },
            "Mortalidade": {
                "Mortalidade (un)": "Mortalidade_un",
                "Mortalidade (%)": "Mortalidade_percent",
                "Referência (%)": "Referencia_percent",
                "Relação": "Relacao_mortalidade"
            },
            "ConsumoRacao": {
                "Referência (kg)": "Referencia_kg", # Assuming kg for Racao
                "Ração automática (kg)": "Consumo_automatico_kg",
                "Relação": "Relacao_auto",
                "Ração manual (kg)": "Consumo_manual_kg",
                "Relação.1": "Relacao_manual"
            },
            "GMD": {
                "Referência (g)": "Referencia_gmd", # Assumido pelo GMD
                "GMD automático (g)": "GMD_automatico_g",
                "Relação": "Relacao_auto",
                "GMD manual (g)": "GMD_manual_g",
                "Relação.1": "Relacao_manual"

            }
        }
        # Define all possible columns for the final DataFrame to ensure consistency
        self.all_target_columns = [
            'lote_composto', 'Grandeza', 'Idade', 'Data',
            'Referencia_kwh', 'Consumo_automatico_kwh', 'Relacao_auto',
            'Consumo_manual_kwh', 'Relacao_manual',
            'Mortalidade_un', 'Mortalidade_percent', 'Referencia_percent', 'Relacao_mortalidade',
            'Referencia_kg', 'Consumo_automatico_kg', 'Consumo_manual_kg', 'GMD_automatico_g', 'GMD_manual_g'
        ]


    def _process_single_file(self, file_path):
        """
        Processes a single CSV file from exportAcompanhamentoLotes.
        Extracts lote_composto and Grandeza, renames columns.
        """
        try:
            df = pd.read_csv(file_path)

            # Extract lote_composto from filename (e.g., export_consumo_energia_1282_19.csv -> 1282_19)
            filename = os.path.basename(file_path)
            lote_composto_match = re.search(r'_(\d+)_(\d+)\.csv$', filename)
            if lote_composto_match:
                aviario = lote_composto_match.group(1)
                lote = lote_composto_match.group(2)
                df['lote_composto'] = f"{aviario}_{lote}"
            else:
                df['lote_composto'] = None
                print(f"Warning: Could not extract lote_composto from filename: {filename}")

            # Extract Grandeza from subdirectory name (e.g., ConsumoEnergia)
            grandeza = os.path.basename(os.path.dirname(file_path))
            df['Grandeza'] = grandeza

            # Apply specific column renames based on Grandeza
            if grandeza in self.column_mappings:
                df = df.rename(columns=self.column_mappings[grandeza])
            
            # Ensure all target columns exist, fill missing with None/NaN
            for col in self.all_target_columns:
                if col not in df.columns:
                    df[col] = None
            
            # Select and reorder columns to match the database schema
            df = df[self.all_target_columns]

            print(f"Successfully processed {file_path}")
            return df
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return pd.DataFrame() # Return empty DataFrame on error

    def process_files(self):
        """
        Finds all CSV files in the specified directory and its subdirectories
        and applies the processing logic to them, returning a concatenated DataFrame.
        """
        all_processed_data = []
        search_pattern = os.path.join(self.csv_directory, '**', '*.csv')
        
        for file_path in glob.glob(search_pattern, recursive=True):
            processed_df = self._process_single_file(file_path)
            if not processed_df.empty:
                all_processed_data.append(processed_df)
        
        if all_processed_data:
            return pd.concat(all_processed_data, ignore_index=True)
        return pd.DataFrame()

if __name__ == "__main__":
    # Example usage if run directly (for testing)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    csv_dir = os.path.join(project_root, 'data', 'raw', 'exportAcompanhamentoLotes')
    
    processor = AcompanhamentoLotesProcessor(csv_dir)
    combined_df = processor.process_files()
    if not combined_df.empty:
        print("\nCombined Processed Data Head:")
        print(combined_df.head())
        print("\nCombined Processed Data Info:")
        combined_df.info()
