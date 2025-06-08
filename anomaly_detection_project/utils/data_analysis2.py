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

def explore_data_by_site(df, EDA_SAVE_DIR, limits_path, site_col='Site'):
    
    
    upper_limits, lower_limits = load_limits(limits_path)

    print("\n🔍 전체 데이터프레임 기본 정보:")
    print(df.info())
    print("\n🔍 전체 결측값 확인:")
    print(df.isnull().sum())

    grouped = df.groupby(site_col)

    for site, group in grouped:
        print(f"\n🚩 Site: {site} 데이터 분석 중...")
        

        for col in group.select_dtypes(include=['number']).columns:
            clean_data = group[col].dropna()
            if clean_data.empty:
                print(f"⚠️ [Site {site}] {col}: 모든 값이 NaN → 스킵")
                continue

            # === 히스토그램 ===
            upper = upper_limits.get(col, np.nan)
            lower = lower_limits.get(col, np.nan)
            x_min, x_max = get_adjusted_limits(clean_data, upper, lower)

            plt.figure(figsize=(6, 4))
            plt.hist(clean_data, bins=50, color='skyblue', edgecolor='black')
            plt.title(f"[Site {site}] Histogram of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.xlim(x_min, x_max)

            if not np.isnan(upper):
                plt.axvline(upper, color="red", linestyle="dashed", label=f"Upper: {upper}")
            if not np.isnan(lower):
                plt.axvline(lower, color="blue", linestyle="dashed", label=f"Lower: {lower}")

            plt.legend()
            hist_path = os.path.join(EDA_SAVE_DIR, f"histogram_{col}_{site}.png")
            plt.savefig(hist_path)
            plt.close()
            print(f"✅ 저장 완료: {hist_path}")

            # === 박스플롯 ===
            y_min, y_max = get_adjusted_limits(clean_data, upper, lower)
            plt.figure(figsize=(6, 4))
            sns.boxplot(y=clean_data, color="lightcoral")
            plt.title(f"[Site {site}] Boxplot of {col}")
            plt.ylim(y_min, y_max)

            if not np.isnan(upper):
                plt.axhline(upper, color="red", linestyle="dashed", label=f"Upper: {upper}")
            if not np.isnan(lower):
                plt.axhline(lower, color="blue", linestyle="dashed", label=f"Lower: {lower}")

            plt.legend()
            box_path = os.path.join(EDA_SAVE_DIR, f"boxplot_{col}_{site}.png")
            plt.savefig(box_path)
            plt.close()
            print(f"✅ 저장 완료: {box_path}")
