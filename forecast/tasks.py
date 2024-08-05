import logging
from celery import shared_task
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

# Configure logging
logger = logging.getLogger(__name__)


@shared_task
def train_model():
    try:
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), "data", "Training_data.csv")
        df = pd.read_csv(data_path)
        logger.info("Data loaded successfully from %s", data_path)

        # Prepare the features and target variable
        features = [
            "temperature_2m",
            "relativehumidity_2m",
            "dewpoint_2m",
            "windspeed_10m",
            "windspeed_100m",
            "winddirection_10m",
            "winddirection_100m",
            "windgusts_10m",
        ]
        target = "Power"

        X = df[features]
        y = df[target]
        logger.info("Features and target variable prepared.")

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )
        logger.info("Data split into training and test sets.")

        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        logger.info("Model trained successfully.")

        # Save model
        model_path = os.path.join(
            os.path.dirname(__file__), "models", "wind_power_model.pkl"
        )
        joblib.dump(model, model_path)
        logger.info("Model saved successfully to %s", model_path)

        return "Model trained and saved successfully!"

    except Exception as e:
        logger.error("An error occurred during model training or saving: %s", str(e))
        return "An error occurred during model training or saving."


@shared_task
def make_prediction(data):
    try:
        # Load models
        model_path = os.path.join(
            os.path.dirname(__file__), "models", "wind_power_model.pkl"
        )
        wind_power_model = joblib.load(model_path)
        logger.info("Model loaded successfully from %s", model_path)

        # Prepare data for prediction
        prediction_data = pd.DataFrame(data)
        logger.info("Data prepared for prediction: %s", data)

        # Make prediction
        predicted_power = wind_power_model.predict(prediction_data)
        formatted_predictions = [round(pred, 4) for pred in predicted_power]
        logger.info("Prediction made successfully: %s", formatted_predictions)

        return formatted_predictions

    except Exception as e:
        logger.error("An error occurred during prediction: %s", str(e))
        return {"error": "An error occurred during prediction."}
