# import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# send GET request to Wikipedia page 
website = "https://en.wikipedia.org/wiki/List_of_Friends_episodes"
website_response = requests.get(website)

# parse content
soup = BeautifulSoup(website_response.text, 'html.parser')


## extract headers
first_table = soup.find('table', class_ = "wikitable plainrowheaders wikiepisodetable")
first_table_first_row = first_table.find('tr')
raw_list_headers = first_table_first_row.find_all('th')

clean_list_headers = [header.get_text() for header in raw_list_headers]
clean_list_headers.insert(1,'Season')


## extract rows 
#all tables
raw_tables = soup.find_all('table', class_ = "wikitable plainrowheaders wikiepisodetable")[:-1]

clean_rows = []
season_number = 0
for table in raw_tables: #loop through tables and extract rows
    list_of_rows = table.find_all('tr')[1:]
    season_number += 1
    for row in list_of_rows:
        raw_rows = row.find_all(['th', 'td'])
        rows_text = [x.get_text() for x in raw_rows]
        rows_text.insert(1,season_number)
        if len(rows_text) > 9: #some tables have an additional column 
            clean_rows.append(rows_text[:9])
        else:
            clean_rows.append(rows_text)
       
# assign to dataframe and clean
episdoes_df = pd.DataFrame(clean_rows, columns= clean_list_headers)
episdoes_df.dropna( inplace = True)
episdoes_df.drop(['Prod.code'], axis=1, inplace=True)
episdoes_df['U.S. viewers(millions)'] = episdoes_df['U.S. viewers(millions)'].str.replace(r'\[.*?\]', '', regex=True)
episdoes_df['Original release date'] = episdoes_df['Original release date'].str.extract(r'\((\d{4}-\d{2}-\d{2})\)')

#save to excel
episdoes_df.to_excel('friends_episodes.xlsx', index=False)


