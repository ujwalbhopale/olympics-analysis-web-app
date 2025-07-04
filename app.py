import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess the data
df = preprocessor.preprocess(df, region_df)

st.title("Olympics Analysis App")

st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    year,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if year == 'Overall' and country == 'Overall':
        st.title("Overall Tally")
    if year == 'Overall' and country != 'Overall':
        st.title(selected_country + " Overall Performance")
    if year != 'Overall' and country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if year != 'Overall' and country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")

    st.dataframe(medal_tally)

if user_menu=='Overall Analysis':

    st.title("Top Statics")
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time=helper.data_over_time(df,'region')
    st.title('Participating Nations Over the years')
    fig = px.line(nations_over_time, x='Editions', y='region')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    st.title('Participating Events Over the years')
    fig = px.line(events_over_time, x='Editions', y='Event')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    st.title('Participating Athlete Over the years')
    fig = px.line(athlete_over_time, x='Editions', y='Name')
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select Sport",sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':

    st.sidebar.title("Country-wise Analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.title("Height vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select Sport", sport_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title("Men vs Women partcipation over the years")
    final=helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)