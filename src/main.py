import pandas as pd

from src.recommendation_engine import recommend_train

# Load data
df = pd.read_excel("data/train_data.xlsx")

df["actual_arr"] = pd.to_datetime(
    df["actual_arr"],
    format="%H:%M:%S"
)

df["actual_dep_ngp"] = pd.to_datetime(
    df["actual_dep_ngp"],
    format="%H:%M:%S"
)

df["sched_dep_ngp"] = pd.to_datetime(
    df["sched_dep_ngp"],
    format="%H:%M:%S"
)

df["sched_arr"] = pd.to_datetime(
    df["sched_arr"],
    format="%H:%M:%S"
)
# Preprocessing
df["day"] = pd.to_datetime(
    df["date"]
).dt.day_name()

df["arrival_minutes"] = (
    df["actual_arr"].dt.hour * 60
    +
    df["actual_arr"].dt.minute
)

df["departure_delay"] = (
    (
        df["actual_dep_ngp"].dt.hour * 60
        +
        df["actual_dep_ngp"].dt.minute
    )
    -
    (
        df["sched_dep_ngp"].dt.hour * 60
        +
        df["sched_dep_ngp"].dt.minute
    )
)
df["delay_min"] = (
    (
        df["actual_arr"].dt.hour * 60
        +
        df["actual_arr"].dt.minute
    )
    -
    (
        df["sched_arr"].dt.hour * 60
        +
        df["sched_arr"].dt.minute
    )
)

# Run engine
recommendation_df, recommendation = recommend_train(
    df,
    "Wardha",
    "Monday",
    pd.to_datetime("09:30").time(),
    pd.to_datetime("11:30").time()
)

print(recommendation)