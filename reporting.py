# intelligent_resume_analyzer_simple/reporting.py
import streamlit as st
import pandas as pd

def visualize_skill_gap(skill_gaps):
    """Visualizes the skill gaps."""
    if skill_gaps:
        st.subheader("Key Skill Gaps")
        df = pd.DataFrame({'Skill': skill_gaps})
        st.bar_chart(df['Skill'].value_counts())
    else:
        st.info("No significant skill gaps identified.")