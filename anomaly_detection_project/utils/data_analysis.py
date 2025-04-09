import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.limits_handler import load_limits

def get_adjusted_limits(clean_data, upper, lower, margin_ratio=0.1):
    """Limit 값이 있으면 10% margin 적용, 없으면 데이터의 최대/최소 기준으로 margin 적용"""
    min_val = clean_data.min()
    max_val = clean_data.max()

    if np.isnan(lower):
        lower = min_val
    if np.isnan(upper):
        upper = max_val

    margin = (upper - lower) * margin_ratio
    return lower - margin, upper + margin


def explore_data(df, EDA_SAVE_DIR, limits_path):
    """데이터 탐색 및 시각화 후, 개별 파일로 저장"""
    
    # Limit 값 불러오기
    upper_limits, lower_limits = load_limits(limits_path)
    
    print("\n🔍 데이터 기본 정보:")
    print(df.info())

    print("\n🔍 결측값 확인:")
    print(df.isnull().sum())

    if not os.path.exists(EDA_SAVE_DIR):
        os.makedirs(EDA_SAVE_DIR)

    # ✅ 히스토그램 저장
    for col in df.select_dtypes(include=['number']).columns:
        clean_data = df[col].dropna()  # NaN 제거
        if clean_data.empty:  # 값이 하나도 없으면 스킵
            print(f"⚠️ {col} 컬럼은 모든 값이 NaN이므로 그래프를 건너뜀")
            continue

        # Limit 값 가져오기
        upper = upper_limits.get(col, np.nan)
        lower = lower_limits.get(col, np.nan)

        # x축 범위 자동 조정
        x_min, x_max = get_adjusted_limits(clean_data, upper, lower)

        plt.figure(figsize=(6, 4))
        plt.hist(clean_data, bins=50, color='skyblue', edgecolor='black')
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.xlim(x_min, x_max)  # x축 범위 조정

        # limit 값이 존재하면 점선 추가
        if not np.isnan(upper):
            plt.axvline(upper, color="red", linestyle="dashed", label=f"Upper: {upper}")
        if not np.isnan(lower):
            plt.axvline(lower, color="blue", linestyle="dashed", label=f"Lower: {lower}")

        plt.legend()

        save_path = os.path.join(EDA_SAVE_DIR, f"histogram_{col}.png")
        plt.savefig(save_path)
        plt.close()
        print(f"✅ 히스토그램 저장 완료: {save_path}")
        

    # ✅ 박스 플롯 저장
    for col in df.select_dtypes(include=['number']).columns:
        clean_data = df[col].dropna()  # NaN 제거
        if clean_data.empty:  # 값이 하나도 없으면 스킵
            print(f"⚠️ {col} 컬럼은 모든 값이 NaN이므로 그래프를 건너뜀")
            continue
        
        # Limit 값 가져오기
        upper = upper_limits.get(col, np.nan)
        lower = lower_limits.get(col, np.nan)

        # y축 범위 자동 조정
        y_min, y_max = get_adjusted_limits(clean_data, upper, lower)

        plt.figure(figsize=(6, 4))
        sns.boxplot(y=clean_data, color="lightcoral")
        plt.title(f"Boxplot of {col}")
        plt.ylim(y_min, y_max)  # y축 범위 조정

        # limit 값이 존재하면 점선 추가
        if not np.isnan(upper):
            plt.axhline(upper, color="red", linestyle="dashed", label=f"Upper: {upper}")
        if not np.isnan(lower):
            plt.axhline(lower, color="blue", linestyle="dashed", label=f"Lower: {lower}")

        plt.legend()

        save_path = os.path.join(EDA_SAVE_DIR, f"boxplot_{col}.png")
        plt.savefig(save_path)
        plt.close()
        print(f"✅ 박스 플롯 저장 완료: {save_path}")

