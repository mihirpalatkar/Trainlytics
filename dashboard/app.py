import streamlit as st
import pandas as pd
from datetime import date
import sys
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
def train_model(df):

    train_encoder = LabelEncoder()
    day_encoder = LabelEncoder()
    destination_encoder = LabelEncoder()

    df["train_encoded"] = train_encoder.fit_transform(
        df["train_name"]
    )

    df["day_encoded"] = day_encoder.fit_transform(
        df["day"]
    )

    df["destination_encoded"] = destination_encoder.fit_transform(
        df["Destination"]
    )
    

    X = df[
        [
            "train_encoded",
            "day_encoded",
            "destination_encoded"
        ]
    ]

    y = df["delay_min"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return (
        model,
        train_encoder,
        day_encoder,
        destination_encoder
    )


def predict_delay(
    model,
    train_encoder,
    day_encoder,
    destination_encoder,
    train_name,
    day,
    destination
):

    train_encoded = (
        list(train_encoder.classes_)
        .index(train_name)
    )

    day_encoded = (
        list(day_encoder.classes_)
        .index(day)
    )

    destination_encoded = (
        list(destination_encoder.classes_)
        .index(destination)
    )

    X_new = pd.DataFrame(
        {
            "train_encoded": [
                train_encoded
            ],
            "day_encoded": [
                day_encoded
            ],
            "destination_encoded": [
                destination_encoded
            ]
        }
    )

    prediction = model.predict(
        X_new
    )[0]

    return prediction

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

#PAGE

st.set_page_config(
    page_title="Trainlytics",
    page_icon="🚆",
    layout="wide"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

#DATA

df = pd.read_excel("data/train_data.xlsx")

def time_to_minutes(t):
    return t.hour * 60 + t.minute
def minutes_to_clock(minutes):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"
def get_reliability(delay):

    if delay < 15:
        return "Excellent"

    elif delay < 30:
        return "Good"

    elif delay < 60:
        return "Average"

    else:
        return "Poor"

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.day_name()

df["arrival_minutes"] = (
    df["actual_arr"].apply(time_to_minutes)
)

df["departure_delay"] = (
    df["actual_dep_ngp"].apply(time_to_minutes)
    -
    df["sched_dep_ngp"].apply(time_to_minutes)
)

df["delay_min"] = (
    df["actual_arr"].apply(time_to_minutes)
    -
    df["sched_arr"].apply(time_to_minutes)
)
(
    model,
    train_encoder,
    day_encoder,
    destination_encoder
) = train_model(df)
st.success("ML Model Loaded Successfully ")

#UI

st.title("🚆 TRAINLYTICS")

st.caption(
    "Train Recommendation & Reliability Analytics"
)

st.divider()

#JOURNEY

col1, col2 = st.columns(2)

with col1:
    destination = st.selectbox(
        "Destination",
        ["Wardha", "Sewagram"]
    )

with col2:
    journey_date = st.date_input(
        "Journey Date",
        value=date.today()
    )

day = pd.Timestamp(journey_date).day_name()

st.write(f"Selected Day: **{day}**")

st.divider()

#ARRIVAL WINDOW

col3, col4 = st.columns(2)

with col3:
    start_window = st.selectbox(
        "Arrival Window Start",
        [
            "08:00",
            "08:30",
            "09:00",
            "09:30",
            "10:00",
            "10:30",
            "11:00"
        ]
    )

with col4:
    end_window = st.selectbox(
        "Arrival Window End",
        [
            "09:00",
            "09:30",
            "10:00",
            "10:30",
            "11:00",
            "11:30",
            "12:00",
            "12:30",
            "13:00"
        ]
    )

start_time = pd.to_datetime(start_window).time()
end_time = pd.to_datetime(end_window).time()

#FIND TRAIN

if st.button(
    "FIND BEST TRAIN",
    use_container_width=True
):
    st.success("Recommendation generated successfully!")

    filtered = df[
        (df["Destination"] == destination)
        &
        (df["day"] == day)
    ]

    if filtered.empty:

        st.error(
            "No train data found for selected day."
        )

    else:

        results = []

        start_minutes = (
            start_time.hour * 60
            +
            start_time.minute
        )

        end_minutes = (
            end_time.hour * 60
            +
            end_time.minute
        )

        for train in filtered["train_name"].unique():

            train_data = filtered[
                filtered["train_name"] == train
            ]

            within_window = (
                (
                    train_data["arrival_minutes"]
                    >= start_minutes
                )
                &
                (
                    train_data["arrival_minutes"]
                    <= end_minutes
                )
            )

            success_rate = (
                within_window.mean() * 100
            )

            avg_delay = (
                train_data["delay_min"]
                .mean()
            )

            avg_arrival_minutes = (
                train_data["arrival_minutes"]
                .mean()
            )

            typical_arrival = (
                minutes_to_clock(
                    avg_arrival_minutes
                )
            )


            results.append(
                [
                    train,
                    typical_arrival,
                    success_rate,
                    avg_delay,
                ]
            )

        recommendation_df = pd.DataFrame(
            results,
            columns=[
                "train",
                "typical_arrival",
                "success_rate",
                "avg_delay"
            ]
        )
        recommendation_df = recommendation_df[
            [
                "train",
                "typical_arrival",
                "success_rate",
                "avg_delay"
            ]
        ]
        recommendation_df = (
            recommendation_df
            .sort_values(
                by=[
                    "success_rate",
                    "avg_delay"
                ],  
                ascending=[
                    False,
                    True
                ]
            )
        )

        best_train = recommendation_df.iloc[0]


    #TRAIN DETAILS 

        best_train_name = best_train["train"]
        predicted_delay = predict_delay(
            model,
            train_encoder,
            day_encoder,
            destination_encoder,
            best_train_name,
            day,
            destination
        )

        confidence = max(
            50,
            100 - predicted_delay
        )
        if predicted_delay <= 10:
            reliability = "Excellent"
        elif predicted_delay <= 25:
            reliability = "Good"
        elif predicted_delay <= 45:
            reliability = "Average"
        else:
            reliability = "Poor"

        train_data = filtered[
            filtered["train_name"] == best_train_name
        ]

        scheduled_departure = (
            train_data["sched_dep_ngp"]
            .iloc[0]
        )

        scheduled_arrival = (
            train_data["sched_arr"]
            .iloc[0]
        )

        avg_departure_delay = (
            train_data["departure_delay"]
            .mean()
        )

        avg_arrival_delay = predicted_delay

        scheduled_dep_minutes = (
            time_to_minutes(scheduled_departure)
        )

        scheduled_arr_minutes = (
            time_to_minutes(scheduled_arrival)
        )

        expected_dep_minutes = (
            scheduled_dep_minutes
            + avg_departure_delay
        )

        expected_arr_minutes = (
            scheduled_arr_minutes
            + avg_arrival_delay
        )

    #RECOMMENDED TRAIN 

        st.divider()

        st.subheader("🏆 Recommended Train")
        st.markdown(f"## {best_train_name}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Scheduled Departure",
                scheduled_departure.strftime("%H:%M")
            )

            st.metric(
                "Expected Departure",
                minutes_to_clock(expected_dep_minutes)
            )

        with col2:
            st.metric(
                "Scheduled Arrival",
                scheduled_arrival.strftime("%H:%M")
            )

            st.metric(
                "Expected Arrival",
                minutes_to_clock(expected_arr_minutes)
            )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Reliability",
                reliability
            )

        with col2:
            st.metric(
                "Window Success",
                f"{best_train['success_rate']:.0f}%"
            )

        with col3:
            st.metric(
                "ML Predicted Delay",
                f"{predicted_delay:.0f} min"
            )
        with col4:
            st.metric(
                "Prediction Confidence",
                f"{confidence:.0f}%"
            )
        st.divider()

        st.subheader("📌 Journey Insights")

        insight_1 = (
            f"{best_train_name} reaches "
            f"{destination} within your selected window "
            f"{best_train['success_rate']:.0f}% of the time."
        )

        insight_2 = (
            f"ML predicts a delay of "
            f"{predicted_delay:.0f} minutes."
        )

        insight_3 = (
            f"Expected arrival time is "
            f"{minutes_to_clock(expected_arr_minutes)}."
        )

        st.info(insight_1)
        st.info(insight_2)
        st.info(insight_3)

    #ALTERNATIVE TRAINS 

        st.divider()

        st.subheader("🚆 Alternative Trains")
        alternatives = recommendation_df.iloc[1:4]

        if alternatives.empty:
            st.info("No alternative trains available.")
        else:
            cols = st.columns(len(alternatives))

            for i, (_, row) in enumerate(alternatives.iterrows()):

                alt_train_data = filtered[
                    filtered["train_name"] == row["train"]
                ]

                avg_arrival_minutes = (
                    alt_train_data["arrival_minutes"]
                    .mean()
                )

                typical_arrival = (
                    minutes_to_clock(
                        avg_arrival_minutes
                )
                )

                with cols[i]:

                    st.markdown(
                        f"###  {row['train']}"
                    )

                    st.metric(
                        "Typical Arrival Time",
                        typical_arrival
                    )

                    st.caption(
                        f"Window Success: {row['success_rate']:.0f}%"
                    )

                    st.caption(
                        f"Delay: {row['avg_delay']:.0f} min"
                    )

    #RANKINGS 

        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Trains",
                df["train_name"].nunique()
            )

        with col2:
            st.metric(
                "Historical Records",
                len(df)
            )

        with col3:
            st.metric(
                "Destinations",
                df["Destination"].nunique()
            )

        st.divider()

        st.subheader("📊 Train Rankings")

        table_df = recommendation_df.copy()
        table_df["reliability"] = (
            table_df["avg_delay"]
            .apply(get_reliability)
        )

        table_df = table_df.reset_index(
            drop=True
        )
        table_df.index = table_df.index + 1

        table_df.columns = [
            "Train",
            "Typical Arrival",
            "Success Rate (%)",
            "Average Delay (min)",
            "Reliability"
        ]

        st.dataframe(
            table_df,
            use_container_width=True
        )
        st.subheader("📈 Train Success Comparison")

        chart_df = recommendation_df.copy()

        chart_df = chart_df.sort_values(
            by="success_rate",
            ascending=False
        )

        st.bar_chart(
            chart_df.set_index("train")[
                "success_rate"
            ]
        )
        st.divider()

        st.subheader("📅 Average Delay by Day")

        day_delay = (
            df.groupby("day")["delay_min"]
            .mean()
            .reset_index()
        )

        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        day_delay["day"] = pd.Categorical(
            day_delay["day"],
            categories=day_order,
            ordered=True
        )

        day_delay = day_delay.sort_values("day")

        st.bar_chart(
            day_delay.set_index("day")[
                "delay_min"
            ]
        )
st.divider()

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #7f8c8d;
        font-size: 13px;
        padding: 10px;
        background-color: #0E1117;
        border-top: 1px solid rgba(255,255,255,0.08);
        z-index: 999;
    }
    </style>

    <div class="footer">
        Trainlytics © 2026 • Developed by Mihir Palatkar
    </div>
    """,
    unsafe_allow_html=True
)