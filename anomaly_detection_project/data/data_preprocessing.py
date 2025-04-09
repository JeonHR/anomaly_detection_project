import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def preprocess_data(df):
    """ 숫자형 데이터 정규화 """
    numeric_df = df.select_dtypes(include=["number"])
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)
    processed_df = pd.DataFrame(scaled_data, columns=numeric_df.columns)
    return processed_df

