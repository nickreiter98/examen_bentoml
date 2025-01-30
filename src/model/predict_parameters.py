import json
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

def predict_params(repo_path):
    X_train_scaled = pd.read_csv(f'{repo_path}/data/processed/X_train_scaled.csv', index_col=0)
    y_train = pd.read_csv(f'{repo_path}/data/processed/y_train.csv', index_col=0)

    model = RandomForestRegressor()
    param_grid = {
        'n_estimators': np.arange(10, 15),
        'max_depth': np.arange(5, 10, 1),
        'min_samples_split': np.arange(2, 10, 2),
        'min_samples_leaf': np.arange(1, 10, 2),
    }

    grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, scoring='neg_mean_squared_error')
    grid_search.fit(X_train_scaled, y_train)

    best_params = grid_search.best_params_
    best_params = {k: int(v) for k, v in best_params.items()}
    with open(f'{repo_path}/models/parameters.json', 'w') as f:
        json.dump(best_params, f)


if __name__ == "__main__":
    repo_path = os.getcwd()
    predict_params(repo_path)