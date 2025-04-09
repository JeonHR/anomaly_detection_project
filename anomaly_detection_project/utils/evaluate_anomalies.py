import os
import pandas as pd
import numpy as np

def analyze_anomalies(df, anomalies, anomaly_counts_df, thresholds=None, EVALU_DIR="evaluation_reports", use_default_if_missing=True):
    if not os.path.exists(EVALU_DIR):
        os.makedirs(EVALU_DIR)

    report = []
    default_threshold = 5
    total_samples = df.shape[0]
    if total_samples == 0:
        print("⚠️ 데이터가 없습니다. 분석을 종료합니다.")
        return

    for col in anomalies.columns:
        if col not in df.columns:
            continue

        anomaly_count = anomaly_counts_df.at["Anomaly_Count", col] if col in anomaly_counts_df.columns else 0
        if anomaly_count == 0:
            continue

        anomaly_ratio = (anomaly_count / total_samples) * 100
        print(f"📌 컬럼: {col}, 이상값 비율: {anomaly_ratio:.2f}%")

        if thresholds is not None and col in thresholds:
            col_threshold = thresholds[col]
            if col_threshold > default_threshold:
                selected_threshold = col_threshold
                threshold_source = "동적 Threshold (우선 적용)"
            else:
                selected_threshold = default_threshold
                threshold_source = "디폴트 Threshold (동적 값보다 낮음)"
        elif use_default_if_missing:
            selected_threshold = default_threshold
            threshold_source = "디폴트 Threshold"
        else:
            raise ValueError(f"컬럼 '{col}'에 대한 Threshold가 제공되지 않았습니다.")

        alert = "🔴 이상 감지" if anomaly_ratio >= selected_threshold else "🟢 정상 범위"

        anomaly_values = pd.to_numeric(anomalies[col], errors="coerce").dropna()
        if anomaly_values.empty:
            continue

        mean_anomaly = anomaly_values.mean()
        std_anomaly = anomaly_values.std()
        min_anomaly = anomaly_values.min()
        max_anomaly = anomaly_values.max()

        report.append(f"📌 컬럼: {col}")
        report.append(f"   - 이상값 개수: {anomaly_count}")
        report.append(f"   - 이상값 비율: {anomaly_ratio:.2f}% ({alert})")
        report.append(f"   - 이상값 평균: {mean_anomaly:.2f}, 표준편차: {std_anomaly:.2f}")
        report.append(f"   - 이상값 최소값: {min_anomaly}, 최대값: {max_anomaly}")
        report.append(f"   - 사용된 Threshold (비율): {selected_threshold:.2f}% ({threshold_source})")
        if thresholds and col in thresholds:
            report.append(f"   - 제공된 동적 Threshold: {col_threshold:.2f}%")
        report.append("-" * 40)

    if report:
        report_path = os.path.join(EVALU_DIR, "anomaly_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print(f"✅ 이상값 분석 완료. 결과 저장: {report_path}")
    else:
        print("⚠️ 분석할 이상값이 없습니다.")