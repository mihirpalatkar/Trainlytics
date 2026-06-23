import pandas as pd

def minutes_to_time(minutes):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"

def filter_day_destination(df, day, destination):

    filtered = df[
        (df["day"] == day)
        &
        (df["Destination"] == destination)
    ]

    return filtered

def calculate_window_success(data, start_time, end_time):

    print("CALCULATE_WINDOW_SUCCESS RUNNING")

    print(type(data["actual_arr"].iloc[0]))
    print(data["actual_arr"].head())

    within_window = (
        (data["actual_arr"] >= start_time)
        &
        (data["actual_arr"] <= end_time)
    )

    return within_window.mean() * 100