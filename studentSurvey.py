import streamlit as st
import pandas as pd
import plotly.express as px

# Define the URL for the dataset
URL = 'https://raw.githubusercontent.com/aleya566/ass-indv-sv/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset_version-2.csv'

# --- Streamlit App Configuration and Data Loading ---

st.set_page_config(
    page_title="Sleep Quality vs. Academic Performance",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Sleep Quality and Academic Performance Analysis")

@st.cache_data
def load_data(url):
    """Loads the dataset from the specified URL."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(URL)

if not df.empty:
    st.header("Raw Data Preview")
    st.write(df.head())

    # --- Data Preparation for Plotly Visualization ---

    # Create a cross-tabulation of Sleep_Quality and Academic_Performance
    # Normalize='index' calculates the proportion of Academic_Performance for each Sleep_Quality level
    cross_tab = pd.crosstab(
        df['Sleep_Quality'],
        df['Academic_Performance'],
        normalize='index'
    )

    # Reset index to turn the index (Sleep_Quality) into a column
    # Then unpivot the DataFrame from 'wide' format to 'long' format (melt)
    # This is often the preferred format for Plotly Express
    cross_tab_df = cross_tab.reset_index()

    # The column names (Academic_Performance levels) are now the values in the variable 'Academic_Performance'
    # The proportions are in the new 'Proportion' column
    plot_df = cross_tab_df.melt(
        id_vars='Sleep_Quality',
        var_name='Academic_Performance',
        value_name='Proportion'
    )

    st.header("Stacked Bar Chart: Sleep Quality vs. Academic Performance")

    # --- Plotly Express Visualization ---

    # Create the stacked bar chart using Plotly Express
    # x: Sleep_Quality categories
    # y: Proportion (for the height of the bars)
    # color: Academic_Performance (for stacking and coloring)
    # text: The proportion value displayed on the bar segments
    # The barmode='stack' is the default for a column chart in Plotly Express, but explicitly stated for clarity.
    fig = px.bar(
        plot_df,
        x='Sleep_Quality',
        y='Proportion',
        color='Academic_Performance',
        title='Proportion of Academic Performance within each Sleep Quality Category',
        labels={
            'Sleep_Quality': 'Sleep Quality',
            'Proportion': 'Proportion of Students',
            'Academic_Performance': 'Academic Performance'
        },
        category_orders={"Sleep_Quality": sorted(plot_df['Sleep_Quality'].unique())}, # Sort the x-axis categories if needed
        # Set colors for the categories
        color_discrete_map={
            'Excellent': 'green',
            'Good': 'lightgreen',
            'Average': 'orange',
            'Poor': 'red'
        },
    )

    # Customize the layout for better readability
    fig.update_layout(
        xaxis={'title': 'Sleep Quality'},
        yaxis={
            'title': 'Proportion',
            'tickformat': '.0%', # Format y-axis ticks as percentages
        },
        legend_title_text='Academic Performance',
        hovermode="x unified"
    )

    # Optionally add text labels on the bars for the proportions
    # This requires adding the proportion to the text argument and configuring the text position
    fig.update_traces(
        texttemplate='%{y:.1%}', # Display proportion as percentage with one decimal place
        textposition='inside',
        insidetextfont={'color': 'black', 'size': 12}
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Could not load data. Please check the URL and network connection.")
