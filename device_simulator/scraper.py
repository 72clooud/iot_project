import pandas as pd
import requests
import io

class DataFetch:
    def __init__(self):    
        self.df = None
        self.url = "https://pl.wikipedia.org/wiki/Dane_statystyczne_o_miastach_w_Polsce"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }


    def get_table(self) -> pd.DataFrame:

        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        self.df = pd.read_html(io.StringIO(response.text))
        self.df = self.df[0]

    def normalize_data(self) -> pd.DataFrame:
        col_miasto = next((c for c in self.df.columns if 'miasto' in c.lower() or 'nazwa' in c.lower()), None)
        col_ludnosc = next((c for c in self.df.columns if 'ludno' in c.lower() or 'populacja' in c.lower()), None)

        if not col_miasto or not col_ludnosc:
            raise ValueError(f"Erorr: {self.df.columns.tolist()}")

        self.df = self.df[[col_miasto, col_ludnosc]].copy()
        self.df.columns = ['City', 'Population']

        self.df['Population'] = (
            self.df['Population']
            .astype(str)
            .str.replace(r'\D', '', regex=True)
        )

        self.df['Population'] = pd.to_numeric(self.df['Population'], errors='coerce').astype(int)

        self.df.sort_values(by='Population', ascending=False, inplace=True, ignore_index=True)
    
    def get_data(self) -> pd.DataFrame:
        self.get_table()
        self.normalize_data()

    def save_to_parquet(self, file_path: str) -> None:
        if self.df is not None:
            self.df.to_parquet(file_path, index=False)
        
if __name__ == "__main__":

    data_fetcher = DataFetch()
    data_fetcher.get_data()
    data_fetcher.save_to_parquet("../data/polish_cities.parquet")
