import os
import pandas as pd
import numpy as np

def analyze_site_commonality(df, anomalies,  site_col="Site", EVALU_DIR="evaluation_reports"):
    """
    ✅ Site별 이상값 공통 발생 분석
    - 특정 컬럼에서 이상값(1)이 특정 Site에서 집중적으로 발생하는지 확인
    - Site별 이상값 비율 계산 후 Common Issue 여부 판단
    """

    if not os.path.exists(EVALU_DIR):
        os.makedirs(EVALU_DIR)

    # ✅ Site 컬럼이 없는 경우 예외 처리
    threshold = 5  # 특정 Site에서 이상값이 발생한 비율(%) 경고 임계값

    # ✅ 전체 샘플 수 확인
    total_samples = df.shape[0]
    if total_samples == 0:
        print("⚠️ 데이터가 없습니다. 분석을 종료합니다.")
        return

    # ✅ Site별 이상값 개수 분석
    site_report = []
    for col in anomalies.columns:
        if not col.endswith("_outlier"):  # "_outlier"가 붙은 컬럼만 분석
            continue

        original_col = col.replace("_outlier", "")  # 원래 컬럼명 복구
        if original_col not in df.columns:
            continue

        # ✅ Site별 이상값 개수 집계
        site_anomalies = anomalies[anomalies[col] == 1].groupby(site_col).size()
        
        if site_anomalies.empty:
            continue

        # ✅ 전체 Site별 데이터 개수 가져오기
        site_total_counts = df[site_col].value_counts()

        # ✅ Site별 이상값 비율 계산
        site_anomaly_ratio = (site_anomalies / site_total_counts * 100).fillna(0)
    
        # ✅ 이상값 비율이 높은 Site 탐지
        for site, ratio in site_anomaly_ratio.items():
            alert = "🔴 Common Issue Detected" if ratio >= threshold else "🟢 Normal"
            site_report.append(f"📌 컬럼: {original_col} | Site: {site}")
            site_report.append(f"   - 이상값 개수: {site_anomalies.get(site, 0)}")
            site_report.append(f"   - 해당 Site에서의 이상값 비율: {ratio:.2f}% ({alert})")
            site_report.append("-" * 40)




    # ✅ 분석 결과 저장
    if site_report:
        report_path = os.path.join(EVALU_DIR, "site_anomaly_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(site_report))
        print(f"✅ Site Commonality 분석 완료. 결과 저장: {report_path}")
    else:
        print("⚠️ Site별 공통 이상값이 없습니다.")
