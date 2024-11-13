import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st

# import dataset
def load_data():
    file = 'aircrahesFullDataUpdated_2024.csv'
    df = pd.read_csv(file)
    df['Country/Region'] = df['Country/Region'].str.strip().str.title()
    # Aircraft Manufacturer
    df['Aircraft Manufacturer'] = df['Aircraft Manufacturer'].str.strip().str.title()
    # Aircraft
    df['Aircraft'] = df['Aircraft'].str.strip()
    # location
    df['Location'] = df['Location'].str.strip()
    # Operator
    df['Operator'] = df['Operator'].str.strip()
    # check for duplicate
    duplicate_count = df.duplicated().sum()
    print(duplicate_count)
    #merging year day and month
    df['Date'] = df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-' + df['Day'].astype(str)
    return df

# load the dataset 
df = load_data()

# app title
st.title("ATOLANI PYTHON PROJECT:AIRCRASHES ANALYSIS")

# Calculate the total number of accidents
total_accidents = len(df)

# Calculate the total number of fatalities
total_fatalities = df['Fatalities (air)'].sum()

# Calculate the total number of survivors
total_survivors = df['Aboard'].sum() - total_fatalities

# Calculate the survival rate
survival_rate = (total_survivors / total_accidents) * 100
print(f'Survival rate: {survival_rate:.1f}%')


Q1_fatalities = df['Fatalities (air)'].quantile(0.25)
Q3_fatalities = df['Fatalities (air)'].quantile(0.75)
IQR_fatalities = Q3_fatalities - Q1_fatalities

col1, col2, col3, col4 = st.columns(4)

col1.metric("Survival rate", survival_rate)
col2.metric("Total number of survivors", total_survivors)
col3.metric("Total number of fatalities", total_fatalities)
col4.metric("Total number of accidents",total_accidents)

st.write(df)

# Charts and graphs
# Scatter plot of Fatalities vs. Aboard
st.subheader("Fatalities vs. Aboard")
fig, ax = plt.subplots()
sns.scatterplot(x=df['Aboard'], y=df['Fatalities (air)'], ax=ax)
ax.set_title('Fatalities vs. Aboard')
ax.set_xlabel('Number of People Aboard')
ax.set_ylabel('Number of Fatalities')
st.pyplot(fig)

# aircraft fatality
aircraft_fatality = df.groupby('Aircraft')['Fatalities (air)'].sum().reset_index()
top_aircraft = aircraft_fatality.head(20)
print(top_aircraft)
st.subheader("Crashes by Aircraft")
fig, ax = plt.subplots()
top_aircraft.plot(kind='bar', ax=ax, color='green')
ax.set_title('Crashes by Country/Region (Top 10)')
ax.set_xlabel('Country/Region')
ax.set_ylabel('Number of Crashes')
st.pyplot(fig)

# Year fatality
try:
    st.write("## Crashes by Year ")
    Year_fatality = df.groupby('Year')['Fatalities (air)'].sum().reset_index()
    # plot
    st.subheader("Crashes by Year")
    fig, ax = plt.subplots()
    Year_fatality.plot(kind='line', ax=ax)
    ax.set_title('Number of Crashes by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Crashes')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )

# Fatalities by Country/Region - Line plot
try:
    country_fatality = df.groupby('Country/Region')['Fatalities (air)'].sum().reset_index()
    top_countries = country_fatality.head(20)
    print(top_countries)
    st.subheader("Country/Region Fatality")
    fig, ax = plt.subplots()
    top_countries.plot(kind='line', ax=ax, color='red')
    ax.set_title('Fatalities by Country/Region')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Fatalities')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )

## location fatality - Bar plot
try:
    location_fatality = df.groupby('Location')['Fatalities (air)'].sum().reset_index()
    top_location = location_fatality.head(20)
    print(top_location)
    st.subheader("location fatality")
    fig, ax = plt.subplots()
    top_location.plot(kind='bar', ax=ax)
    ax.set_title('Location Fatalities (Top 20)')
    ax.set_xlabel('Manufacturer')
    ax.set_ylabel('Number of Fatalities')
    st.pyplot(fig)
except ValueError as e:
    st.error(
       """ Error: """ % e.reason
    )