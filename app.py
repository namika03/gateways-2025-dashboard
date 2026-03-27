import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="GATEWAYS-2025 Analytics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('fest.csv')
    return df

df = load_data()

# Title
st.title("GATEWAYS-2025 Fest Analytics Dashboard")
st.markdown("Comprehensive Analysis of Participation Trends, Feedback & Insights")
st.divider()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis",
                        ["Overview", "State-wise Distribution Map",
                         "Participation Trends", "Feedback & Ratings Analysis"])

# ================= OVERVIEW =================
if page == "Overview":

    st.header("Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Participants", len(df))
    col2.metric("Total Events", df['Event Name'].nunique())
    col3.metric("Participating Colleges", df['College'].nunique())
    col4.metric("States Covered", df['State'].nunique())

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Participation by Event Type")
        event_type_dist = df['Event Type'].value_counts()
        st.bar_chart(event_type_dist)

    with col2:
        st.subheader("Average Rating by Event Type")
        avg_rating = df.groupby('Event Type')['Rating'].mean()
        st.bar_chart(avg_rating)

# ================= STATE MAP =================
elif page == "State-wise Distribution Map":

    st.header("State-wise Participant Distribution in India")

    state_count = df['State'].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Top State", state_count.index[0])
    col2.metric("Participants", state_count.values[0])
    col3.metric("Total States", len(state_count))

    st.divider()

    st.subheader("State-wise Participation")

    fig, ax = plt.subplots(figsize=(12,8))
    ax.barh(state_count.index[:20], state_count.values[:20])
    ax.set_xlabel("Participants")
    ax.set_title("Top States by Participation")
    st.pyplot(fig)

# ================= PARTICIPATION =================
elif page == "Participation Trends":

    st.header("Participation Trends Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Participation by Event")
        st.bar_chart(df['Event Name'].value_counts())

    with col2:
        st.subheader("Participation by College")
        st.bar_chart(df['College'].value_counts().head(15))

    st.divider()

    st.subheader("Rating Distribution")
    st.bar_chart(df['Rating'].value_counts())

# ================= FEEDBACK =================
elif page == "Feedback & Ratings Analysis":

    st.header("Feedback & Ratings Analysis")

    def get_sentiment(text):
        if pd.isna(text):
            return 0
        text = str(text).lower()

        positive = ['good', 'excellent', 'great', 'amazing', 'nice', 'awesome']
        negative = ['bad', 'poor', 'boring', 'worst', 'issue']

        pos = sum(word in text for word in positive)
        neg = sum(word in text for word in negative)

        if pos > neg:
            return 1
        elif neg > pos:
            return -1
        else:
            return 0

    df['Sentiment'] = df['Feedback on Fest'].apply(get_sentiment)

    col1, col2, col3 = st.columns(3)

    col1.metric("Positive %",
                round((df['Sentiment'] > 0).mean()*100,2))
    col2.metric("Neutral %",
                round((df['Sentiment'] == 0).mean()*100,2))
    col3.metric("Negative %",
                round((df['Sentiment'] < 0).mean()*100,2))

    st.divider()

    st.subheader("Sentiment Distribution")
    st.bar_chart(df['Sentiment'].value_counts())

    st.divider()

    st.subheader("Event vs Rating Heatmap")
    matrix = pd.crosstab(df['Event Name'], df['Rating'])

    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(matrix, annot=True, cmap="YlGn", fmt='d', ax=ax)
    st.pyplot(fig)
