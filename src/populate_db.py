import pandas as pd
import sqlite3
import glob
import os
import re

class DBPopulator:
    def __init__(self, db_path, csv_directory):
        self.db_path = db_path
        self.csv_directory = csv_directory

    def populate(self):
        """
        Populates an SQLite database with data from processed CSV files.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            search_pattern = os.path.join(self.csv_directory, '**', '*.csv')
            
            table_created = False
            table_name = 'eprodutor_iot_data'

            for file_path in glob.glob(search_pattern, recursive=True):
                try:
                    # Read the CSV file with appropriate parameters (already processed by CSVProcessor)
                    df = pd.read_csv(file_path, sep=';', skiprows=1, decimal=',')

                    # Ensure 'lote_composto' column exists before inserting
                    if 'lote_composto' not in df.columns:
                        print(f"Warning: 'lote_composto' column not found in {file_path}. Skipping insertion.")
                        continue

                    if not table_created:
                        df.to_sql(table_name, conn, if_exists='replace', index=False)
                        table_created = True
                    else:
                        df.to_sql(table_name, conn, if_exists='append', index=False)
                    
                    print(f"Successfully loaded data from {file_path} into {table_name}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

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