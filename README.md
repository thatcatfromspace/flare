# Flare Driver Acceptance & Scoring System

This project predicts driver acceptance for deliveries and ranks drivers using a modular machine learning pipeline. It includes data preprocessing, model training, scoring algorithms, and sample data for simulation.

## Features

- Logistic regression model for driver acceptance prediction
- Modular scoring algorithm for ranking drivers
- Integration with HERE Traffic and OpenWeather APIs
- Sample data for Orlando, FL and Austin, TX
- Extensible for new features and vehicle types

## Project Structure

```
clients/           # API clients for traffic and weather
model/             # Model training, features, and artifacts
sample_data/       # Example driver and delivery data
score/             # Scoring and ranking algorithms
tests/             # Unit tests
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd flare
```

### 2. Create a Virtual Environment (Recommended)

```sh
python -m venv venv
.\venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

#### Example `requirements.txt` (create this file if missing):

```
pandas
numpy
scikit-learn
geopy
joblib
python-dotenv
```

### 4. Prepare Data

- Place your driver acceptance dataset as `model/driver_acceptance_dataset.csv`.
- Adjust sample data in `sample_data/` as needed.

### 5. Train the Model

```sh
python model/model.py
```

This will train the logistic regression model and export the feature order for scoring.

### 6. Run Scoring Algorithm

```sh
python score/scoring_algorithm.py
```

This will simulate driver ranking and acceptance prediction using the sample data.

### 7. Environment Variables

- Set your HERE and OpenWeather API keys in a `.env` file:

```
HERE_API_KEY=your_here_api_key
OPEN_WEATHER_API_KEY=your_openweather_api_key
```

## Testing

Add or run tests in the `tests/` directory as needed.

## Notes

- Ensure the feature order in `model/model_features.json` matches between model training and scoring.
- Update vehicle types in both model training and scoring if new types are added.

## License

MIT License
