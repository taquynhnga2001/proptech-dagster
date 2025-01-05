import requests
import pandas as pd

def fetch_all_rows_from_api(dataset_id):
    url = "https://data.gov.sg/api/action/datastore_search"
    limit = 10000  # Adjust based on the API's max limit
    offset = 0   # Start with the first batch
    all_data = []
    
    while True:
        params = {
            "resource_id": dataset_id,
            "limit": limit,
            "offset": offset,
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        records = response.json()['result']['records']
        if not records:  # If no records are returned, stop the loop
            print(f"API Loaded {len(all_data)} rows >>> Done!!")
            break
        
        print(f"API Loaded {offset:,} rows")
        
        all_data.extend(records)
        offset += limit
    
    return pd.DataFrame(all_data)