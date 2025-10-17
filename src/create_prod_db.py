import sqlite3
import pandas as pd
import os
import glob

class ProdDBGenerator:
    def __init__(self, processed_data_directory, output_db_path):
        self.processed_data_directory = processed_data_directory
        self.output_db_path = output_db_path

    def generate_db(self):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.output_db_path), exist_ok=True)

        # Delete existing production database if it exists
        if os.path.exists(self.output_db_path):
            os.remove(self.output_db_path)
            print(f"Deleted existing production database: {self.output_db_path}")

        conn = None
        try:
            conn = sqlite3.connect(self.output_db_path)
            
            search_pattern = os.path.join(self.processed_data_directory, '*_prod.csv')
            
            for file_path in glob.glob(search_pattern):
                try:
                    df = pd.read_csv(file_path)
                    
                    # Extract table name from filename (e.g., daily_iot_summary_prod.csv -> daily_iot_summary)
                    table_name = os.path.basename(file_path).replace('_prod.csv', '')
                    
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"Successfully loaded {file_path} into table {table_name} in {self.output_db_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    processed_data_dir = os.path.join(project_root, 'data', 'processed')
    prod_db_path = os.path.join(project_root, 'database', 'clima_prod.db')

    generator = ProdDBGenerator(processed_data_dir, prod_db_path)
    generator.generate_db()
