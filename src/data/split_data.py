import pandas as pd
import os
from sklearn.model_selection import train_test_split
from pathlib import Path

def split_data(repo_path):
    df = pd.read_csv(f'{repo_path}/data/raw/admission.csv', index_col=0)

    X = df.drop('Chance of Admit', axis=1)
    y = df['Chance of Admit']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train.to_csv(f'{repo_path}/data/processed/X_train.csv')
    X_test.to_csv(f'{repo_path}/data/processed/X_test.csv')
    y_train.to_csv(f'{repo_path}/data/processed/y_train.csv')
    y_test.to_csv(f'{repo_path}/data/processed/y_test.csv')
    

if __name__ == "__main__":
    repo_path = os.getcwd()
    split_data(repo_path)
