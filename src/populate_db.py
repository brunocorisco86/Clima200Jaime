import pandas as pd
import sqlite3
import glob
import os
import re
from src.process_acompanhamento_lotes import AcompanhamentoLotesProcessor # New import

class DBPopulator:
    def __init__(self, db_path, csv_directory):
        self.db_path = db_path
        self.csv_directory = csv_directory
        self.acompanhamento_lotes_csv_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'exportAcompanhamentoLotes'))


    def populate(self):
        """
        Populates an SQLite database with data from processed CSV files.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # --- Populate eprodutor_iot_data table --- (Existing logic)
            search_pattern_iot = os.path.join(self.csv_directory, '**', '*.csv')
            
            table_created_iot = False
            table_name_iot = 'eprodutor_iot_data'

            for file_path in glob.glob(search_pattern_iot, recursive=True):
                try:
                    df = pd.read_csv(file_path, sep=';', skiprows=1, decimal=',')

                    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
                    if unnamed_cols:
                        df = df.drop(columns=unnamed_cols)

                    if 'Coletor' in df.columns:
                        df['Coletor'] = df['Coletor'].astype(str).str.extract(r'(\d+)', expand=False).fillna(df['Coletor'])
                    
                    lote_match = re.search(r'lote_(\d+)', file_path)
                    if lote_match:
                        lote_number = lote_match.group(1)
                        df['Lote'] = lote_number
                    else:
                        df['Lote'] = None
                    
                    if 'Coletor' in df.columns and 'Lote' in df.columns:
                        # Changed from underscore to hyphen for consistency with lote_composto table
                        df['lote_composto'] = df['Coletor'].astype(str) + '-' + df['Lote'].astype(str)
                    
                    if not table_created_iot:
                        df.to_sql(table_name_iot, conn, if_exists='replace', index=False)
                        table_created_iot = True
                    else:
                        df.to_sql(table_name_iot, conn, if_exists='append', index=False)
                    
                    print(f"Successfully loaded data from {file_path} into {table_name_iot}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

            # --- Populate acompanhamento_lotes_data table --- (New logic)
            print("\nPopulating acompanhamento_lotes_data table...")
            acompanhamento_processor = AcompanhamentoLotesProcessor(self.acompanhamento_lotes_csv_directory)
            acompanhamento_df = acompanhamento_processor.process_files()

            if not acompanhamento_df.empty:
                table_name_acompanhamento = 'acompanhamento_lotes_data'
                acompanhamento_df.to_sql(table_name_acompanhamento, conn, if_exists='append', index=False)
                print(f"Successfully loaded data into {table_name_acompanhamento}")
            else:
                print("No data processed for acompanhamento_lotes_data.")


        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    # Example usage if run directly (for testing)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    db_path = os.path.join(project_root, 'database', 'clima.db')
    csv_dir = os.path.join(project_root, 'data', 'raw', 'exportEprodutorIOT')
    
    # Ensure the database is clean for testing
    if os.path.exists(db_path):
        os.remove(db_path)

    populator = DBPopulator(db_path, csv_dir)
    populator.populate()