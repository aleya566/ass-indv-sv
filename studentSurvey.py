import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration for Streamlit Page ---
st.set_page_config(
    page_title="Sleep Quality vs. Academic Performance",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
@st.cache_data # Cache the data to prevent re-downloading on every rerun
def load_data():
    """Loads the dataset from the URL."""
    url = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset_version-2.csv'
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

df = load_data()

# --- Application Title and Description ---
st.title("📊 Sleep Quality vs. Academic Performance Analysis")
st.markdown("This application visualizes the relationship between self-rated sleep quality and academic performance using a stacked bar chart powered by **Plotly**.")

# Check if data was loaded successfully
if df.empty:
    st.warning("Could not load the dataset. Please check the URL and internet connection.")
else:
    # --- Display Data Head (Optional, but useful) ---
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # --- Data Preparation for Plotly (Crosstab equivalent) ---
    # Define column names based on your original script
    sleep_quality_col = '6. How would you rate the overall quality of your sleep?'
    academic_performance_col = '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'

    # 1. Calculate the frequency (crosstab)
    cross_tab_counts = pd.crosstab(
        df[sleep_quality_col], 
        df[academic_performance_col]
    )
    
    # 2. Convert to proportions normalized by 'Sleep Quality' (index)
    cross_tab_proportion = cross_tab_counts.div(cross_tab_counts.sum(axis=1), axis=0).mul(100)
    
    # 3. Reset index and melt the DataFrame for Plotly compatibility
    plot_df = cross_tab_proportion.reset_index().melt(
        id_vars=sleep_quality_col, 
        var_name='Academic Performance', 
        value_name='Proportion (%)'
    )

    # Sort the dataframe by the sleep quality column to ensure a logical order in the plot
    # Assuming 'Poor', 'Fair', 'Good', 'Excellent' is the desired order.
    # You might need to adjust this list based on the actual unique values in your dataset.
    sleep_order = ['Poor', 'Fair', 'Good', 'Excellent'] # Example order
    # Filter for values present in the data and sort
    present_order = [quality for quality in sleep_order if quality in plot_df[sleep_quality_col].unique()]
    plot_df[sleep_quality_col] = pd.Categorical(plot_df[sleep_quality_col], categories=present_order, ordered=True)
    plot_df = plot_df.sort_values(sleep_quality_col)


    # --- Plotly Visualization ---
    st.subheader("Stacked Bar Chart: Sleep Quality vs. Academic Performance")

    fig = px.bar(
        plot_df,
        x=sleep_quality_col,
        y='Proportion (%)',
        color='Academic Performance',
        title='Relationship between Sleep Quality and Academic Performance (Proportion of each Academic Rating within each Sleep Quality Category)',
        labels={
            sleep_quality_col: 'Sleep Quality',
            'Proportion (%)': 'Proportion of Students (%)'
        },
        barmode='stack', # This ensures a stacked bar chart
        color_discrete_sequence=px.colors.qualitative.Vivid # Use a visually distinct color scale
    )
    
    # Customize the layout for better readability and presentation
    fig.update_layout(
        xaxis_title="Overall Quality of Sleep",
        yaxis_title="Proportion of Students (%)",
        legend_title="Academic Performance",
        # Optionally, ensure y-axis goes up to 100 for proportions
        yaxis=dict(range=[0, 100]), 
        hovermode="x unified" # Nice interactive feature for Plotly
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # --- Explanation ---
    st.markdown("""
    ---
    ### Interpretation
    Each bar represents a category of **Sleep Quality**. The segments within each bar show the **proportion** of students in that sleep quality group who reported a specific **Academic Performance** rating.
    This chart is **interactive**:
    * **Hover** over the bars to see exact proportions.
    * **Click** on legend items to hide/show specific academic performance categories.
    * **Zoom** and **Pan** the chart using the tools on the top-right.
    """)

# --- To Run the App ---
# 1. Save the code above as a Python file (e.g., app.py).
# 2. Run it from your terminal using: streamlit run app.py
