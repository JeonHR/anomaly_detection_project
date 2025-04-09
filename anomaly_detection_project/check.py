import os
import pandas as pd
from utils.data_loader import load_data
from utils.data_analysis import explore_data
from utils.anomaly_detection import detect_anomalies
from utils.evaluate_anomalies import analyze_anomalies
from utils.commonality_analysis import analyze_site_commonality

# ✅ 데이터 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "tester_data.CSV")
EDA_SAVE_DIR = os.path.join(BASE_DIR, "eda_plots")
LIMITS_PATH = os.path.join(BASE_DIR, "data", "limits.json")
SAVE_DIR = os.path.join(BASE_DIR, "anomaly_plots")
EVALU_DIR = os.path.join(BASE_DIR, "evaluation_reports")

# ✅ 데이터 로드 및 전처리
df, upper_limits, lower_limits = load_data(DATA_PATH)

df, anomalies,anomaly_counts_df = detect_anomalies(df,LIMITS_PATH,SAVE_DIR)
analyze_anomalies(df, anomalies,anomaly_counts_df,EVALU_DIR)
analyze_site_commonality(df, anomalies,  site_col="Site", EVALU_DIR=EVALU_DIR)

print("finish")
