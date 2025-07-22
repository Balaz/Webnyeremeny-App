import pandas as pd

def get_reference_stores() -> pd.DataFrame:
    """
    Reads the reference stores from a CSV file and returns a DataFrame.
    """
    try:
        stores_reference = pd.read_csv('hungarian_stores.csv')
    except FileNotFoundError:
        raise FileNotFoundError("hungarian_stores.csv file not found!")
    
    return stores_reference

def get_all_stores(contests_df: pd.DataFrame ) -> pd.DataFrame:
    """    
    Collect stores from the contests DataFrame and match them with store URLs.
    Returns a DataFrame with store names and their corresponding URLs.
    """
    store_contests_df = contests_df[contests_df["title"] == "Üzletekhez kötődő"]
    
    stores_reference = get_reference_stores()                               
    stores_reference = stores_reference['stores'].str.strip().str.lower()     # Clean and process stores_reference

    # Clean and process the games column
    stores_df = store_contests_df['games'].str.replace("-", ",").str.split(',').to_frame(name='games')
    stores_df = stores_df['games'].explode()        # Remove the list parameter
    stores_df = stores_df.str.strip().str.lower()   # Clean whitespace and normalize case
    stores_df = stores_df.to_frame(name='games')

    # Keep only the relevant stores from the reference
    filtered_df = pd.merge(stores_df, stores_reference, left_on='games', right_on='stores', how='inner').drop('games', axis=1)
    
    # Remove duplicates and reset index
    filtered_df = filtered_df.drop_duplicates(subset=['stores']).reset_index(drop=True)

    return filtered_df

    # Add the all URLs next to the stores