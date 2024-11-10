import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_paddy_classifier():
    # Sample training data
    # Features: [NDVI, EVI, NDWI, LSWI]
    X = np.array([
        [0.8, 0.7, 0.2, 0.3],  # Mature paddy
        [0.7, 0.6, 0.3, 0.4],  # Reproductive stage
        [0.4, 0.3, 0.5, 0.6],  # Early growth
        [0.2, 0.1, 0.7, 0.8],  # Flooding stage
        # ... more training examples ...
    ])
    
    # Labels: Growth stages
    y = np.array([
        'mature',
        'reproductive',
        'early_growth',
        'flooding'
    ])
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and train the Random Forest model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    return model

def predict_growth_stage(model, ndvi, evi, ndwi, lswi):
    """
    Predict paddy growth stage using trained model
    """
    features = np.array([[ndvi, evi, ndwi, lswi]])
    prediction = model.predict(features)
    return prediction[0]

# Example usage
if __name__ == "__main__":
    # Train model
    model = train_paddy_classifier()
    
    # Example prediction
    sample_values = {
        'ndvi': 0.75,
        'evi': 0.65,
        'ndwi': 0.25,
        'lswi': 0.35
    }
    
    stage = predict_growth_stage(
        model,
        sample_values['ndvi'],
        sample_values['evi'],
        sample_values['ndwi'],
        sample_values['lswi']
    )
    
    print(f"Predicted Growth Stage: {stage}")