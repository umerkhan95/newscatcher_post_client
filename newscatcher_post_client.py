import pandas as pd
from newscatcherapi import NewsCatcherApiClient
from datetime import datetime, timedelta
import requests

url = "path to your datastore"  # Directus API endpoint for the "test" collection
token = "path to your token"  # Replace with your bearer token

# Initialize the NewsCatcherApiClient object
client = NewsCatcherApiClient(x_api_key='give your api key here')

# Define the date range for the search
start_date = datetime.strptime('2023-04-12', '%Y-%m-%d')
end_date = datetime.strptime('2023-05-11', '%Y-%m-%d')

# Define the number of days for each iteration
delta = timedelta(days=7)

# Initialize an empty DataFrame to hold the extracted data
all_articles_df = pd.DataFrame(columns=['title', 'language', 'author', 'published_date', 'link', 'excerpt', 'country', 'authors', 'metadata', 'summary', 'rights'])

# Loop over the date range with 7-day intervals
while start_date <= end_date:
    # Define the start and end dates for the current iteration
    from_date = start_date.strftime('%Y/%m/%d')
    to_date = (start_date + delta).strftime('%Y/%m/%d')

    # Retrieve the news articles using the NewsCatcherApiClient
    articles = client.get_search_all_articles(q='*',
                                               lang='de',
                                               countries=['DE','AT', 'CH'],
                                               from_=from_date,
                                               to_=to_date,
                                               page_size=100,
                                               ranked_only=False)

    # Convert the articles data to a pandas DataFrame
    articles_df = pd.DataFrame(articles['articles'])
    articles_df['Twitter Account Name'] = articles_df['Twitter Account Name'].str.replace('@', '')
    articles_df['Twitter Account Name'] = articles_df['Twitter Account Name'].str.replace('\n', '')
    
    for index, row in articles_df.iterrows():
        # Access row data using row[column_name]
        title = row['title']
        language = row['language']
        author = row['author']
        published_date = row['published_date']
        link = row["link"]
        excerpt = row["excerpt"]
        country = row["country"]
        authors = row["authors"]
        metadata = row["metadata"]
        summary = row["summary"]
        
        data = {
            "title": title,
            "language": language,
            "author": author,
            "published_date": published_date,
            "link": link,
            "excerpt": excerpt,
            "country": country,
            "authors": authors,
            "metadata": metadata,
            "summary": summary
        }

        def post_data(data):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print("Data posted successfully.")
            else:
                print("Error:", response.text)
        
        # Use multiprocessing to post data in parallel
        with Pool(processes=44) as pool:  # Adjust the number of processes as per your system's capabilities
            pool.map(post_data, rows_data)
    
    start_date += delta
