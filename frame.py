import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dbhelper import DB

db = DB()
df = pd.read_csv(r'C:\Users\HP\Desktop\Project -Tags\Indian_StartUp_Analyis\startup_cleaned.csv')

st.sidebar.title('Startup Funding Analysis')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


def load_overall_analysis():
    st.markdown('<h1 style="font-weight:bold; color:brown;">Overall Analysis</h1>', unsafe_allow_html=True)

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<h2 style="color:blue;">Total Amount</h2>', unsafe_allow_html=True)
        st.metric('total', str(total) + ' Cr')
    with col2:
        st.markdown('<h2 style="color:green;">Maximum Amount</h2>', unsafe_allow_html=True)
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.markdown('<h2 style="color:orange;">Average Amount</h2>', unsafe_allow_html=True)
        st.metric('avg', str(round(avg_funding)) + ' Cr')

    with col4:
        st.markdown('<h2 style="color:yellow;">Funded StartUps</h2>', unsafe_allow_html=True)
        st.metric('Numbers', num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)
    # top invested sector
    fig4, ax4 = plt.subplots()
    st.subheader('Top Sectors Money Invested')
    x1 = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
    ax4.pie(x1, labels=x1.index, autopct='%.2f')
    st.pyplot(fig4)
    # number of startups in top setors
    fig5, ax5 = plt.subplots()
    st.subheader('Number StartUps in top Sectors')
    x2 = df.groupby('vertical')['startup'].count().sort_values(ascending=False).head(5)
    ax5.pie(x1, labels=x1.index, autopct=lambda pct: f'{int(pct / 100 * x2.sum())} ({pct:.2f}%)')
    st.pyplot(fig5)
    # types of funding
    st.subheader('Types of funding')
    y = df['round'].value_counts()
    st.dataframe(y)
    # citywise funding
    st.subheader('Citywise Funding')
    y1 = df.groupby(['city', 'round'])['startup'].count()
    st.dataframe(y1)
    # top startups yearwise
    y2 = df.groupby(['year', 'startup'])['amount'].sum().groupby('year').nlargest(3)
    st.dataframe(y2)

    # top investors(bar graph)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    y3 = df.groupby('investors')['amount'].sum().head(3)
    ax6.bar(y3.index, y3.values)
    plt.xticks(rotation=45)
    st.pyplot(fig6)

    # funding heatmap
    fig7, ax7 = plt.subplots()
    st.subheader('Heatmap Funding')
    data_matrix = df[['year', 'amount']].corr()
    sns.heatmap(data_matrix, annot=True, cmap='coolwarm')
    st.pyplot(fig7)


def load_start_up_details(startup):
    st.title(startup)
    col1, col2, col3 = st.columns(3)
    industry = df[df['startup'] == startup]['vertical'].values[0]
    sub_industry = df[df['startup'] == startup]['subvertical'].values[0]
    location = df[df['startup'] == startup]['city'].values[0]
    with col1:
        st.metric('Industry', str(industry))
    with col2:
        st.metric('Sub Industry', str(sub_industry))
    with col3:
        st.metric('Location', str(location))

    st.subheader('Funding Rounds')
    funding_details = df[df['startup'] == startup][['date', 'round', 'investors']].reset_index(drop=True)
    st.dataframe(funding_details)

    st.subheader('Similar Companies')
    vert = df[df['startup'] == startup]['vertical'].values[0]
    st.dataframe(df[df['vertical'] == vert]['startup'].reset_index(drop=True))


def load_investor_details(investor):
    # load recent 5 investments
    st.title(investor)

    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Rounds invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(round_series, labels=round_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)

    with col4:
        round_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('Cities invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(round_series, labels=round_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)

        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

        st.subheader('YoY Investment')
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index, year_series.values)

        st.pyplot(fig2)

    similar_investors = df[df['vertical'].isin(df[df['investors'] == 'Sequoia Capital India']['vertical'].values)][
        'investors'].head(5)
    st.subheader('Similar investors')
    st.subheader('Similar investors')
    st.dataframe(similar_investors)


option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_start_up_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')
    if btn2:
        load_investor_details(selected_investor)
