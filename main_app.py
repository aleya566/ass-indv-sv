
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Student Insomnia & Educational Outcomes", layout="wide")

DATA_PATH = "Student Insomnia and Educational Outcomes Dataset.csv"

@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load dataset. Make sure '{DATA_PATH}' is in the same folder as this app. Error: {e}")
    st.stop()

# Column short-hand mapping for easier usage
col_year = "1. What is your year of study?"
col_gender = "2. What is your gender?"
col_difficulty_sleep = "3. How often do you have difficulty falling asleep at night? "
col_sleep_hours = "4. On average, how many hours of sleep do you get on a typical day?"
col_wake_trouble = "5. How often do you wake up during the night and have trouble falling back asleep?"
col_sleep_quality = "6. How would you rate the overall quality of your sleep?"
col_concentration = "7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?"
col_fatigue = "8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?"
col_miss_classes = "9. How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?"
col_assignments = "10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?"
col_device = "11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?"
col_caffeine = "12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?"
col_activity = "13. How often do you engage in physical activity or exercise?"
col_stress = "14. How would you describe your stress levels related to academic workload?"
col_gpa = "15. How would you rate your overall academic performance (GPA or grades) in the past semester?"

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Objective 1", "Objective 2", "Objective 3"])

def home_page():
    st.title("Student Insomnia & Educational Outcomes — Visualisation")
    st.markdown("""
This interactive Streamlit app reproduces the visualisations developed for the JIE42303 assignment.
The app uses interactive Plotly charts and contains three objective pages:
- Objective 1: Distribution of sleep & stress factors by year & gender.
- Objective 2: Relationship between lifestyle behaviours (caffeine, activity, device usage) and sleep quality.
- Objective 3: Impact of sleep issues on concentration, fatigue and academic performance.
""")
    st.subheader("Dataset preview")
    st.dataframe(df.head(10))
    st.subheader("Dataset columns and basic info")
    info_col1, info_col2 = st.columns([2,1])
    with info_col1:
        st.write("Columns:")
        for c in df.columns:
            st.write(f"- {c}")
    with info_col2:
        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])
        st.write("Dtypes:")
        st.write(df.dtypes.astype(str))
    st.markdown("---")
    st.write("If any visualization is blank, it likely means that column values are missing or not in an expected numeric format. I prepared the app to handle non-numeric responses gracefully where possible.")

def objective1():
    st.header("Objective 1 — Distribution of key sleep and stress factors by year & gender")
    st.markdown("**Objective:** Explore the distribution of key sleep and stress factors among students across different years of study and genders.")
    st.markdown("### Summary (automatic)")
    # Automatic summary: show counts by year and gender, average sleep hours by year
    try:
        counts_by_year = df[col_year].value_counts().sort_index()
        counts_by_gender = df[col_gender].value_counts()
        mean_sleep_by_year = df.groupby(col_year)[col_sleep_hours].agg(lambda x: pd.to_numeric(x, errors='coerce').mean())
    except Exception as e:
        st.write("Unable to compute summaries due to column format. Error:", e)
        counts_by_year = pd.Series()
        counts_by_gender = pd.Series()
        mean_sleep_by_year = pd.Series()

    st.write("- Respondents by year (counts):")
    st.write(counts_by_year)
    st.write("- Respondents by gender (counts):")
    st.write(counts_by_gender)
    st.write("- Average reported sleep hours by year:")
    st.write(mean_sleep_by_year.round(2))

    st.markdown("### Visualisations")

    # Viz 1: Stacked bar of stress levels by year (normalized)
    if col_year in df.columns and col_stress in df.columns:
        cros = pd.crosstab(df[col_year], df[col_stress], normalize='index')
        cros = cros.reset_index().melt(id_vars=col_year, var_name="Stress Level", value_name="Proportion")
        fig1 = px.bar(cros, x=col_year, y="Proportion", color="Stress Level", title="Stress Levels by Year (proportion)", labels={col_year:"Year of study"})
        fig1.update_layout(barmode='stack', legend_title_text='Stress level')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Stress by year plot not available (missing columns).")

    # Viz 2: Distribution of sleep hours by gender (histogram)
    if col_sleep_hours in df.columns and col_gender in df.columns:
        # convert to numeric if possible
        df['_sleep_hours_num'] = pd.to_numeric(df[col_sleep_hours], errors='coerce')
        fig2 = px.histogram(df, x='_sleep_hours_num', color=col_gender, nbins=20, barmode='overlay', title='Distribution of Sleep Hours by Gender', labels={'_sleep_hours_num':'Sleep hours (avg)'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sleep hours by gender plot not available (missing columns).")

    # Viz 3: Violin plot of sleep quality by year
    if col_sleep_quality in df.columns and col_year in df.columns:
        # attempt to coerce sleep quality to numeric where applicable
        try:
            df['_sleep_quality_num'] = pd.to_numeric(df[col_sleep_quality], errors='coerce')
            fig3 = px.violin(df, x=col_year, y='_sleep_quality_num', box=True, points='all', title='Sleep Quality by Year (numeric where available)', labels={'_sleep_quality_num':'Sleep quality'})
            st.plotly_chart(fig3, use_container_width=True)
        except Exception:
            st.info("Could not create violin plot for sleep quality (non-numeric responses).")
    else:
        st.info("Sleep quality by year plot not available (missing columns).")

    st.markdown("### Interpretation")
    st.write("Use the plots above to evaluate whether certain years report systematically higher stress or lower sleep quality. For example, higher proportions of 'High' stress in final-year students or lower average sleep hours for certain gender groups would suggest targeted interventions.")

def objective2():
    st.header("Objective 2 — Lifestyle behaviours vs sleep quality")
    st.markdown("**Objective:** Analyze the relationship between student lifestyle behaviors (caffeine consumption, physical activity, and device usage) and overall sleep quality.")
    st.markdown("### Summary (automatic)")
    try:
        avg_caffeine = pd.to_numeric(df[col_caffeine], errors='coerce').mean()
        avg_device = pd.to_numeric(df[col_device], errors='coerce').mean()
        avg_activity = pd.to_numeric(df[col_activity], errors='coerce').mean()
        avg_sleep_quality = pd.to_numeric(df[col_sleep_quality], errors='coerce').mean()
    except Exception as e:
        st.write("Unable to compute numeric averages automatically:", e)
        avg_caffeine = avg_device = avg_activity = avg_sleep_quality = np.nan

    st.write(f"- Average caffeine frequency (encoded): {np.round(avg_caffeine,2)} (depends on encoding in survey)")
    st.write(f"- Average device usage frequency (encoded): {np.round(avg_device,2)}")
    st.write(f"- Average physical activity frequency (encoded): {np.round(avg_activity,2)}")
    st.write(f"- Average sleep quality (encoded): {np.round(avg_sleep_quality,2)}")

    st.markdown("### Visualisations")

    # Viz 1: Scatter caffeine vs sleep quality (with trendline)
    if col_caffeine in df.columns and col_sleep_quality in df.columns:
        df['_caffeine_num'] = pd.to_numeric(df[col_caffeine], errors='coerce')
        df['_sleep_quality_num2'] = pd.to_numeric(df[col_sleep_quality], errors='coerce')
        fig1 = px.scatter(df, x='_caffeine_num', y='_sleep_quality_num2', color=col_gender if col_gender in df.columns else None,
                          trendline='ols', title='Caffeine (frequency) vs Sleep Quality (encoded)',
                          labels={'_caffeine_num':'Caffeine (encoded)','_sleep_quality_num2':'Sleep quality (encoded)'})
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Caffeine vs sleep quality plot not available (missing columns).")

    # Viz 2: Boxplot of sleep hours by physical activity level (binned)
    if col_activity in df.columns and col_sleep_hours in df.columns:
        df['_activity_num'] = pd.to_numeric(df[col_activity], errors='coerce')
        df['_sleep_hours_num2'] = pd.to_numeric(df[col_sleep_hours], errors='coerce')
        # Create bins for activity frequency
        try:
            bins = pd.qcut(df['_activity_num'].fillna(0)+1, q=4, duplicates='drop')
            fig2 = px.box(df, x=bins.astype(str), y='_sleep_hours_num2', points="all", title="Sleep Hours by Physical Activity (binned)",
                          labels={'x':'Physical activity (binned)','_sleep_hours_num2':'Sleep hours'})
            st.plotly_chart(fig2, use_container_width=True)
        except Exception:
            st.info("Could not bin physical activity for boxplot (possibly non-numeric responses).")
    else:
        st.info("Physical activity vs sleep hours plot not available (missing columns).")

    # Viz 3: Correlation heatmap among lifestyle and sleep numeric columns
    cols = []
    for c in [col_caffeine, col_activity, col_device, col_sleep_hours, col_sleep_quality]:
        if c in df.columns:
            cols.append(c)
    if len(cols) >= 2:
        numeric_df = df[cols].apply(pd.to_numeric, errors='coerce')
        corr = numeric_df.corr()
        fig3 = px.imshow(corr, text_auto=True, title="Correlation matrix (lifestyle & sleep numeric encodings)")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Not enough numeric columns found for correlation heatmap.")

    st.markdown("### Interpretation")
    st.write("Check the scatter and heatmap for evidence that higher caffeine use or device usage is associated with worse sleep quality (higher encoded values may represent more frequent use). Depending on the survey coding, look for positive correlations between device/caffeine and poor sleep quality and negative correlation between physical activity and poor sleep outcomes.")

def objective3():
    st.header("Objective 3 — Impact of sleep issues on concentration, fatigue and academic performance")
    st.markdown("**Objective:** Investigate the impact of sleep-related issues on students' concentration, fatigue levels and academic performance.")
    st.markdown("### Summary (automatic)")
    try:
        conc_counts = df[col_concentration].value_counts()
        fatigue_counts = df[col_fatigue].value_counts()
        gpa_numeric = pd.to_numeric(df[col_gpa], errors='coerce')
    except Exception as e:
        st.write("Unable to create summary automatically:", e)
        conc_counts = fatigue_counts = pd.Series()
        gpa_numeric = pd.Series(dtype=float)

    st.write("- Concentration difficulty counts:")
    st.write(conc_counts)
    st.write("- Fatigue counts:")
    st.write(fatigue_counts)
    st.write(f"- Mean GPA (where numeric): {np.round(gpa_numeric.mean(),2)}")

    st.markdown("### Visualisations")

    # Viz 1: Bar chart showing concentration frequency by presence of severe sleep difficulty (use difficulty_sleep)
    if col_difficulty_sleep in df.columns and col_concentration in df.columns:
        cros = pd.crosstab(df[col_difficulty_sleep], df[col_concentration], normalize='index')
        cros = cros.reset_index().melt(id_vars=col_difficulty_sleep, var_name='Concentration difficulty', value_name='Proportion')
        fig1 = px.bar(cros, x=col_difficulty_sleep, y='Proportion', color='Concentration difficulty', title='Concentration difficulty by frequency of falling asleep problems')
        fig1.update_layout(barmode='stack')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Concentration vs difficulty falling asleep plot not available (missing columns).")

    # Viz 2: Scatter sleep hours vs GPA
    if col_sleep_hours in df.columns and col_gpa in df.columns:
        df['_sleep_hours_num3'] = pd.to_numeric(df[col_sleep_hours], errors='coerce')
        df['_gpa_num'] = pd.to_numeric(df[col_gpa], errors='coerce')
        fig2 = px.scatter(df, x='_sleep_hours_num3', y='_gpa_num', trendline='ols', title='Sleep Hours vs GPA (numeric where available)',
                          labels={'_sleep_hours_num3':'Sleep hours','_gpa_num':'GPA'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sleep hours vs GPA plot not available (missing columns).")

    # Viz 3: Stacked bar of fatigue level by year
    if col_fatigue in df.columns and col_year in df.columns:
        cros2 = pd.crosstab(df[col_year], df[col_fatigue], normalize='index')
        cros2 = cros2.reset_index().melt(id_vars=col_year, var_name='Fatigue level', value_name='Proportion')
        fig3 = px.bar(cros2, x=col_year, y='Proportion', color='Fatigue level', title='Fatigue levels by Year (proportion)')
        fig3.update_layout(barmode='stack')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Fatigue by year plot not available (missing columns).")

    st.markdown("### Interpretation")
    st.write("Investigate whether participants who report frequent sleep onset difficulty also report more concentration problems, higher fatigue, and lower GPA (if numeric GPA values are available). Use scatter trendline and stacked proportions to support conclusions.")

# Page routing
if page == "Home":
    home_page()
elif page == "Objective 1":
    objective1()
elif page == "Objective 2":
    objective2()
elif page == "Objective 3":
    objective3()
