# objective_3.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Column definitions and mappings ---
COL_ACADEMIC_PERF_CAT = '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
COL_ASSIGNMENT_IMPACT = '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?'
COL_CONCENTRATION_CAT = '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?'
COL_FATIGUE_CAT = '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?'

COL_ACADEMIC_PERF_NUM = 'Academic_Performance_Numeric'
COL_CONCENTRATION_NUM = 'Concentration_Difficulty_Numeric'
COL_FATIGUE_NUM = 'Fatigue_Frequency_Numeric'

ACADEMIC_PERF_MAP = {'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5}
CONCENTRATION_MAP = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}
FATIGUE_MAP = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}


# --- Data Loading and Preprocessing (CORRECTED) ---
@st.cache_data
def load_data():
    """Loads and preprocesses the dataset."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    try:
        df = pd.read_csv(url)

        # 🚨 FIX: Using df.rename() prevents the Length Mismatch error
        df.rename(columns={
            COL_ACADEMIC_PERF_CAT: 'Academic_Performance',
            COL_ASSIGNMENT_IMPACT: 'Assignment_Impact',
            COL_CONCENTRATION_CAT: 'Concentration_Difficulty',
            COL_FATIGUE_CAT: 'Fatigue_Frequency',
        }, inplace=True)
        
        # Map categorical to numerical for plotting
        df[COL_ACADEMIC_PERF_NUM] = df['Academic_Performance'].map(ACADEMIC_PERF_MAP)
        df[COL_CONCENTRATION_NUM] = df['Concentration_Difficulty'].map(CONCENTRATION_MAP)
        df[COL_FATIGUE_NUM] = df['Fatigue_Frequency'].map(FATIGUE_MAP)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def app():
    df = load_data()
    
    st.title('Objective 3: Impact of Sleep Issues on Concentration, Fatigue, and Performance')
    st.markdown("Investigating the impact of sleep-related issues on student concentration, fatigue levels and academic performance.")

    if df.empty:
        return

    # 1. Box Plot: Academic Performance by Impact on Assignment Completion
    st.subheader("Academic Performance by Impact of Insufficient Sleep on Assignments")

    assignment_impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']

    fig_boxplot = px.box(
        df, x='Assignment_Impact', y=COL_ACADEMIC_PERF_NUM, color='Assignment_Impact',
        category_orders={'Assignment_Impact': assignment_impact_order},
        labels={'Assignment_Impact': 'Impact of Insufficient Sleep on Assignments', COL_ACADEMIC_PERF_NUM: 'Academic Performance (Numeric Score)'},
        color_discrete_sequence=px.colors.sequential.Agsunset, height=550
    )

    fig_boxplot.update_xaxes(tickangle=45)
    fig_boxplot.update_yaxes(tickvals=list(ACADEMIC_PERF_MAP.values()), ticktext=list(ACADEMIC_PERF_MAP.keys()))
    
    st.plotly_chart(fig_boxplot, use_container_width=True)

    # 2. Heatmap: Average Academic Performance by Concentration Difficulty and Fatigue
    st.subheader("Average Academic Performance by Fatigue and Concentration Difficulty")

    heatmap_data_performance = df.pivot_table(
        index=COL_CONCENTRATION_NUM, columns=COL_FATIGUE_NUM,
        values=COL_ACADEMIC_PERF_NUM, aggfunc='mean'
    )

    concentration_order = list(CONCENTRATION_MAP.values())
    fatigue_order = list(FATIGUE_MAP.values())
    heatmap_data_performance = heatmap_data_performance.reindex(concentration_order).T.reindex(fatigue_order).T

    x_labels = list(FATIGUE_MAP.keys())
    y_labels = list(CONCENTRATION_MAP.keys())

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data_performance.values, x=x_labels, y=y_labels,
        colorscale=px.colors.sequential.Plasma_r, zmin=1, zmax=5
    ))

    annotations = []
    for i, row in enumerate(heatmap_data_performance.values):
        for j, val in enumerate(row):
            if not pd.isna(val):
                annotations.append(go.layout.Annotation(
                    x=x_labels[j], y=y_labels[i], text=f"{val:.2f}", showarrow=False,
                    font=dict(color="black" if val > 4 else "white")
                ))

    fig_heatmap.update_layout(
        xaxis_title='Fatigue Frequency', yaxis_title='Difficulty Concentrating Frequency',
        annotations=annotations, height=600, xaxis=dict(tickangle=45),
        yaxis=dict(categoryorder='array', categoryarray=y_labels[::-1]) 
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # 3. Violin Plot - Academic Performance by Difficulty Concentrating
    st.subheader("Distribution of Academic Performance by Difficulty Concentrating Frequency")

    concentration_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']

    fig_violin = px.violin(
        df, x='Concentration_Difficulty', y=COL_ACADEMIC_PERF_NUM, color='Concentration_Difficulty',
        box=True, points="outliers",
        category_orders={'Concentration_Difficulty': concentration_order},
        labels={'Concentration_Difficulty': 'Difficulty Concentrating Frequency', COL_ACADEMIC_PERF_NUM: 'Academic Performance (Numeric Score)'},
        color_discrete_sequence=px.colors.qualitative.Set1, height=550
    )

    fig_violin.update_xaxes(tickangle=45)
    fig_violin.update_yaxes(tickvals=list(ACADEMIC_PERF_MAP.values()), ticktext=list(ACADEMIC_PERF_MAP.keys()))

    st.plotly_chart(fig_violin, use_container_width=True)

app()
