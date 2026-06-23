import pandas as pd
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

    X_new = pd.DataFrame(
        {
            st.write(train_encoder.classes_)
            st.write(train_name)
            "train_encoded": [
                train_encoder.transform(
                    [train_name]
                )[0]
            ],
            "day_encoded": [
                day_encoder.transform(
                    [day]
                )[0]
            ],
            "destination_encoded": [
                destination_encoder.transform(
                    [destination]
                )[0]
            ]
        }
    )

    prediction = model.predict(
        X_new
    )[0]

    return prediction
print("PREDICT FUNCTION FILE LOADED")
def test_function():
    return "hello"