# objective_1.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading and Preprocessing (Common to all files) ---
@st.cache_data
def load_data():
    """Loads and preprocesses the dataset."""
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
        # Convert to numeric for box plot
        df['Avg_Sleep_Hours'] = pd.to_numeric(df['Avg_Sleep_Hours'], errors='coerce')
        return df.dropna(subset=['Avg_Sleep_Hours']) # Drop rows where sleep hours is not convertible
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def app():
    df = load_data()
    
    st.title('Objective 1: Sleep, Stress, and Educational Outcomes')
    st.markdown("Exploring the distribution of key sleep and stress factors among students.")

    if df.empty:
        return

    # 1. Stacked Bar Chart – Academic Stress Levels by Year of Study
    st.subheader("Academic Stress Levels by Year of Study")
    
    stress_year_crosstab = pd.crosstab(df['Year_of_Study'], df['Academic_Stress_Level'], normalize='index').reset_index()
    stress_year_crosstab_melt = stress_year_crosstab.melt(
        id_vars=['Year_of_Study'], var_name='Stress Level', value_name='Proportion'
    )
    
    stress_levels_order = sorted(df['Academic_Stress_Level'].unique(), key=lambda x: ['Low', 'Moderate', 'High', 'Very High'].index(x) if x in ['Low', 'Moderate', 'High', 'Very High'] else 99)
    colors = px.colors.qualitative.Plotly[:len(stress_levels_order)] 

    fig_stress = go.Figure()
    for i, level in enumerate(stress_levels_order):
        subset = stress_year_crosstab_melt[stress_year_crosstab_melt['Stress Level'] == level]
        fig_stress.add_trace(go.Bar(
            x=subset['Year_of_Study'], y=subset['Proportion'], name=level, marker_color=colors[i]
        ))

    fig_stress.update_layout(barmode='stack', xaxis_title='Year of Study', yaxis_title='Proportion', legend_title='Stress Level', height=500)
    st.plotly_chart(fig_stress, use_container_width=True)

    # 2. Box Plot – Average Sleep Hours by Gender
    st.subheader("Average Sleep Hours by Gender")
    
    gender_order = ['Male', 'Female']
    df_clean_sleep = df.copy()
    df_clean_sleep['Gender'] = pd.Categorical(df_clean_sleep['Gender'], categories=gender_order, ordered=True)
    df_clean_sleep.sort_values('Gender', inplace=True)
    
    fig_sleep = px.box(
        df_clean_sleep, x='Gender', y='Avg_Sleep_Hours', color='Gender',
        category_orders={"Gender": gender_order},
        labels={'Avg_Sleep_Hours': 'Average Sleep Hours', 'Gender': 'Gender'},
        color_discrete_sequence=px.colors.sequential.Agsunset, height=500
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

    # 3. Stacked Bar Chart - Sleep Quality vs Academic Performance
    st.subheader("Relationship between Sleep Quality and Academic Performance")
    
    cross_tab_perf = pd.crosstab(df['Sleep_Quality'], df['Academic_Performance'], normalize='index').reset_index()
    cross_tab_perf_melt = cross_tab_perf.melt(
        id_vars=['Sleep_Quality'], var_name='Academic Performance', value_name='Proportion'
    )

    performance_levels_order = ['Poor', 'Fair', 'Good', 'Excellent']
    performance_levels_present = [level for level in performance_levels_order if level in df['Academic_Performance'].unique()]
    colors_perf = px.colors.qualitative.Vivid[:len(performance_levels_present)]
    sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']

    fig_perf = go.Figure()
    for i, level in enumerate(performance_levels_present):
        subset = cross_tab_perf_melt[cross_tab_perf_melt['Academic Performance'] == level]
        fig_perf.add_trace(go.Bar(x=subset['Sleep_Quality'], y=subset['Proportion'], name=level, marker_color=colors_perf[i]))
        
    fig_perf.update_layout(
        barmode='stack', xaxis_title='Sleep Quality', yaxis_title='Proportion', legend_title='Academic Performance',
        xaxis={'categoryorder': 'array', 'categoryarray': sleep_quality_order}, height=500
    )
    st.plotly_chart(fig_perf, use_container_width=True)

app()
