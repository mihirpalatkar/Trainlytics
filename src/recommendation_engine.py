import pandas as pd
from datetime import datetime, timedelta
from data_processor import (
    calculate_window_success,
    minutes_to_time
)
def get_reliability(consistency):

    if consistency <15:
        return "Excellent"
    elif consistency <30:
        return "Good"
    elif consistency <60:
        return "Average"
    else:
        return "Poor"
def get_confidence(records):

    if records >= 16:
        return "High (Strong historical evidence)"

    elif records >= 8:
        return "Medium (Moderate historical evidence)"

    else:
        return "Low (Limited historical data)"

def recommend_train(df, destination, day, start_time, end_time):

    filtered = df[(df["Destination"] == destination) & (df["day"] == day)]
    if filtered.empty:
        return None, {
            "error": "No trains found for the selected destination and day."
        }
    results = []

    for train in filtered["train_name"].unique():
        train_data = filtered[filtered["train_name"] == train]
        window_success = calculate_window_success(train_data, start_time, end_time)
        consistency = train_data["arrival_minutes"].std()
        records = len(train_data)
        avg_arrival = minutes_to_time(train_data["arrival_minutes"].mean())
        results.append([train, window_success, consistency, records, avg_arrival])
    recommendation_df = pd.DataFrame(results, columns=["train_name", "window_success", "consistency", "records", "avg_arrival"])
    recommendation_df = recommendation_df.sort_values(by=["window_success", "consistency"],ascending=[False, True])
    best_train = recommendation_df.iloc[0]
    train_name = best_train["train_name"]

    train_data = df[
    df["train_name"] == train_name]
    scheduled_arrival = (
    train_data["sched_arr"]
    .iloc[0])

    avg_arrival_delay = (
    train_data["delay_min"]
    .mean())
    expected_arrival = (
    datetime.combine(
        datetime.today(),
        scheduled_arrival
    )
    +
    timedelta(minutes=avg_arrival_delay)).time()

    scheduled_departure = (
    train_data["sched_dep_ngp"]
    .iloc[0])

    avg_departure_delay = (
    train_data["departure_delay"]
    .mean())

    expected_departure = (
    datetime.combine(
        datetime.today(),
        scheduled_departure
    )
    +
    timedelta(minutes=avg_departure_delay)).time()
    top_3 = recommendation_df[
    recommendation_df["window_success"] >= 50].head(3)
    top_3["reliability"] = (
    top_3["consistency"]
    .apply(get_reliability))

    alternatives = top_3.iloc[1:]

    alternative_list = []

    for _, row in alternatives.iterrows():

        alternative_list.append({
        "train_name": row["train_name"],
        "arrival": row["avg_arrival"],
        "reliability": row["reliability"],
        "window_success": float(
            round(row["window_success"], 2)
        )
        })

    reliability = get_reliability(best_train["consistency"])
    confidence = get_confidence(best_train["records"])

    recommendation = {

    "train_name": best_train["train_name"],

    "scheduled_departure":
        scheduled_departure.strftime("%H:%M"),

    "expected_departure":
        expected_departure.strftime("%H:%M"),

    "scheduled_arrival":
        scheduled_arrival.strftime("%H:%M"),

    "expected_arrival":
    expected_arrival.strftime("%H:%M"),

    "typical_arrival_delay":
        float(round(avg_arrival_delay, 2)),

    "reliability":
        reliability,

    "window_success":
        float(round(best_train["window_success"], 2)),

    "confidence":
        confidence,

    "alternatives":
        alternative_list
}
   

    return recommendation_df, recommendation
