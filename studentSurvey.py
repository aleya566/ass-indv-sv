import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(
    page_title="Student Sleep and Educational Outcomes Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    """Loads the dataset from the URL."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset_version-2.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Streamlit App Title and Introduction ---
st.title("📊 Student Sleep and Educational Outcomes Analysis")
st.markdown("""
This application visualizes key sleep and stress factors among students,
exploring their distribution across different years of study and genders,
and their relationship with academic performance.
""")

st.markdown("---")

# --- Display Data Section ---
if st.checkbox("Show Raw Data Sample", False):
    st.subheader("Data Preview")
    st.dataframe(df.head())
    st.info(f"The dataset has **{len(df)}** rows and **{len(df.columns)}** columns.")

st.markdown("---")

# --- 1. Stacked Bar Chart – Stress Levels by Year of Study (Plotly Express) ---
st.header("1. Academic Stress Levels by Year of Study")
st.markdown("""
This plot shows the **proportion of students** in each **year of study** who reported different levels of academic stress.
""")

# Crosstab equivalent for Plotly
stress_year_crosstab = pd.crosstab(
    df['1. What is your year of study?'],
    df['14. How would you describe your stress levels related to academic workload?'],
    normalize='index'
).mul(100).round(2).stack().reset_index(name='Proportion (%)')
stress_year_crosstab.columns = ['Year of Study', 'Stress Level', 'Proportion (%)']

# Define the order for better visualization
stress_order = ['Extremely Low', 'Low', 'Moderate', 'High', 'Extremely High']

# Create the Plotly figure (Stacked Bar Chart)
fig_stress_year = px.bar(
    stress_year_crosstab,
    x='Year of Study',
    y='Proportion (%)',
    color='Stress Level',
    title='Academic Stress Levels by Year of Study',
    labels={'Year of Study': 'Year of Study', 'Proportion (%)': 'Proportion (%)'},
    category_orders={"Stress Level": stress_order},
    color_discrete_sequence=px.colors.sequential.Flare_r # Reverse Flare for a similar feel to 'flare'
)

# Customize the layout
fig_stress_year.update_layout(
    xaxis={'tickangle': 45},
    legend_title_text='Stress Level',
    bargap=0.1
)

st.plotly_chart(fig_stress_year, use_container_width=True)

st.markdown("---")

# --- 2. Box Plot – Sleep Hours by Gender (Plotly Express) ---
st.header("2. Average Sleep Hours by Gender")
st.markdown("""
This **box plot** visualizes the **distribution** of average sleep hours for male and female students,
showing median, quartiles, and outliers.
""")

# Rename columns for simpler plotting
df_sleep_gender = df.rename(columns={
    '2. What is your gender?': 'Gender',
    '4. On average, how many hours of sleep do you get on a typical day?': 'Average Sleep Hours'
})

# Create the Plotly figure (Box Plot)
fig_sleep_gender = px.box(
    df_sleep_gender,
    x='Gender',
    y='Average Sleep Hours',
    color='Gender',
    title='Average Sleep Hours by Gender',
    category_orders={"Gender": ['Male', 'Female']},
    color_discrete_sequence=px.colors.sequential.Plotly3 # Using a suitable Plotly sequence
)

# Customize the layout
fig_sleep_gender.update_traces(boxpoints='all', jitter=0.3, pointpos=-1.8) # Show all points as well
fig_sleep_gender.update_layout(
    xaxis_title='Gender',
    yaxis_title='Average Sleep Hours',
    showlegend=False
)

st.plotly_chart(fig_sleep_gender, use_container_width=True)

st.markdown("---")

# --- 3. Stacked Bar Chart - Sleep Quality vs Academic Performance (Plotly Express) ---
st.header("3. Relationship between Sleep Quality and Academic Performance")
st.markdown("""
This plot shows the **relationship** between self-reported **sleep quality** and **academic performance**.
""")

# Crosstab equivalent for Plotly
cross_tab_perf = pd.crosstab(
    df['6. How would you rate the overall quality of your sleep?'],
    df['15. How would you rate your overall academic performance (GPA or grades) in the past semester?'],
    normalize='index'
).mul(100).round(2).stack().reset_index(name='Proportion (%)')
cross_tab_perf.columns = ['Sleep Quality', 'Academic Performance', 'Proportion (%)']

# Define the order for better visualization
sleep_quality_order = ['Very Poor', 'Poor', 'Neutral', 'Good', 'Very Good']
performance_order = ['Poor', 'Fair', 'Good', 'Excellent']

# Create the Plotly figure (Stacked Bar Chart)
fig_sleep_perf = px.bar(
    cross_tab_perf,
    x='Sleep Quality',
    y='Proportion (%)',
    color='Academic Performance',
    title='Relationship between Sleep Quality and Academic Performance',
    labels={'Sleep Quality': 'Sleep Quality', 'Proportion (%)': 'Proportion (%)'},
    category_orders={
        "Sleep Quality": sleep_quality_order,
        "Academic Performance": performance_order
    },
    color_discrete_sequence=px.colors.sequential.Plasma # Another suitable sequential colormap
)

# Customize the layout
fig_sleep_perf.update_layout(
    xaxis={'tickangle': 45},
    legend_title_text='Academic Performance',
    bargap=0.1
)

st.plotly_chart(fig_sleep_perf, use_container_width=True)

st.markdown("---")
st.caption("Data source: Publicly available student survey dataset.")
