import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

def normalize_data(repo_path):
    X_train = pd.read_csv(f'{repo_path}/data/processed/X_train.csv', index_col=0)
    X_test = pd.read_csv(f'{repo_path}/data/processed/X_test.csv', index_col=0)

    scaler = MinMaxScaler()
    normalized_X_train = pd.DataFrame(
        scaler.fit_transform(X_train), columns=X_train.columns
    )
    normalized_X_test = pd.DataFrame(
        scaler.fit_transform(X_test), columns=X_test.columns
    )

    normalized_X_train.to_csv(f'{repo_path}/data/processed/X_train_scaled.csv')
    normalized_X_test.to_csv(f'{repo_path}/data/processed/X_test_scaled.csv')

    

if __name__ == "__main__":
    repo_path = os.getcwd()
    normalize_data(repo_path)