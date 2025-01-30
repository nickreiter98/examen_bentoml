import pickle
import json
import bentoml
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor

def train_model(repo_path):
    X_train_scaled = pd.read_csv(f'{repo_path}/data/processed/X_train_scaled.csv', index_col=0)
    y_train = pd.read_csv(f'{repo_path}/data/processed/y_train.csv', index_col=0)

    with open(f'{repo_path}/models/parameters.json', 'rb') as file:
        params = json.load(file)

    model = RandomForestRegressor(**params)
    model.fit(X_train_scaled, y_train)
    
    model_ref = bentoml.sklearn.save_model("uni_acceptance_lr", model)
    print(f"Model saved as: {model_ref}")

if __name__ == "__main__":
    repo_path = os.getcwd()
    train_model(repo_path)