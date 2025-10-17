import pandas as pd
import glob
import os
import re

class CSVProcessor:
    def __init__(self, csv_directory):
        self.csv_directory = csv_directory

    def _process_single_file(self, file_path):
        """
        Processes a single CSV file to:
        1. Edit the 'Coletor' column, extracting the number from the string.
        2. Add a new 'Lote' column, extracting the lot number from the file path.
        3. Create a 'lote_composto' column by concatenating 'Coletor' and 'Lote'.
        """
        try:
            df = pd.read_csv(file_path, sep=';', skiprows=1, decimal=',')

            unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
            if unnamed_cols:
                df = df.drop(columns=unnamed_cols)

            if 'Coletor' in df.columns:
                df['Coletor'] = df['Coletor'].astype(str).str.extract(r'(\d+)', expand=False).fillna(df['Coletor'])
            else:
                print(f"Warning: 'Coletor' column not found in {file_path}")

            lote_match = re.search(r'lote_(\d+)', file_path)
            if lote_match:
                lote_number = lote_match.group(1)
                df['Lote'] = lote_number
            else:
                df['Lote'] = None
                print(f"Warning: Could not extract 'Lote' from file path: {file_path}")

            if 'Coletor' in df.columns and 'Lote' in df.columns:
                df['lote_composto'] = df['Coletor'].astype(str) + '_' + df['Lote'].astype(str)
            else:
                print(f"Warning: Could not create 'lote_composto' in {file_path} due to missing 'Coletor' or 'Lote' column.")

            with open(file_path, 'w') as f:
                    f.write('sep=;\n')
                    df.to_csv(f, index=False, sep=';', decimal=',')

            print(f"Successfully processed {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def process_files(self):
        """
        Finds all CSV files in the specified directory and its subdirectories
        and applies the processing logic to them.
        """
        search_pattern = os.path.join(self.csv_directory, '**', '*.csv')
        
        for file_path in glob.glob(search_pattern, recursive=True):
            self._process_single_file(file_path)

if __name__ == "__main__":
    # Example usage if run directly (for testing)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    csv_dir = os.path.join(project_root, 'data', 'raw', 'exportEprodutorIOT')
    processor = CSVProcessor(csv_dir)
    processor.process_files()