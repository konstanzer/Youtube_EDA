import pandas as pd
import json

class VideoDataLoader:
    def __init__(self):
        self.country_codes = ["US", "CA", "DE", "FR", "GB", "IN", "KR", "MX", "RU"]
        self.root_path = "data/"
        self.category_dict = self.categories_dict()
    
    def load_data(self):
        '''
        Load YouTube data into a dictionary of pandas dataframes, one for each country.
        '''
        data = {}
        for country in self.country_codes:
            PATH = f"{self.root_path}{country}videos.csv"
            df = pd.read_csv(PATH)
            data[country] = df
            
            #add new columns
            df['category'] = df['category_id'].map(self.category_dict)
            df['coms_views_ratio'] = df['comment_count'] / df['views']
            df['like_ratio'] = df['likes'] /  (df['likes'] + df['dislikes'])
            
        self.data = data

    def categories_dict(self):
        '''
        Load category name and ID into a dictionary for each country.
        '''
        data = {}
        for country in self.country_codes:
            PATH = f"{self.root_path}{country}_category_id.json"
            with open(PATH, "r") as f:
                cat_data = json.load(f)
                for item in cat_data["items"]: #first nested dictionary in JSON file
                    data[int(item["id"])] = item["snippet"]["title"] #second nested dictionary "snippet" contains the title
            
        return data
   