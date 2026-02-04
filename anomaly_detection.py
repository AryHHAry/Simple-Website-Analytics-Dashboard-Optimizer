import numpy as np
from sklearn.linear_model import LinearRegression

def predict_trends(data_values):
    """
    Dummy predict trend: Linear regression on visitor count.
    """
    if len(data_values) < 2:
        return data_values[-1] if len(data_values) > 0 else 0
    
    X = np.arange(len(data_values)).reshape(-1, 1)
    y = np.array(data_values)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next value
    next_idx = np.array([[len(data_values)]])
    prediction = model.predict(next_idx)[0]
    
    # Simple anomaly flag: if actual > pred + 2 sigma
    std_dev = np.std(y)
    actual_last = data_values[-1]
    is_anomaly = actual_last > (prediction + 2 * std_dev) or actual_last < (prediction - 2 * std_dev)
    
    return float(prediction), bool(is_anomaly)

def calculate_confidence_interval(data_values):
    """
    Calculate +/- 10% based on data variation.
    """
    mean_val = np.mean(data_values)
    std_val = np.std(data_values)
    # Return as percentage or range
    return mean_val * 0.1 # +/- 10% estimation
