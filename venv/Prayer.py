
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
import os
st.set_page_config(page_title="Prayer Times", page_icon=":mosque:", layout="centered")

# Add a banner image
st.image("https://png.pngtree.com/png-vector/20190521/ourmid/pngtree-mosque-icon-for-personal-and-commercial-use-png-image_1044910.jpg", width=100)

# Create a title and subtitle
st.title("Morocco Prayers Times")
st.subheader("Select a city to view the prayer times")

# List of names
names = ["casablanca", "rabat", "marrakech", "tanger","tetouan","fes","agadir","meknes","dakhla","oujda","nador"]

# Create a dropdown menu to select a city
city = st.selectbox("Select a city", names)

# Create a function to scrape the data
@st.cache
def scrape_data(city):
    # Create the URL with the current name
    url = f'https://lematin.ma/horaire-priere-{city}.html#'

    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

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
    return df

# Show the dataframe when the user selects a city
if st.button("Display the prayer times"):
    if city:
        df = scrape_data(city)
        st.dataframe(df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#f7f7f9'), ('color', '#4d4d4d'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('background-color', '#f7f7f9'), ('color', '#4        d4d4d')]},
            {'selector': 'tr:nth-of-type(even)', 'props': [('background-color', '#f2f2f2')]},
        ]))
    else:
        st.warning("Please select a city")

# Add a prayer times guide
if st.checkbox("Show Prayer Times Guide"):
    st.subheader("Prayer Times Guide")
    st.markdown(
        """
        - **Fajr**: Dawn prayer, before sunrise
        - **Dhuhr**: Midday prayer, after the sun passes its zenith
        - **Asr**: Mid-afternoon prayer, between the decline of the sun and sunset
        - **Maghrib**: Sunset prayer, after sunset
        - **Isha**: Night prayer, after twilight
        """
    )


# Add a support message
st.success("May Allah guide us in our prayers.")
st.success("Thank you for your time ! I will try to improve this app")

