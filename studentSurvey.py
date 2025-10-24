import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the page configuration
st.set_page_config(
    page_title="Student Sleep and Educational Outcomes Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

## Data Loading
@st.cache_data
def load_data():
    """Loads and caches the dataset."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset_version-2.csv'
    df = pd.read_csv(url)
    
    # Rename columns for easier use
    df.columns = [
        'Timestamp', 'Gender', 'Year of Study', 'Sleep Hours', 'Sleep Latency', 
        'Sleep Quality', 'Insomnia Status', 'Morning Fatigue', 'Daytime Sleepiness', 
        'Focus Difficulty', 'Emotional Control Difficulty', 'Stress Level', 
        'Academic Stress', 'Academic Performance', 'Future Plans Impact', 
        'Mental Health Impact', 'Mental Health Support'
    ]
    return df

df = load_data()

st.title("Student Sleep and Educational Outcomes Analysis 🎓")
st.markdown("This dashboard explores the distribution of key sleep and stress factors among students across different years of study and genders, using data from the **Student Insomnia and Educational Outcomes Dataset**.")

# Display a snippet of the data
if st.checkbox('Show raw data', False):
    st.subheader('Raw Data Sample')
    st.dataframe(df.head())

# Add a divider
st.markdown("---")

## 1. Stacked Bar Chart – Academic Stress Levels by Year of Study (Plotly)
st.header("1. Academic Stress Levels by Year of Study")
st.markdown("This plot shows the proportion of students in each year of study who reported different levels of academic stress.")

# Prepare the data (same as your original crosstab)
stress_year_crosstab = pd.crosstab(
    df['Year of Study'], 
    df['Academic Stress'], 
    normalize='index'
).reset_index()

# Melt the dataframe for Plotly Express (suitable for stacked bar charts)
stress_year_melted = stress_year_crosstab.melt(
    id_vars='Year of Study',
    value_vars=stress_year_crosstab.columns[1:],
    var_name='Academic Stress Level',
    value_name='Proportion'
)

# Plot using Plotly Express
fig_stress_year = px.bar(
    stress_year_melted,
    x='Year of Study',
    y='Proportion',
    color='Academic Stress Level',
    title='Academic Stress Levels by Year of Study (Proportion)',
    labels={'Proportion': 'Proportion of Students', 'Year of Study': 'Year of Study'},
    color_discrete_sequence=px.colors.sequential.Sunsetdark  # Use a nice color sequence
)

# Customize layout
fig_stress_year.update_layout(
    xaxis_title='Year of Study',
    yaxis_title='Proportion',
    legend_title='Stress Level',
    barmode='stack',
    hovermode="x unified"
)

st.plotly_chart(fig_stress_year, use_container_width=True)

# Add a divider
st.markdown("---")

## 2. Box Plot – Average Sleep Hours by Gender (Plotly)
st.header("2. Average Sleep Hours by Gender")
st.markdown("This box plot visualizes the distribution of average sleep hours for male and female students.")

# Plot using Plotly Express
fig_sleep_gender = px.box(
    df,
    x='Gender',
    y='Sleep Hours',
    color='Gender',
    title='Distribution of Average Sleep Hours by Gender',
    labels={'Sleep Hours': 'Average Sleep Hours', 'Gender': 'Gender'},
    color_discrete_map={'Male': '#D84315', 'Female': '#6A1B9A'} # Custom colors
)

# Customize layout
fig_sleep_gender.update_layout(
    xaxis_title='Gender',
    yaxis_title='Average Sleep Hours',
    showlegend=False
)

st.plotly_chart(fig_sleep_gender, use_container_width=True)

# Add a divider
st.markdown("---")

## 3. Stacked Bar Chart - Sleep Quality vs Academic Performance (Plotly)
st.header("3. Sleep Quality vs Academic Performance")
st.markdown("This plot shows the relationship between self-reported sleep quality and academic performance.")

# Prepare the data (same as your original crosstab)
cross_tab_perf = pd.crosstab(
    df['Sleep Quality'], 
    df['Academic Performance'], 
    normalize='index'
).reset_index()

# Melt the dataframe for Plotly Express
cross_tab_perf_melted = cross_tab_perf.melt(
    id_vars='Sleep Quality',
    value_vars=cross_tab_perf.columns[1:],
    var_name='Academic Performance Rating',
    value_name='Proportion'
)

# Define a specific order for 'Sleep Quality' for better visualization
sleep_quality_order = ['Excellent', 'Good', 'Fair', 'Poor', 'Very Poor']

# Plot using Plotly Express
fig_sleep_perf = px.bar(
    cross_tab_perf_melted,
    x='Sleep Quality',
    y='Proportion',
    color='Academic Performance Rating',
    title='Relationship between Sleep Quality and Academic Performance (Proportion)',
    labels={'Proportion': 'Proportion of Students', 'Sleep Quality': 'Sleep Quality'},
    category_orders={'Sleep Quality': sleep_quality_order},
    color_discrete_sequence=px.colors.sequential.Aggrnyl # Another color sequence
)

# Customize layout
fig_sleep_perf.update_layout(
    xaxis_title='Sleep Quality',
    yaxis_title='Proportion',
    legend_title='Academic Performance',
    barmode='stack',
    hovermode="x unified"
)

st.plotly_chart(fig_sleep_perf, use_container_width=True)
