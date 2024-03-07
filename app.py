import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

vehicles_data = pd.read_csv('vehicles_us.csv')

vehicles_data['model_year'] = vehicles_data.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
vehicles_data['cylinders'] = vehicles_data.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))
vehicles_data['odometer'] = vehicles_data.groupby(['model_year', 'model'])['odometer'].transform(lambda x: x.fillna(x.median()))

def remove_outliers(vehilces_data, column):
    Q1 = vehicles_data[column].quantile(0.25)
    Q3 = vehicles_data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return vehicles_data[(vehicles_data[column] >= lower_bound) & (vehicles_data[column] <= upper_bound)]

vehicles_data = remove_outliers(vehicles_data, 'model_year')
vehicles_data = remove_outliers(vehicles_data, 'price')


vehicles_data['manufacturer'] = vehicles_data['model'].str.split().str[0]

st.header('Vehicle Analysis Dashboard')
st.dataframe(vehicles_data)







#

models_per_manufacturer = vehicles_data.groupby('manufacturer')['model'].nunique().reset_index(name= 'Number of Models')

show_fig1 = st.checkbox('Show Number of Different Car Models per Manufacturer')

if show_fig1:
    fig = px.bar(models_per_manufacturer, x='manufacturer', y='Number of Models',
             title="Number of Models per Manufacturer",
             labels={"Number of Models": "Count of Models", "manufacturer": "Manufacturer"})

    st.plotly_chart(fig)
    st.markdown('This is a bar graph of the number of different car models each manufacturer has based on the data')

#

vehicle_types = vehicles_data.groupby('manufacturer')['type'].nunique().reset_index(name='Number of Vehicles Types')

show_fig2 = 'Number of Types of Cars each Manufacturer has within the Dataset'

if show_fig2:
    fig = px.bar(vehicle_types, x='manufacturer', y='Number of Vehicles Types',
             title="Number of Types of Cars per Manufacturer",
             labels={"Number of Types of Cars": "Count of Car Types", "manufacturer": "Manufacturer"})


    st.plotly_chart
    st.markdown('This is a bar graph that shows us the variety of the number of types of cars each manufacturer has within this car advertisement dataset')

#

vehicle_type_counts = vehicles_data.groupby(['manufacturer', 'type'])['type'].count().reset_index(name='Number of Vehicles')
pivot_df = vehicle_type_counts.pivot(index='manufacturer', columns='type', values= 'Number of Vehicles').fillna(0)

melted_df = pivot_df.reset_index().melt(id_vars='manufacturer', var_name='type', value_name='Number of Vehicles')

show_fig3 = st.checkbox('Show Distribution of different car types for each manufacturer')

if show_fig3:
    fig = px.bar(melted_df,
             x='manufacturer',
             y='Number of Vehicles',
             color='type',  # Differentiates vehicle types with color
             title='Distribution of Vehicle Types by Manufacturer')



        # Rotated x-axis labels for better readability
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig)
    st.markdown('This is a bar graph that shows each manufacturers most common type of car that they build based on the data')

#


vehicles_data_clean = vehicles_data.dropna(subset=['price', 'manufacturer'])

average_price_per_manufacturer = vehicles_data_clean.groupby('manufacturer')['price'].mean().reset_index(name='Average Price')

show_fig4 = st.checkbox('Show average price per manufactuer')

if show_fig4:
    fig = px.scatter(average_price_per_manufacturer, x='Average Price', y='manufacturer',
                 color='manufacturer',  # This assigns a unique color to each manufacturer
                 hover_data=['manufacturer', 'Average Price'],  # Customize hover data
                 title="Average Vehicle Price by Manufacturer")

    st.plotly_chart(fig)
    st.markdown('This is a scatter plot that shows us the average car price for each manufacturer based on the data')

#

show_fig5 = st.checkbox('Show average price distribution per manufacturer')

if show_fig5:
    fig = px.histogram(vehicles_data, 
                   x="price", 
                   color="manufacturer", 
                   barmode="overlay", 
                   nbins=50, 
                   title="Price Distribution by Manufacturer")


    st.plotly_chart(fig)
    st.markdown('This histogram shows us the distribution of prices for each manufacturer')

#

show_fig6 = st.checkbox('Show the manufacturers whom had the best conditioned cars')

if show_fig6:
    condition_counts = vehicles_data.groupby(['manufacturer', 'condition']).size().reset_index(name='count')

    fig = px.bar(condition_counts,
             x='manufacturer',
             y='count',
             color='condition',
             title='Car Conditions Across Manufacturers')

    st.plotly_chart(fig)
    st.markdown('This bar graph show us the manufacturers who had the most and least cars with certain conditions')

#

transmission_data = vehicles_data[['manufacturer', 'transmission']]
transmission_counts = vehicles_data.groupby(['manufacturer','transmission']).size().reset_index(name='count')

show_fig7 = st.checkbox('Show most frequent types of cars built regarding manual, automatic or other')

if show_fig7:
    fig = px.bar(transmission_counts,
             x='manufacturer',
             y='count',
             color='transmission', # This will create different bars/colors for each transmission type
             barmode='group', # This ensures that the bars for each transmission type are grouped
             title='Count of Vehicle Transmissions by Manufacturer')

    st.plotly_chart(fig)
    st.markdown('This bar graph shows us the frequent types of transmissions the manufacturers most commonly built')