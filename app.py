import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set the title and initial configuration for the Streamlit app
st.set_page_config(layout="wide")
st.title('Student Sleep, Stress, and Educational Outcomes Analysis')
st.markdown("This dashboard explores the distribution of key sleep and stress factors among students across different years of study and genders using interactive Plotly charts.")

@st.cache_data
def load_data():
    """Loads the dataset from the specified URL."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    try:
        df = pd.read_csv(url)
        # Rename long columns for easier plotting
        df.rename(columns={
            '1. What is your year of study?': 'Year_of_Study',
            '2. What is your gender?': 'Gender',
            '4. On average, how many hours of sleep do you get on a typical day?': 'Avg_Sleep_Hours',
            '6. How would you rate the overall quality of your sleep?': 'Sleep_Quality',
            '14. How would you describe your stress levels related to academic workload?': 'Academic_Stress_Level',
            '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': 'Academic_Performance'
        }, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.header("Raw Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

    ## Interactive Visualizations with Plotly

    # 1. Stacked Bar Chart – Academic Stress Levels by Year of Study
    st.header("Academic Stress Levels by Year of Study")
    st.markdown("This plot shows the proportion of students in each year of study who reported different levels of academic stress.")

    stress_year_crosstab = pd.crosstab(df['Year_of_Study'], df['Academic_Stress_Level'], normalize='index').reset_index()
    stress_year_crosstab_melt = stress_year_crosstab.melt(
        id_vars=['Year_of_Study'],
        var_name='Stress Level',
        value_name='Proportion'
    )

    # Define a color sequence
    color_sequence_stress = px.colors.sequential.Inferno
    # Use go.Bar for better control over the stacked bar chart creation, similar to the matplotlib version
    fig_stress = go.Figure()

    # Get unique stress levels for iterating and stacking
    stress_levels = df['Academic_Stress_Level'].unique()
    
    # Sort stress levels for consistent stacking (e.g., from low to high stress)
    stress_levels_order = sorted(stress_levels, key=lambda x: ['Low', 'Moderate', 'High', 'Very High'].index(x) if x in ['Low', 'Moderate', 'High', 'Very High'] else 99)
    
    colors = px.colors.qualitative.Plotly[:len(stress_levels_order)] # Using a qualitative set for distinct categories

    for i, level in enumerate(stress_levels_order):
        subset = stress_year_crosstab_melt[stress_year_crosstab_melt['Stress Level'] == level]
        fig_stress.add_trace(go.Bar(
            x=subset['Year_of_Study'],
            y=subset['Proportion'],
            name=level,
            marker_color=colors[i] # Assign a distinct color
        ))

    fig_stress.update_layout(
        barmode='stack',
        title='Academic Stress Levels by Year of Study',
        xaxis_title='Year of Study',
        yaxis_title='Proportion',
        legend_title='Stress Level',
        height=500
    )

    st.plotly_chart(fig_stress, use_container_width=True)

    st.markdown("---")

    # 2. Box Plot – Average Sleep Hours by Gender
    st.header("Average Sleep Hours by Gender")
    st.markdown("This box plot visualizes the distribution of average sleep hours for male and female students.")

    # Convert to numeric, coercing errors to NaN for cleaner visualization
    df['Avg_Sleep_Hours'] = pd.to_numeric(df['Avg_Sleep_Hours'], errors='coerce')
    df_clean_sleep = df.dropna(subset=['Avg_Sleep_Hours', 'Gender'])

    # Ensure correct order for the x-axis
    gender_order = ['Male', 'Female']
    df_clean_sleep['Gender'] = pd.Categorical(df_clean_sleep['Gender'], categories=gender_order, ordered=True)
    df_clean_sleep.sort_values('Gender', inplace=True)
    
    # Use Plotly Express for the box plot
    fig_sleep = px.box(
        df_clean_sleep,
        x='Gender',
        y='Avg_Sleep_Hours',
        color='Gender', # Color the boxes by gender
        category_orders={"Gender": gender_order},
        title='Average Sleep Hours by Gender',
        labels={'Avg_Sleep_Hours': 'Average Sleep Hours', 'Gender': 'Gender'},
        color_discrete_sequence=px.colors.sequential.Agsunset, # A palette for distinct colors
        height=500
    )

    st.plotly_chart(fig_sleep, use_container_width=True)

    st.markdown("---")

    # 3. Stacked Bar Chart - Sleep Quality vs Academic Performance
    st.header("Relationship between Sleep Quality and Academic Performance")
    st.markdown("This plot shows the relationship between self-reported sleep quality and academic performance.")

    cross_tab_perf = pd.crosstab(df['Sleep_Quality'], df['Academic_Performance'], normalize='index').reset_index()
    cross_tab_perf_melt = cross_tab_perf.melt(
        id_vars=['Sleep_Quality'],
        var_name='Academic Performance',
        value_name='Proportion'
    )

    fig_perf = go.Figure()
    
    # Define a consistent order for performance levels (e.g., from lowest to highest)
    performance_levels_order = ['Poor', 'Fair', 'Good', 'Excellent']
    
    # Filter performance levels present in the data and sort
    performance_levels_present = [level for level in performance_levels_order if level in df['Academic_Performance'].unique()]
    
    # Using a distinct color palette
    colors_perf = px.colors.qualitative.Vivid[:len(performance_levels_present)]

    for i, level in enumerate(performance_levels_present):
        subset = cross_tab_perf_melt[cross_tab_perf_melt['Academic Performance'] == level]
        fig_perf.add_trace(go.Bar(
            x=subset['Sleep_Quality'],
            y=subset['Proportion'],
            name=level,
            marker_color=colors_perf[i]
        ))
        
    # Define a consistent order for sleep quality for the x-axis
    sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']
    
    fig_perf.update_layout(
        barmode='stack',
        title='Relationship between Sleep Quality and Academic Performance',
        xaxis_title='Sleep Quality',
        yaxis_title='Proportion',
        legend_title='Academic Performance',
        xaxis={'categoryorder': 'array', 'categoryarray': sleep_quality_order}, # Set the order for the x-axis
        height=500
    )

    st.plotly_chart(fig_perf, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please check the URL and network connection.")
