# main_app.py
import streamlit as st

st.set_page_config(
    page_title="Student Sleep and Outcomes Dashboard",
    layout="wide"
)

# ----------------------------------------------------
# Define the pages using the names of the objective files
# ----------------------------------------------------

# Objective 1: Sleep, Stress, and Outcomes (from your first request)
objective_1 = st.Page('objective_1.py', 
                      title='Objective 1: Sleep, Stress & Outcomes', 
                      icon=":material/stacked_bar_chart:")

# Objective 2: Lifestyle Behaviors vs. Sleep Quality (from your second request)
objective_2 = st.Page('objective_2.py', 
                      title='Objective 2: Lifestyle & Sleep Quality', 
                      icon=":material/heatmap:")

# Objective 3: Sleep Issues Impact (from your third request)
objective_3 = st.Page('objective_3.py', 
                      title='Objective 3: Sleep Issues Impact', 
                      icon=":material/bar_chart_4_bars:",
                      default=True) # Set this as the default page

# ----------------------------------------------------
# Create the navigation menu
# ----------------------------------------------------
pg = st.navigation(
    {
        "Analysis Objectives": [objective_1, objective_2, objective_3]
    }
)

# Run the application
pg.run()
