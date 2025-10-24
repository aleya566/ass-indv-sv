# objective_2.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Data Loading and Preprocessing (Common to all files) ---

# Define common column names and mappings for objective 2
COL_DIFFICULTY_ASLEEP = '3. How often do you have difficulty falling asleep at night? '
COL_NIGHT_AWAKENINGS = '5. How often do you wake up during the night and have trouble falling back asleep?'
COL_SLEEP_QUALITY = '6. How would you rate the overall quality of your sleep?'
COL_DEVICE_USE = '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?'
COL_CAFFEINE_CONSUMPTION = '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?'
COL_PHYSICAL_ACTIVITY = '13. How often do you engage in physical activity or exercise?'
COL_AVG_SLEEP_HOURS = '4. On average, how many hours of sleep do you get on a typical day?'


SLEEP_HOUR_MAP = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                  '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9}
DEVICE_USE_MAP = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                  'Often (5-6 times a week)': 5.5, 'Every night': 7}
CAFFEINE_ORDER = ['Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every day']
QUALITY_ORDER = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']


@st.cache_data
def load_data():
    """Loads and preprocesses the dataset."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def app():
    df = load_data()
    
    st.title('Objective 2: Lifestyle Behaviors and Sleep Quality Analysis')
    st.markdown("Analyzing the relationship between student lifestyle behaviors (caffeine, activity, device use) and overall sleep quality.")

    if df.empty:
        return

    # 1. Correlation Heatmap – Behaviors vs Sleep Issues
    st.subheader("Correlation Matrix of Behaviors and Sleep Issues")

    behavior_sleep_df = df[[COL_DIFFICULTY_ASLEEP, COL_NIGHT_AWAKENINGS, COL_SLEEP_QUALITY,
                            COL_DEVICE_USE, COL_CAFFEINE_CONSUMPTION, COL_PHYSICAL_ACTIVITY]].copy()
    behavior_sleep_df.columns = ['Difficulty falling asleep', 'Nighttime awakenings', 'Overall sleep quality',
                                 'Electronic device use', 'Caffeine consumption', 'Physical activity']

    behavior_sleep_numeric_df = pd.DataFrame()
    for col in behavior_sleep_df.columns:
        behavior_sleep_numeric_df[col] = pd.factorize(behavior_sleep_df[col])[0]

    correlation_matrix = behavior_sleep_numeric_df.corr()

    fig_corr = px.imshow(
        correlation_matrix, text_auto=".2f", aspect="auto",
        color_continuous_scale=px.colors.sequential.Inferno,
        x=correlation_matrix.columns, y=correlation_matrix.index
    )

    fig_corr.update_layout(height=600)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # 2. Visualize Sleep Hours vs Device Use (2D Density Heatmap)
    st.subheader("Density of Observations: Average Hours of Sleep vs. Electronic Device Use Before Sleep")

    sleep_device_df = df[[COL_AVG_SLEEP_HOURS, COL_DEVICE_USE]].copy()
    sleep_device_df['Avg_Sleep_Hours_Numeric'] = sleep_device_df[COL_AVG_SLEEP_HOURS].map(SLEEP_HOUR_MAP)
    sleep_device_df['Electronic_Device_Use_Numeric'] = sleep_device_df[COL_DEVICE_USE].map(DEVICE_USE_MAP)

    heatmap_data = sleep_device_df.pivot_table(
        index='Avg_Sleep_Hours_Numeric', columns='Electronic_Device_Use_Numeric',
        aggfunc='size', fill_value=0
    )
    
    heatmap_data = heatmap_data.reindex(list(SLEEP_HOUR_MAP.values())).T.reindex(list(DEVICE_USE_MAP.values())).T.fillna(0)
    
    x_labels = list(DEVICE_USE_MAP.keys())
    y_labels = list(SLEEP_HOUR_MAP.keys())

    fig_density = go.Figure(data=go.Heatmap(
        z=heatmap_data.values, x=x_labels, y=y_labels, colorscale=px.colors.sequential.Plasma
    ))

    annotations = []
    for i, row in enumerate(heatmap_data.values):
        for j, val in enumerate(row):
            annotations.append(go.layout.Annotation(
                x=x_labels[j], y=y_labels[i], text=str(int(val)), showarrow=False,
                font=dict(color="white" if val > np.max(heatmap_data.values) / 2 else "black")
            ))

    fig_density.update_layout(
        xaxis_title='Electronic Device Use Before Sleep', yaxis_title='Average Hours of Sleep',
        annotations=annotations, height=600, xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_density, use_container_width=True)

    st.markdown("---")

    # 3. Grouped Bar Chart – Sleep Quality by Caffeine Frequency
    st.subheader("Sleep Quality Ratings by Caffeine Consumption Frequency")

    caffeine_sleep_crosstab = pd.crosstab(
        df[COL_CAFFEINE_CONSUMPTION], df[COL_SLEEP_QUALITY], normalize='index'
    ).reset_index()

    caffeine_sleep_melt = caffeine_sleep_crosstab.melt(
        id_vars=COL_CAFFEINE_CONSUMPTION, var_name='Sleep Quality', value_name='Proportion'
    )

    fig_bar = px.bar(
        caffeine_sleep_melt, x=COL_CAFFEINE_CONSUMPTION, y='Proportion', color='Sleep Quality',
        barmode='group', labels={COL_CAFFEINE_CONSUMPTION: 'Caffeine Consumption Frequency', 'Proportion': 'Proportion of Students'},
        category_orders={COL_CAFFEINE_CONSUMPTION: CAFFEINE_ORDER, "Sleep Quality": QUALITY_ORDER},
        color_discrete_sequence=px.colors.qualitative.Bold, height=550
    )

    fig_bar.update_xaxes(tickangle=45)
    st.plotly_chart(fig_bar, use_container_width=True)

app()
