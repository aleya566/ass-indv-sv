import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Student Sleep and Educational Outcomes Analysis")

# --- Data Loading ---
@st.cache_data
def load_data(url):
    """Loads the dataset from the provided URL."""
    try:
        df = pd.read_csv(url)
        # Standardize column names for easier access (optional but helpful)
        df.columns = [
            'ID', 'Year_of_Study', 'Gender', 'Age', 'Avg_Sleep_Hours',
            'Time_to_Sleep', 'Sleep_Quality', 'Insomnia_Severity',
            'Sleep_Interference', 'Tiredness_Impact', 'Energy_Levels',
            'Coping_Ability', 'Social_Life_Impact', 'Academic_Stress_Level',
            'Academic_Performance', 'Other_Factors'
        ]
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Data URL
url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
df = load_data(url)

# Check if data loaded successfully
if df.empty:
    st.stop()

st.title("Student Insomnia and Educational Outcomes Analysis")
st.markdown("Exploring the distribution of key sleep and stress factors among students across different years of study and genders using Plotly.")

# Display a snippet of the data
st.subheader("Raw Data Snippet")
st.dataframe(df.head())

st.divider()

## 1. Stacked Bar Chart: Academic Stress Levels by Year of Study

st.header("1. Academic Stress Levels by Year of Study")

# Prepare the data for the stacked bar chart (normalization/crosstab)
stress_year_crosstab = pd.crosstab(df['Year_of_Study'], df['Academic_Stress_Level'], normalize='index').reset_index()
stress_year_crosstab = stress_year_crosstab.melt(id_vars='Year_of_Study', var_name='Stress_Level', value_name='Proportion')

# Define a consistent color sequence based on stress level for clarity
stress_level_order = ['Very Low Stress', 'Low Stress', 'Moderate Stress', 'High Stress', 'Very High Stress']
# Using a 'flare'-like palette or a sequential one for stress
stress_colors = ['#abd9e9', '#74add1', '#4575b4', '#313695', '#a50026'] # Blue to Red gradient

# Create the stacked bar chart using Plotly Express
fig1 = px.bar(
    stress_year_crosstab,
    x='Year_of_Study',
    y='Proportion',
    color='Stress_Level',
    category_orders={'Stress_Level': stress_level_order}, # Ensure consistent ordering
    color_discrete_sequence=stress_colors,
    title='Proportion of Academic Stress Levels by Year of Study',
    labels={
        'Year_of_Study': 'Year of Study',
        'Proportion': 'Proportion',
        'Stress_Level': 'Stress Level'
    }
)

fig1.update_layout(
    xaxis_title='Year of Study',
    yaxis_title='Proportion',
    yaxis_tickformat='.0%', # Format y-axis as percentage
    legend_title='Stress Level',
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

## 2. Box Plot: Average Sleep Hours by Gender

st.header("2. Average Sleep Hours by Gender")

# Create the box plot using Plotly Express
fig2 = px.box(
    df.replace({'Gender': {'2': 'Female', '1': 'Male'}}), # Clean the 'Gender' column
    x='Gender',
    y='Avg_Sleep_Hours',
    color='Gender',
    category_orders={'Gender': ['Male', 'Female']},
    color_discrete_sequence=px.colors.sequential.Flare,
    title='Distribution of Average Sleep Hours by Gender',
    labels={
        'Gender': 'Gender',
        'Avg_Sleep_Hours': 'Average Sleep Hours (Hours)'
    }
)

fig2.update_layout(
    xaxis_title='Gender',
    yaxis_title='Average Sleep Hours',
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

## 3. Stacked Bar Chart: Sleep Quality vs Academic Performance

st.header("3. Relationship between Sleep Quality and Academic Performance")

# Prepare the data for the second stacked bar chart (normalization/crosstab)
cross_tab_perf = pd.crosstab(df['Sleep_Quality'], df['Academic_Performance'], normalize='index').reset_index()
cross_tab_perf = cross_tab_perf.melt(id_vars='Sleep_Quality', var_name='Academic_Performance', value_name='Proportion')

# Define order for Sleep Quality and Academic Performance
sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']
performance_order = ['Poor', 'Fair', 'Good', 'Excellent']

# Create the stacked bar chart using Plotly Express
fig3 = px.bar(
    cross_tab_perf,
    x='Sleep_Quality',
    y='Proportion',
    color='Academic_Performance',
    category_orders={'Sleep_Quality': sleep_quality_order, 'Academic_Performance': performance_order},
    color_discrete_sequence=px.colors.sequential.Sunsetdark, # Another 'flare'-like palette
    title='Proportion of Academic Performance by Sleep Quality',
    labels={
        'Sleep_Quality': 'Sleep Quality',
        'Proportion': 'Proportion',
        'Academic_Performance': 'Academic Performance'
    }
)

fig3.update_layout(
    xaxis_title='Sleep Quality',
    yaxis_title='Proportion',
    yaxis_tickformat='.0%',
    legend_title='Academic Performance',
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)
