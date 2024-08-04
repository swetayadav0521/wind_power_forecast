# Wind Power Prediction

Predict Power based on below inputs:

- **temperature_2m** - Temperature in degrees Fahrenheit at 2 meters above the surface
- **relativehumidity_2m** - Relative humidity (as a percentage) at 2 meters above the surface
- **dewpoint_2m** - Dew point in degrees Fahrenheit at 2 meters above the surface
- **windspeed_10m** - Wind speed in meters per second at 10 meters above the surface
- **windspeed_100m** - Wind speed in meters per second at 100 meters above the surface
- **winddirection_10m** - Wind direction in degrees (0-360) at 10 meters above the surface
- **winddirection_100m** - Wind direction in degrees (0-360) at 100 meters above the surface (0-360)
- **windgusts_10m** - Wind gusts in meters per second at 100 meters above the surface
---

### Technical Concept
The system architecture consists of multiple components integrated together.
The flow starts with data capture from sensors, followed by data storage, processing, machine learning, and finally deployment and monitoring.
- **Data Capture**: Data is captured by sensors and sent to RabbitMQ for message queuing. This ensures reliable and efficient data transfer for further processing.
- **Data Storage**: Raw and processed data is stored in a data lake and cloud storage services like AWS S3 and Azure Blob Storage. This provides scalable and durable storage solutions.
- **Data Processing**: Data processing involves extracting, transforming, and loading (ETL) data. Apache Spark and PySpark are used for large-scale data processing, while pandas is used for smaller datasets and data manipulation.
- **Machine Learning**: Machine learning models are developed and trained using scikit-learn and TensorFlow. These models are used for predictions and analytics to derive insights from the data.
- **Deployment and Monitoring**: The deployment pipeline includes Docker for containerization, Jenkins for CI/CD, Terraform and Ansible for infrastructure automation, and Grafana for monitoring and visualization.

## Prerequisites

- Docker
- Docker compose

## Steps to run the application

1. Clone the Repository

```
git clone https://github.com/swetayadav0521/wind_power_forecast.git
cd DocPad

```

2. Build Docker Image

```
docker-compose build

```
3. Run Docker Container

```
docker-compose up

```

4. Open `http://localhost:8000/predict` to access application and predict wind power generated based on attributes

5. Press `CTRL+C` to quit the docker.






