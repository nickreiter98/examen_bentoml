import pickle
import os
import bentoml
import json
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_model(repo_path):
    X_test_scaled = pd.read_csv(f'{repo_path}/data/processed/X_test_scaled.csv', index_col=0)
    y_test = pd.read_csv(f'{repo_path}/data/processed/y_test.csv', index_col=0)

    model = bentoml.sklearn.load_model('uni_acceptance_lr:latest')

    y_pred = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        'MSE': str(mse),
        'MAE': str(mae),
        'r2': str(r2)
    }

    print(f"Model Performance Metrics: MSE={mse:.3f}, MAE={mae:.3f}, R2={r2:.3f}")

    

if __name__ == "__main__":
    repo_path = os.getcwd()
    evaluate_model(repo_path)