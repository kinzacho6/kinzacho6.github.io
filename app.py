import pandas as pd
import streamlit as st
import altair as alt
import requests

st.title("The Evolution of Electric Vehicles in Washington State")
st.text("By: Kinza Chouhdry & Esbeida Garcia")

st.subheader("Introduction")
st.text("""
Electric vehicles (EVs) play a critical role in the transition toward sustainable and energy-efficient transportation. Washington State, recognized for its commitment to clean energy policies, has experienced significant growth in EV adoption in recent years. This project examines key trends, performance metrics, and the regional distribution of EVs within the state, providing a detailed analysis of how electric vehicles are contributing to advancements in transportation and environmental sustainability.
The analysis utilizes a series of interactive and contextual visualizations to present insights into the growth of EV adoption over time, the performance and range capabilities of different manufacturers, and the geographic distribution of EV registrations at both state and county levels. As an attempt to earn extra credit, the Electric Vehicle Distribution by County visualization was created to offer a deeper understanding of how EVs are adopted across various regions. All other visualizations, including line charts, bar charts, and histograms, were generated using Python and advanced data visualization libraries. The only exception is the map of EV charging stations, which was sourced externally to enhance the overall analysis. This project provides a comprehensive perspective on Washington State’s electric vehicle landscape, supporting policymakers, researchers, and stakeholders in understanding the evolving dynamics of EV adoption.
""")
        
st.subheader("Electric Vehicle Population Dataset")
st.markdown("[Access to the full dataset can be obtained here](https://catalog.data.gov/dataset/electric-vehicle-population-data)")
data = pd.read_csv("Electric_Vehicle_Population_Data.csv")
data

# Interactive Visualization 1: Electric Vehicle Trends Over Time
st.subheader("Electric Vehicle Trends")
st.text("""
The first visualization explores the growth of electric vehicles over the years, and it allows users to select the manufacturer and the vehicle type to explore trends and ranges for various electric vehicles. The line chart clearly illustrates the growth trajectory, providing a valuable overview of EV adoption in the state over the years. Additionally, the second visualization provides an interactive overview of the electric range distribution. This histogram allows users to explore how the electric range varies across different vehicle types. Together, both of these visualizations offer a comprehensive understanding of the growth and performance of electric vehicles in Washington State. By examining both adoption trends over time and the distribution of electric ranges, users can gain insights into how different vehicle types have evolved in terms of popularity and technological advancements. These visualizations provide a holistic view of the state's electric vehicle landscape, helping to inform decisions regarding infrastructure development, policy planning, and consumer preferences.
""" )
st.markdown("Explores the growth of electric vehicles over the years.")

selected_make = st.selectbox("Select Manufacturer", options=["All"] + list(data['Make'].unique()), index=0)
selected_type = st.selectbox("Select Vehicle Type", options=["All"] + list(data['Electric Vehicle Type'].unique()), index=0)

filtered_data = data
if selected_make != "All":
    filtered_data = filtered_data[filtered_data['Make'] == selected_make]
if selected_type != "All":
    filtered_data = filtered_data[filtered_data['Electric Vehicle Type'] == selected_type]

ev_count_by_year = filtered_data.groupby('Model Year').size().reset_index(name='Count')
line_chart = alt.Chart(ev_count_by_year).mark_line(point=True).encode(
    x='Model Year:N',
    y='Count:Q',
    tooltip=['Model Year', 'Count']
).properties(
    title=f"Growth of Electric Vehicles Over Time ({selected_make} - {selected_type})",
    width=700,
    height=400
)

st.altair_chart(line_chart, use_container_width=True)

# Interactive Visualization: Electric Range Distribution
st.subheader("Electric Range Distribution")
st.markdown("Analyzes the distribution of electric ranges for all vehicles or specific types.")

range_filtered_data = data
if selected_type != "All":
    range_filtered_data = range_filtered_data[range_filtered_data['Electric Vehicle Type'] == selected_type]

range_histogram = alt.Chart(range_filtered_data).mark_bar().encode(
    x=alt.X('Electric Range:Q', bin=alt.Bin(maxbins=20), title="Electric Range (miles)"),
    y=alt.Y('count()', title="Number of Vehicles"),
    tooltip=['Electric Range', 'count()'],
    color=alt.Color('Electric Vehicle Type:N', title="Vehicle Type")
).properties(
    title="Distribution of Electric Range by Vehicle Type",
    width=700,
    height=400
)

st.altair_chart(range_histogram, use_container_width=True)

st.subheader("Contextual Visualizations")
st.text(""" 
The third and fourth visualizations dive into more contextual details, such as the distribution of electric vehicles across counties in Washington State and the average electric range by manufacturer. The county distribution visualization groups counties based on the number of vehicles and uses a color-coded bar chart to show adoption rates, helping users understand regional trends in EV adoption. The average electric range by manufacturer chart highlights the leading manufacturers in terms of range, allowing users to compare the performance of top electric vehicle brands. These visualizations, paired with a map of EV charging stations in the state, provide a comprehensive view of the electric vehicle landscape in Washington, offering insights into both adoption patterns and vehicle performance.
""")
#Contextual Visualization: EV Distribution by County
st.subheader("Electric Vehicle Distribution by County")
st.markdown("""
Explores the distribution of electric vehicles across Washington State counties.
""")

bins = [0, 50, 200, 500, 1000, data['County'].value_counts().max()]
labels = ["0-50", "51-200", "201-500", "501-1000", "1000+"]
data['Adoption Range'] = pd.cut(data['County'].map(data['County'].value_counts()), bins=bins, labels=labels, include_lowest=True)
selected_range = st.selectbox("Select an EV adoption range:", options=["All"] + labels)

filtered_county_data = data if selected_range == "All" else data[data['Adoption Range'] == selected_range]

county_counts = filtered_county_data['County'].value_counts().reset_index()
county_counts.columns = ['County', 'Count']

county_bar_chart = alt.Chart(county_counts).mark_bar().encode(
    x=alt.X('Count:Q', title='Number of Vehicles'),
    y=alt.Y('County:N', title='County', sort='-x'),
    tooltip=['County', 'Count'],
    color=alt.Color('Count:Q', scale=alt.Scale(scheme='bluegreen', domain=[0, county_counts['Count'].max()])),
).properties(
    title="Electric Vehicle Distribution Across Counties",
    width=800,
    height=500
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

st.altair_chart(county_bar_chart, use_container_width=True)

# Contextual Visualization: Average Electric Range by Manufacturer
st.subheader("Average Electric Range by Manufacturer")
st.markdown("Explores which manufacturers offer the highest average electric ranges for their vehicles.")

avg_range_by_make = data.groupby('Make')['Electric Range'].mean().reset_index().sort_values('Electric Range', ascending=False).head(10)
avg_range_chart = alt.Chart(avg_range_by_make).mark_bar().encode(
    x=alt.X('Electric Range:Q', title='Average Electric Range (miles)'),
    y=alt.Y('Make:N', title='Manufacturer', sort='-x'),
    tooltip=['Make', 'Electric Range'],
    color=alt.Color('Electric Range:Q', scale=alt.Scale(scheme='plasma'))
).properties(
    title="Top 10 Manufacturers by Average Electric Range",
    width=700,
    height=400
)

st.altair_chart(avg_range_chart, use_container_width=True)

# Adding an Image
st.subheader("Map of Electric Vehicle Charging Stations in Washington")
st.image(
    "https://cdn.prod.website-files.com/60ce1b7dd21cd5b42639ff42/64f8a7813a231fe32c6b7043_Screenshot%202023-09-06%20at%2012.22.36%20PM.webp",
    caption="https://www.recurrentauto.com/research/washington-electric-vehicles",
    use_container_width=True
)
