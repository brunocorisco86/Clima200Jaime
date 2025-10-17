import sqlite3
import pandas as pd
import os

class DataExporter:
    def __init__(self, db_path, output_directory):
        self.db_path = db_path
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def export_view_to_csv(self, view_name, output_filename):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"SELECT * FROM {view_name};"
            df = pd.read_sql_query(query, conn)
            
            output_path = os.path.join(self.output_directory, output_filename)
            df.to_csv(output_path, index=False)
            print(f"Successfully exported {view_name} to {output_path}")
        except sqlite3.Error as e:
            print(f"Error exporting {view_name}: {e}")
        finally:
            if conn:
                conn.close()

    def export_table_to_csv(self, table_name, output_filename):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"SELECT * FROM {table_name};"
            df = pd.read_sql_query(query, conn)
            
            output_path = os.path.join(self.output_directory, output_filename)
            df.to_csv(output_path, index=False)
            print(f"Successfully exported {table_name} to {output_path}")
        except sqlite3.Error as e:
            print(f"Error exporting {table_name}: {e}")
        finally:
            if conn:
                conn.close()

    def export_all_summarized_data(self):
        # This method exports all summarized views and tables
        self.export_view_to_csv("daily_iot_summary", "daily_iot_summary.csv")
        self.export_view_to_csv("lote_performance_summary", "lote_performance_summary.csv")
        self.export_view_to_csv("distinct_grandezas", "distinct_grandezas.csv")
        self.export_table_to_csv("acompanhamento_lotes_data", "acompanhamento_lotes_data.csv")

    def export_production_data(self):
        # This method exports a lighter set of data for production, excluding raw IoT data
        self.export_view_to_csv("daily_iot_summary", "daily_iot_summary_prod.csv")
        self.export_view_to_csv("lote_performance_summary", "lote_performance_summary_prod.csv")
        self.export_view_to_csv("distinct_grandezas", "distinct_grandezas_prod.csv")
        self.export_table_to_csv("acompanhamento_lotes_data", "acompanhamento_lotes_data_prod.csv")


if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(project_root, 'database', 'clima.db')
    output_dir = os.path.join(project_root, 'data', 'processed')

    exporter = DataExporter(db_path, output_dir)
    exporter.export_all_summarized_data()
    # exporter.export_production_data() # Example of how to call the new function