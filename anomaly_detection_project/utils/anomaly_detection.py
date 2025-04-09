import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.limits_handler import load_limits

def detect_anomalies(df, limits_path, save_dir="anomaly_plots", margin_ratio=0.1):
    """IQR 기반 이상값 탐지 + One-Hot Encoding 적용 + 시각화"""

    # ✅ Limit 값 로드
    upper_limits, lower_limits = load_limits(limits_path)

    # ✅ 이상값 저장할 DataFrame
    anomalies = df.copy()
    
    # ✅ 저장 폴더 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # ✅ 이상값 개수 저장할 딕셔너리
    anomaly_counts = {}

    for col in df.select_dtypes(include=["number"]).columns:

        upper = upper_limits.get(col, np.nan)
        lower = lower_limits.get(col, np.nan)

        # ✅ IQR 계산을 위한 데이터 필터링 (Limit 내 데이터만 사용)
        df_filtered = df.copy()
        if not pd.isna(lower):
            df_filtered = df_filtered[df_filtered[col] >= lower]
        if not pd.isna(upper):
            df_filtered = df_filtered[df_filtered[col] <= upper]

        # ✅ IQR 계산
        Q1 = df_filtered[col].quantile(0.25)
        Q3 = df_filtered[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # ✅ 이상값 탐지 (0 또는 1로 변환)
        anomalies[f"{col}_outlier"] = ((df[col] < lower_bound) | (df[col] > upper_bound)).astype(int)
      


        # ✅ 이상값 개수 저장
        anomaly_counts[col] = anomalies[f"{col}_outlier"].sum()

        # ✅ 이상값이 하나도 없으면 생략
        if anomaly_counts[col] == 0:
            print(f"⚠ {col}: 이상값이 없습니다. 시각화 생략합니다.")
            continue  # 🚀 이상값이 없으면 다음 컬럼으로 넘어감

        # ✅ 이상값이 하나라도 있는 경우 시각화 진행
        plt.figure(figsize=(8, 5))
        df_filtered.boxplot(column=[col])
        outliers = df[df.get(f"{col}_outlier", pd.Series(0, index=df.index)) == 1]


        plt.scatter(outliers.index, outliers[col], color="red", label="Anomalies", zorder=3)

        # ✅ Y축 범위 설정 (Limit 값 기준 확장)
        margin = margin_ratio * (upper - lower) if not pd.isna(upper) and not pd.isna(lower) else margin_ratio * df_filtered[col].std()

        if not pd.isna(lower) and not pd.isna(upper):  # ✅ 둘 다 존재할 경우
            y_min = lower - margin
            y_max = upper + margin
        elif not pd.isna(lower):  # ✅ Lower Limit만 존재
            y_min = lower - margin
            y_max = df_filtered[col].max() + margin
        elif not pd.isna(upper):  # ✅ Upper Limit만 존재
            y_min = df_filtered[col].min() - margin
            y_max = upper + margin
        else:  # ✅ Limit 값이 없을 경우
            y_min = df_filtered[col].min() - margin
            y_max = df_filtered[col].max() + margin

        # ✅ Y축 범위 적용 (유효성 체크)
        if np.isfinite(y_min) and np.isfinite(y_max) and y_min < y_max:
            plt.ylim(y_min, y_max)
        else:
            print(f"⚠ Warning: Invalid y-axis limits for column {col}. Skipping ylim setting.")

        # ✅ Limit 값이 존재하는 경우 점선 추가
        if not pd.isna(lower):
            plt.axhline(y=lower, color='red', linestyle='--', linewidth=1, label="Lower Limit")
        if not pd.isna(upper):
            plt.axhline(y=upper, color='blue', linestyle='--', linewidth=1, label="Upper Limit")

        plt.title(f"Boxplot of {col}")
        plt.legend()
        plt.savefig(os.path.join(save_dir, f"{col}_boxplot.png"))
        plt.close()
        print(f"✅ {col} 이상값 탐지 및 시각화 완료")

    print(f"✅ 이상값 시각화 저장 완료: {save_dir}")

    # ✅ 이상값 개수 CSV 저장
    anomaly_counts_df = pd.DataFrame(list(anomaly_counts.items()), columns=["Column", "Anomaly_Count"])
    anomaly_counts_df = anomaly_counts_df.set_index("Column").T  # ✅ 컬럼명을 인덱스로 설정하고 `.T` 사용하여 변환
    anomaly_counts_csv_path = os.path.join(save_dir, 'anomaly_counts.csv')
    anomaly_counts_df.to_csv(anomaly_counts_csv_path)
    anomalies.to_csv(os.path.join(save_dir, 'anomalies_with_outliers.csv'))
    
     
    print(f"✅ 이상값 개수 저장 완료: {anomaly_counts_csv_path}")

    return df, anomalies, anomaly_counts_df
