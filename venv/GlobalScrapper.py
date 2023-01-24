import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# List of names
names = ["casablanca", "rabat", "marrakech", "tanger", "tetouan", "fes", "agadir", "meknes", "dakhla", "oujda", "nador"]

# Loop through the list of names
for name in names:
    # Create the URL with the current name
    url = f'https://lematin.ma/horaire-priere-{name}.html#'

    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the header text
    header_text = soup.find('h3').text

    # Find the table in the HTML
    table = soup.find("table", class_="table table-striped")

    # Extract the headers of the table
    headers = [th.text for th in table.find("tr").find_all("th")]

    # Extract the data from the table
    data = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    # Create a dataframe
    df = pd.DataFrame(data, columns=headers)

    # Remove the first column
    df = df.drop(columns=['Header'])

    # create the folder if not exist
    if not os.path.exists("./data"):
        os.makedirs("./data")

    # Save the dataframe to a CSV file
    df.to_csv("./data/{}_prayer_times.csv".format(name), index=False)
