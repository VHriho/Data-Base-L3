import pandas as pd
from typing import List, Dict, Any

class CSVDataReader:
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path, delimiter=',')
            return df.to_dict(orient='records')
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found. Ensure it's next to 'main.py' or the path is correct.")
            return []
        except pd.errors.EmptyDataError:
            print(f"Error: File '{file_path}' is empty.")
            return []
        except pd.errors.ParserError as e:
            print(f"CSV parsing error. Check file format and delimiter. Details: {e}")
            return []
        except Exception as e:
            print(f"Unknown error while reading CSV file: {e}")
            return []