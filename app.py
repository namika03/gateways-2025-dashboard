import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from mpl_toolkits.basemap import Basemap
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="GATEWAYS-2025 Analytics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
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

# Title and description
st.title("GATEWAYS-2025 Fest Analytics Dashboard")
st.markdown("**Comprehensive Analysis of Participation Trends, Feedback & Insights**")
st.divider()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis", 
    ["Overview", "State-wise Distribution Map", "Participation Trends", "Feedback & Ratings Analysis"])

# ============= PAGE: OVERVIEW =============
if page == "Overview":
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Participants", len(df))
    
    with col2:
        st.metric("Total Events", df['Event Name'].nunique())
    
    with col3:
        st.metric("Participating Colleges", df['College'].nunique())
    
    with col4:
        st.metric("States Covered", df['State'].nunique())
    
    st.divider()
    
    # Key Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Participation by Event Type")
        event_type_dist = df['Event Type'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#FF6B6B', '#4ECDC4']
        ax.bar(event_type_dist.index, event_type_dist.values, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Event Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Distribution by Event Type', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Rating by Event Type")
        avg_rating = df.groupby('Event Type')['Rating'].mean()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(avg_rating.index, avg_rating.values, color=['#95E1D3', '#F38181'], edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Event Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Rating', fontsize=12, fontweight='bold')
        ax.set_title('Average Rating by Event Type', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 5)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.divider()
    
    # Top events
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Events by Participation")
        top_events = df['Event Name'].value_counts().head(5)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top_events.index, top_events.values, color='#6C5CE7', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Top 5 Events by Participation', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 10 Colleges by Participation")
        top_colleges = df['College'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top_colleges.index, top_colleges.values, color='#00B894', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Colleges by Participation', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

# ============= PAGE: STATE-WISE DISTRIBUTION MAP =============
elif page == "State-wise Distribution Map":
    st.header("🗺️ State-wise Participant Distribution in India")
    
    # Count participants by state
    state_count = df['State'].value_counts().to_dict()
    
    st.subheader("State-wise Participation Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("States with Most Participants", 
                  df['State'].value_counts().index[0],
                  f"{df['State'].value_counts().values[0]} participants")
    
    with col2:
        st.metric("Average Participants per State", 
                  f"{len(df) / df['State'].nunique():.1f}")
    
    with col3:
        st.metric("Total States", len(state_count))
    
    st.divider()
    
    # State participation table
    st.subheader("Detailed State-wise Breakdown")
    state_details = df.groupby('State').agg({
        'Student Name': 'count',
        'Rating': 'mean',
        'Amount Paid': 'sum'
    }).rename(columns={'Student Name': 'Participants', 'Rating': 'Avg Rating', 'Amount Paid': 'Revenue'})
    state_details = state_details.sort_values('Participants', ascending=False)
    state_details['Avg Rating'] = state_details['Avg Rating'].round(2)
    state_details['Revenue'] = state_details['Revenue'].astype(int)
    
    st.dataframe(state_details, use_container_width=True)
    
    st.divider()
    
    # Create India map with Basemap showing state-wise participation
    st.subheader("India Map - State-wise Participant Distribution")
    
    # State coordinates (latitude, longitude for Basemap projection)
    state_coordinates = {
        'Andhra Pradesh': [15.9129, 78.6675],
        'Arunachal Pradesh': [28.2180, 94.7278],
        'Assam': [26.2006, 92.9376],
        'Bihar': [25.5941, 85.1376],
        'Chhattisgarh': [21.2787, 81.8661],
        'Goa': [15.2993, 73.8243],
        'Gujarat': [22.2587, 71.1924],
        'Haryana': [29.0588, 77.0745],
        'Himachal Pradesh': [31.7433, 77.1205],
        'Jharkhand': [23.6102, 85.2799],
        'Karnataka': [15.3173, 75.7139],
        'Kerala': [10.8505, 76.2711],
        'Madhya Pradesh': [22.9375, 78.6553],
        'Maharashtra': [19.7515, 75.7139],
        'Manipur': [24.6637, 93.9063],
        'Meghalaya': [25.4670, 91.3662],
        'Mizoram': [23.1815, 92.9789],
        'Nagaland': [26.1584, 94.5624],
        'Odisha': [20.9517, 85.0985],
        'Punjab': [31.1471, 75.3412],
        'Rajasthan': [27.0238, 74.2179],
        'Sikkim': [27.5330, 88.5122],
        'Tamil Nadu': [11.1271, 79.2787],
        'Telangana': [18.1124, 79.0193],
        'Tripura': [23.4291, 91.9150],
        'Uttar Pradesh': [26.8467, 80.9462],
        'Uttarakhand': [30.0668, 79.0193],
        'West Bengal': [24.5155, 88.2289],
        'Delhi': [28.7041, 77.1025],
        'Jammu and Kashmir': [33.7782, 76.5769],
        'Ladakh': [33.7782, 76.5769],
        'Puducherry': [11.9416, 79.8083],
        'Chandigarh': [30.7333, 76.7794],
        'Lakshadweep': [10.5667, 72.7417],
        'Andaman and Nicobar Islands': [11.7401, 92.6586],
        'Daman and Diu': [20.4283, 72.8479],
        'Dadra and Nagar Haveli': [20.1809, 73.0326]
    }
    
    # Create Basemap visualization
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Create Basemap for India
    m = Basemap(projection='merc', llcrnrlat=6, urcrnrlat=37, 
                llcrnrlon=68, urcrnrlon=98, ax=ax, resolution='l')
    
    # Draw map features
    m.drawcoastlines(linewidth=1, color='black')
    m.drawcountries(linewidth=1.5, color='black')
    m.drawstates(linewidth=0.5, color='gray')
    
    # Get maximum participant count for scaling
    max_count = max(state_count.values()) if state_count else 1
    
    # Plot each state as a circle with size proportional to participant count
    for state, count in state_count.items():
        if state in state_coordinates:
            lat, lon = state_coordinates[state]
            x, y = m(lon, lat)
            
            # Scale the marker size based on participant count
            size = (count / max_count) * 500 + 50
            
            # Color based on participant count
            if count >= max_count * 0.6:
                color = '#FF4444'  # Dark red for high
            elif count >= max_count * 0.3:
                color = '#FF8844'  # Orange for medium
            else:
                color = '#FFB84D'  # Yellow for low
            
            # Plot marker
            m.scatter(x, y, marker='o', s=size, c=color, alpha=0.7, 
                     edgecolors='black', linewidth=2, zorder=5)
            
            # Add state name and count annotation
            ax.annotate(f"{state}\n({count})", xy=(x, y), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax.set_title('India Map - State-wise Participant Distribution in GATEWAYS-2025', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    legend_text = """
    Legend:
    🔴 Red circles: States with high participation (>60% of max)
    🟠 Orange circles: States with medium participation (30-60% of max)
    🟡 Yellow circles: States with lower participation (<30% of max)
    Circle size: Proportional to number of participants
    """
    ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # Statistics by state
    st.subheader("State-wise Statistics")
    
    state_stats = df.groupby('State').agg({
        'Student Name': 'count',
        'Rating': 'mean',
        'Amount Paid': 'sum',
        'College': 'nunique'
    }).rename(columns={
        'Student Name': 'Participants',
        'Rating': 'Avg Rating',
        'Amount Paid': 'Revenue',
        'College': 'Colleges'
    }).sort_values('Participants', ascending=False)
    
    state_stats['Avg Rating'] = state_stats['Avg Rating'].round(2)
    state_stats['Revenue'] = state_stats['Revenue'].astype(int)
    
    st.dataframe(state_stats, use_container_width=True)
    
    st.divider()
    
    # Additional visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("State-wise Average Rating")
        state_rating_top = df.groupby('State')['Rating'].mean().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(state_rating_top.index, state_rating_top.values, color='#FF6B6B', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Average Rating', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 States by Average Rating', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 5)
        for i, v in enumerate(state_rating_top.values):
            ax.text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("State-wise Revenue Distribution")
        state_revenue = df.groupby('State')['Amount Paid'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(state_revenue.index, state_revenue.values, color='#4ECDC4', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Total Revenue (₹)', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 States by Revenue', fontsize=14, fontweight='bold')
        for i, v in enumerate(state_revenue.values):
            ax.text(v + 100, i, f'₹{v:,}', va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

# ============= PAGE: PARTICIPATION TRENDS =============
elif page == "Participation Trends":
    st.header("Participation Trends Analysis")
    
    # Event-wise analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Participation by Event")
        event_dist = df['Event Name'].value_counts().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(event_dist.index, event_dist.values, color='#5F27CD', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Event-wise Participation Distribution', fontsize=14, fontweight='bold')
        for i, v in enumerate(event_dist.values):
            ax.text(v + 0.5, i, str(v), va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Rating by Event")
        event_rating = df.groupby('Event Name')['Rating'].mean().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(event_rating.index, event_rating.values, color='#00D2D3', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Average Rating', fontsize=12, fontweight='bold')
        ax.set_title('Average Rating by Event', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 5)
        for i, v in enumerate(event_rating.values):
            ax.text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    st.divider()
    
    # Top colleges analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Colleges by Participation")
        college_dist = df['College'].value_counts().head(15).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(college_dist.index, college_dist.values, color='#FF6348', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Top 15 Colleges - Participation', fontsize=14, fontweight='bold')
        for i, v in enumerate(college_dist.values):
            ax.text(v + 0.3, i, str(v), va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 15 Colleges by Average Rating")
        college_rating = df.groupby('College')['Rating'].agg(['mean', 'count'])
        college_rating = college_rating[college_rating['count'] >= 2].sort_values('mean', ascending=False).head(15)
        college_rating_sorted = college_rating['mean'].sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(college_rating_sorted.index, college_rating_sorted.values, color='#1DD1A1', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Average Rating', fontsize=12, fontweight='bold')
        ax.set_title('Top 15 Colleges - Average Rating', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 5)
        for i, v in enumerate(college_rating_sorted.values):
            ax.text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    st.divider()
    
    # Rating distribution
    st.subheader("Overall Rating Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        rating_dist = df['Rating'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_rating = ['#FF4757', '#FFA502', '#FFD93D', '#6BCB77', '#4D96FF']
        ax.bar(rating_dist.index, rating_dist.values, color=colors_rating[:len(rating_dist)], 
               edgecolor='black', linewidth=2, width=0.6)
        ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Participants', fontsize=12, fontweight='bold')
        ax.set_title('Overall Rating Distribution', fontsize=14, fontweight='bold')
        ax.set_xticks([1, 2, 3, 4, 5])
        for i, v in enumerate(rating_dist.values):
            ax.text(rating_dist.index[i], v + 0.5, str(v), ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.metric("Average Rating", f"{df['Rating'].mean():.2f}/5")
        st.metric("Median Rating", df['Rating'].median())
        st.metric("Mode Rating", df['Rating'].mode()[0] if len(df['Rating'].mode()) > 0 else "N/A")
    
    st.divider()
    
    # Revenue analysis
    st.subheader("Revenue Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"₹{df['Amount Paid'].sum():,}")
    
    with col2:
        st.metric("Average Amount per Participant", f"₹{df['Amount Paid'].mean():.0f}")
    
    with col3:
        st.metric("Highest Amount Event", 
                  df.groupby('Event Name')['Amount Paid'].sum().idxmax(),
                  f"₹{df.groupby('Event Name')['Amount Paid'].sum().max():,}")
    
    with col4:
        st.metric("Revenue by Event Type", 
                  f"Individual: ₹{df[df['Event Type']=='Individual']['Amount Paid'].sum():,}")

# ============= PAGE: FEEDBACK & RATINGS ANALYSIS =============
elif page == "Feedback & Ratings Analysis":
    st.header("Feedback & Ratings Analysis")
    
    # Sentiment Analysis
    st.subheader("Feedback Quality Analysis")
    
    # Simple sentiment analysis using keyword matching
    def get_sentiment(text):
        if pd.isna(text):
            return 0
        
        text_lower = str(text).lower()
        
        positive_words = ['excellent', 'great', 'good', 'amazing', 'awesome', 'creative', 
                         'engaging', 'informative', 'interactive', 'fun', 'useful', 'practical',
                         'enjoyed', 'loved', 'wonderful', 'fantastic', 'brilliant', 'insightful']
        negative_words = ['bad', 'poor', 'weak', 'boring', 'disappointing', 'improvement needed',
                         'needs improvement', 'issue', 'disappointing', 'could be better']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 1  # Positive
        elif negative_count > positive_count:
            return -1  # Negative
        else:
            return 0  # Neutral
    
    df['Sentiment'] = df['Feedback on Fest'].apply(get_sentiment)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Positive Feedback %", 
                  f"{(df['Sentiment'] > 0).sum() / len(df) * 100:.1f}%")
        st.metric("Neutral Feedback %", 
                  f"{(df['Sentiment'] == 0).sum() / len(df) * 100:.1f}%")
    
    with col2:
        st.metric("Negative Feedback %", 
                  f"{(df['Sentiment'] < 0).sum() / len(df) * 100:.1f}%")
        st.metric("Total Feedback Entries", len(df[df['Feedback on Fest'].notna()]))
    
    st.divider()
    
    # Feedback sentiment distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Feedback Sentiment Distribution")
        sentiment_labels = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}
        sentiment_dist = df['Sentiment'].map(sentiment_labels).value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_sent = ['#6BCB77', '#FFD93D', '#FF6B6B']
        sentiment_order = ['Positive', 'Neutral', 'Negative']
        sentiment_dist_ordered = sentiment_dist.reindex(sentiment_order, fill_value=0)
        ax.bar(sentiment_dist_ordered.index, sentiment_dist_ordered.values, 
               color=colors_sent[:len(sentiment_dist_ordered)], edgecolor='black', linewidth=2)
        ax.set_ylabel('Number of Responses', fontsize=12, fontweight='bold')
        ax.set_title('Feedback Sentiment Distribution', fontsize=14, fontweight='bold')
        for i, v in enumerate(sentiment_dist_ordered.values):
            ax.text(i, v + 1, str(v), ha='center', fontweight='bold', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Sentiment vs Rating Correlation")
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(df['Sentiment'], df['Rating'], 
                           c=df['Rating'], cmap='RdYlGn', 
                           s=100, alpha=0.6, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Sentiment (-1: Negative, 0: Neutral, 1: Positive)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Rating', fontsize=12, fontweight='bold')
        ax.set_title('Sentiment vs Rating Correlation', fontsize=14, fontweight='bold')
        ax.set_xticks([-1, 0, 1])
        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        plt.colorbar(scatter, ax=ax, label='Rating')
        plt.tight_layout()
        st.pyplot(fig)
    
    st.divider()
    
    # Most common feedback words/phrases
    st.subheader("Common Feedback Themes")
    
    # Extract common words from feedback
    from collections import Counter
    all_feedback = ' '.join(df['Feedback on Fest'].dropna().astype(str))
    feedback_lower = all_feedback.lower()
    
    # List of positive and negative keywords
    positive_keywords = ['excellent', 'great', 'good', 'amazing', 'awesome', 'creative', 
                        'engaging', 'informative', 'interactive', 'fun', 'useful', 'practical']
    negative_keywords = ['bad', 'poor', 'weak', 'boring', 'disappointing', 'improvement', 'needs', 'issue']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Positive Keywords")
        positive_counts = {}
        for keyword in positive_keywords:
            count = feedback_lower.count(keyword)
            if count > 0:
                positive_counts[keyword] = count
        
        if positive_counts:
            positive_counts = dict(sorted(positive_counts.items(), key=lambda x: x[1], reverse=True)[:8])
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(list(positive_counts.keys()), list(positive_counts.values()), 
                   color='#1DD1A1', edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_title('Top Positive Keywords in Feedback', fontsize=14, fontweight='bold')
            for i, v in enumerate(positive_counts.values()):
                ax.text(v + 0.2, i, str(v), va='center', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No positive keywords found")
    
    with col2:
        st.subheader("Top Negative Keywords")
        negative_counts = {}
        for keyword in negative_keywords:
            count = feedback_lower.count(keyword)
            if count > 0:
                negative_counts[keyword] = count
        
        if negative_counts:
            negative_counts = dict(sorted(negative_counts.items(), key=lambda x: x[1], reverse=True)[:8])
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(list(negative_counts.keys()), list(negative_counts.values()), 
                   color='#FF6348', edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_title('Top Negative Keywords in Feedback', fontsize=14, fontweight='bold')
            for i, v in enumerate(negative_counts.values()):
                ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No negative keywords found")
    
    st.divider()
    
    # Feedback by Rating
    st.subheader("Feedback Analysis by Rating")
    
    rating_options = sorted(df['Rating'].unique())
    selected_rating = st.selectbox("Select a Rating to View Feedback:", rating_options)
    
    feedback_by_rating = df[df['Rating'] == selected_rating]['Feedback on Fest'].tolist()
    
    st.write(f"**Total feedback entries with rating {selected_rating}: {len(feedback_by_rating)}**")
    
    if feedback_by_rating:
        for idx, feedback in enumerate(feedback_by_rating[:10], 1):
            st.markdown(f"**{idx}.** {feedback}")
        
        if len(feedback_by_rating) > 10:
            st.info(f"Showing 10 of {len(feedback_by_rating)} feedback entries")
    else:
        st.info("No feedback found for this rating")
    
    st.divider()
    
    # Feedback statistics
    st.subheader("Feedback Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback Entries", len(df[df['Feedback on Fest'].notna()]))
    
    with col2:
        avg_feedback_length = df['Feedback on Fest'].str.len().mean()
        st.metric("Average Feedback Length", f"{avg_feedback_length:.0f} characters")
    
    with col3:
        st.metric("Unique Feedback Entries", df['Feedback on Fest'].nunique())
    
    st.divider()
    
    # Heatmap: Event x Rating
    st.subheader("Event vs Rating Analysis")
    
    event_rating_matrix = pd.crosstab(df['Event Name'], df['Rating'])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(event_rating_matrix, annot=True, fmt='d', cmap='YlGn', 
                cbar_kws={'label': 'Count'}, ax=ax, linewidths=0.5, linecolor='gray')
    ax.set_title('Event vs Rating Heatmap', fontsize=14, fontweight='bold')
    ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
    ax.set_ylabel('Event Name', fontsize=12, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)


