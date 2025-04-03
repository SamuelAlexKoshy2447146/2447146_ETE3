import streamlit as st
from random import randint, choice
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# Generate dataset with 10 relevant columns of 300 participants over 5 days, covering 10 sports events and feedback text from each particiant
def generate_sports_data(
    num_participants=300,
    num_days=5,
    output_file="sports_event_feedback.csv",
):
    sports_events = [
        "Football",
        "Basketball",
        "Tennis",
        "Swimming",
        "Running",
        "Badminton",
        "Cycling",
        "Volleyball",
        "Table Tennis",
        "Archery",
    ]
    genders = ["Male", "Female", "Other"]
    colleges = [
        ["College A", "Karnataka"],
        ["College B", "Karnataka"],
        ["College C", "Kerala"],
        ["College D", "Kerala"],
        ["College E", "Tamil Nadu"],
        ["College F", "Andhra Pradesh"],
    ]
    feedback_samples = [
        "Had a great time!",
        "Could be better organized.",
        "Loved the experience!",
        "Facilities need improvement.",
        "Amazing competition!",
        "Looking forward to next time.",
        "Would love more variety in events.",
        "Great energy and atmosphere!",
        "Well managed but could use better timing.",
        "Enjoyed every moment!",
    ]

    data = []
    for _ in range(num_participants):
        participant_id = f"P{randint(1000, 9999)}"
        name = f"Participant_{randint(1, 1000)}"
        age = randint(18, 26)
        gender = choice(genders)

        for day in range(1, num_days + 1):
            sport = choice(sports_events)
            score = randint(1, 100)
            college = choice(colleges)
            satisfaction = randint(1, 5)
            feedback = choice(feedback_samples)

            data.append(
                [
                    participant_id,
                    name,
                    age,
                    gender,
                    day,
                    sport,
                    score,
                    college[0],
                    college[1],
                    satisfaction,
                    feedback,
                ]
            )

    columns = [
        "Participant_ID",
        "Name",
        "Age",
        "Gender",
        "Day",
        "Sport Event",
        "Score",
        "College",
        "State",
        "Satisfaction_Rating",
        "Feedback",
    ]
    return pd.DataFrame(data, columns=columns)
    # data.to_csv(output_file, index=False)
    # print(f"Dataset saved to {output_file}")


# Run the function
data = generate_sports_data()

st.header("CHRISPO Event Feedback Analysis")
st.write(
    "This dashboard provides an analysis of the feedback from participants in the CHRISPO event."
)

st.write("### Dataset Overview")
st.dataframe(data)
new_data = st.button("Click to generate new data")
if new_data:
    data = generate_sports_data()

# Data Analysis
st.write("### Participation Analysis")
category_type = st.radio(
    "Select the type of analysis you want to perform:",
    (
        # "Overall Satisfaction",
        "Age Analysis",
        "College Analysis",
        "State Analysis",
        "Sports Analysis",
    ),
    horizontal=True,
)
chart_type = st.radio(
    "Select the type of chart you want to display:",
    ("Bar Chart", "Pie Chart", "Line Chart"),
    horizontal=True,
)


# Aggregating data based on the selected category
if category_type == "Age Analysis":
    aggregated_data = data["Age"].value_counts()
    label = "Age"
    print(aggregated_data)
elif category_type == "College Analysis":
    aggregated_data = data["College"].value_counts()
    label = "College"
    print(aggregated_data)
elif category_type == "State Analysis":
    aggregated_data = data["State"].value_counts()
    label = "State"
elif category_type == "Sports Analysis":
    aggregated_data = data["Sport Event"].value_counts()
    label = "Sport Event"
elif category_type == "Overall Satisfaction":
    aggregated_data = data["Satisfaction_Rating"].value_counts()
    label = "Satisfaction Rating"

# Display charts in Streamlit
if chart_type == "Bar Chart":
    st.bar_chart(
        pd.DataFrame({label: aggregated_data.index, "Count": aggregated_data.values}),
        x=label,
    )
elif chart_type == "Pie Chart":
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        aggregated_data.values,
        labels=aggregated_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Paired.colors,
    )
    ax.legend(
        wedges,
        aggregated_data.index,
        title=label,
        loc="best",
        bbox_to_anchor=(1, 0.5),
    )
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)
elif chart_type == "Line Chart":
    st.line_chart(
        pd.DataFrame({label: aggregated_data.index, "Count": aggregated_data.values}),
        x=label,
    )

st.write("### Feedback Analysis")
# Select a specific sport to analyze feedback
selected_sport = st.selectbox(
    "Select a sport to view feedback word cloud:", data["Sport Event"].unique()
)

# Filter feedback for the selected sport
sport_feedback = " ".join(data[data["Sport Event"] == selected_sport]["Feedback"])

# Generate Word Cloud
if sport_feedback.strip():  # Check if there's feedback available
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        sport_feedback
    )

    # Display the word cloud
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Hide axes
    st.pyplot(fig)
else:
    st.write("No feedback available for this sport.")
