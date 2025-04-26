import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def train_price_model(data):
    """Train a linear regression model for price prediction"""
    # Extract month and year from dates
    dates = pd.to_datetime(data["Date"])
    X = pd.DataFrame({
        'Month': dates.dt.month,
        'Year': dates.dt.year
    })
    y = data["Modal Price"]
    
    # Train the model
    model = LinearRegression()
    model.fit(X, y)
    
    return model

def predict_price(model, num_months, current_month, current_year):
    """Predict prices for the next num_months"""
    predictions = []
    
    for i in range(1, num_months + 1):
        month = (current_month + i - 1) % 12 + 1
        year_offset = (current_month + i - 1) // 12
        year = current_year + year_offset
        
        # Make prediction
        X_pred = pd.DataFrame({
            'Month': [month],
            'Year': [year]
        })
        pred_price = model.predict(X_pred)[0]
        
        # Format date for display
        date_str = f"{year}-{month:02d}-01"
        
        predictions.append((date_str, pred_price))
    
    return predictions
