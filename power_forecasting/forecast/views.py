import logging
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from .tasks import train_model, make_prediction

# Configure logging
logger = logging.getLogger(__name__)

def predict_from_file_view(request):
    context = {}
    if request.method == 'POST':
        try:
            # Handle file upload
            data_file = request.FILES['data_file']
            df = pd.read_csv(data_file)
            logger.info("File uploaded and read successfully")

            # Ensure the uploaded file contains the required columns
            required_columns = ['temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 
                                'windspeed_10m', 'windspeed_100m', 'winddirection_10m', 
                                'winddirection_100m', 'windgusts_10m']
            if not all(column in df.columns for column in required_columns):
                raise ValueError("Uploaded file is missing required columns")
            # Check for missing values
            if df[required_columns].isnull().values.any():
                raise ValueError("Uploaded file contains NaN values")

            # Ensure the data types are correct
            df[required_columns] = df[required_columns].astype(float)
            logger.info("Input data validated and converted to correct types")
            
            # Make predictions
            predictions = make_prediction(df[required_columns])
            if predictions is None:
                raise ValueError("Prediction failed")

            # Add predictions to the DataFrame
            df['Predicted Power [kW]'] = predictions
            logger.info("Predictions added to DataFrame")
            
            df = df.drop(['Power'], axis=1)

            # Convert DataFrame to dictionary for rendering in template
            results = df.to_dict(orient='records')
            logger.info("Results prepared for rendering")

            context = {'results': results}
            return render(request, 'forecast/results.html', context)
        
        except Exception as e:
            logger.error("An error occurred while processing the file: %s", str(e))
            context = {'error': 'An error occurred during file processing or prediction.'}
    
    return render(request, 'forecast/predict.html', context)


def train_model_view(request):
    try:
        # Trigger model training task
        train_model.delay()
        logger.info("Model training task triggered.")
        
        context = {'message': 'Model training started!'}
    
    except Exception as e:
        logger.error("An error occurred while triggering the model training task: %s", str(e))
        context = {'error': 'An error occurred while starting the model training.'}
    return render(request, 'forecast/train_model.html', context)

