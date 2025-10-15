import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Lifestyle & Screen Time Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("data.csv")

gender_map = {1: "Female", 2: "Male"}
occupation_map = {1: "Employed", 2: "Student", 3: "Self-employed", 4: "Unemployed", 5: "Retired"}
work_mode_map = {1: "Remote", 2: "Hybrid", 3: "In-person"}
sleep_quality_map = {1: "Very Poor", 2: "Poor", 3: "Good", 4: "Excellent"}

df["gender"] = df["gender"].map(gender_map)
df["occupation"] = df["occupation"].map(occupation_map)
df["work_mode"] = df["work_mode"].map(work_mode_map)
df["sleep_quality_1_5"] = df["sleep_quality_1_5"].map(sleep_quality_map)

df["screen_time_hours"] = df["screen_time_hours"].round(2)
df["sleep_hours"] = df["sleep_hours"].round(2)
df["stress_level_0_10"] = df["stress_level_0_10"].round(2)
df["work_screen_hours"] = df["work_screen_hours"].round(2)
df["leisure_screen_hours"] = df["leisure_screen_hours"].round(2)

avg_work_screen = round(df["work_screen_hours"].mean(), 2)
avg_leisure_screen = round(df["leisure_screen_hours"].mean(), 2)
avg_sleep_quality_score = round(df["sleep_quality_1_5"].replace(
    {"Very Poor": 1, "Poor": 2, "Good": 3, "Excellent": 4}
).mean(), 2)
avg_stress = round(df["stress_level_0_10"].mean(), 2)
avg_total_screen = round(df["screen_time_hours"].mean(), 2)


st.title("Lifestyle & Screen Time Dashboard")
st.markdown("Analyze how **screen time**, **sleep**, and **stress** are connected in daily life.")
st.markdown("---")


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Avg Work Screen Time", f"{avg_work_screen:.2f} hrs")
kpi2.metric("Avg Leisure Screen Time", f"{avg_leisure_screen:.2f} hrs")
kpi3.metric("Avg Sleep Quality (1–4)", f"{avg_sleep_quality_score:.2f}")
kpi4.metric("Avg Stress Level", f"{avg_stress:.2f}")
kpi5.metric("Avg Total Screen Time", f"{avg_total_screen:.2f} hrs")

st.markdown("---")


fig1 = px.bar(
    df.groupby("occupation", as_index=False)["sleep_hours"].mean(),
    x="occupation",
    y="sleep_hours",
    color="occupation",
    title="Average Sleeping Hours by Occupation",
    text_auto=".2f"
)

fig2 = px.bar(
    df.groupby("work_mode", as_index=False)["sleep_hours"].mean(),
    x="work_mode",
    y="sleep_hours",
    color="work_mode",
    title="Average Sleeping Hours by Work Mode",
    text_auto=".2f"
)

fig3 = px.box(
    df,
    x="sleep_quality_1_5",
    y="screen_time_hours",
    color="sleep_quality_1_5",
    title="Screen Time Distribution by Sleep Quality",
)
fig3.update_traces(hovertemplate="Sleep Quality: %{x}<br>Screen Time: %{y:.2f} hrs")

fig4 = px.scatter(
    df,
    x="screen_time_hours",
    y="stress_level_0_10",
    color="sleep_quality_1_5",
    size="sleep_hours",
    hover_data={
        "occupation": True,
        "work_mode": True,
        "screen_time_hours": ":.2f",
        "stress_level_0_10": ":.2f",
        "sleep_hours": ":.2f"
    },
    title="Screen Time vs Stress Level",
)
fig4.update_traces(hovertemplate="Screen Time: %{x:.2f} hrs<br>Stress Level: %{y:.2f}<br>Sleep Hours: %{marker.size:.2f}")


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(
        """
        **Insight:**  
        People with **better sleep quality** spend **less time on screens**.  
        Heavy screen users often report **poor sleep**.
        """
    )

with col2:
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown(
        """
        **Insight:**  
        Higher **screen time** is clearly linked to **higher stress levels**.  
        Users with **excellent sleep** tend to report **lower stress**.
        """
    )

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        """
        **Insight:**  
        People across all occupations sleep roughly **7 hours on average**.  
        **Unemployed and retired** individuals tend to sleep slightly more than others.
        """
    )

with col4:
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        """
        **Insight:**  
        Sleep time is almost the same for all work modes.  
        **In-person workers** sleep a little more, while **remote workers** sleep slightly less.
        """
    )



st.markdown("---")
st.subheader("📊 Overall Report Summary")
st.markdown(
    """
    ### Key Observations:
    - Most people get around **7 hours of sleep**, which is healthy.  
    - **Job type** and **work mode** only make a small difference in sleep time.  
    - There’s a **negative link** between **screen time and sleep quality** —  
      more screen time usually means poorer sleep.  
    - **Stress levels** go up when **screen time** increases.  
      Good sleep and balanced screen use can help reduce stress.

    ### Lifestyle Tips:
    - Try to use screens less, especially before sleeping, to sleep better.  
    - Take small breaks from screens to reduce stress and eye tiredness.  
    - Remote or hybrid workers should keep a regular sleep routine.  
    - Add offline activities or exercise to keep life balanced.

    ---
    **Final Note:**  
    A good balance between **screen time, sleep, and stress control**  
    helps improve your overall health and daily life.
    """
)
