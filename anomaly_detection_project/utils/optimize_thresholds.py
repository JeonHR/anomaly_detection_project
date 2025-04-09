import os
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import IsolationForest

def manage_thresholds(df, anomalies, anomaly_counts_df, base_dir,
                      evalu_dir, change_threshold=20, use_ml=True):
    """
    Threshold 관리 및 변동 경고 (비율 기반)
    - JSON 파일을 base_dir 기준 data/ 디렉토리에 저장
    - IsolationForest 사용 시 오류 방지
    """
    total_samples = df.shape[0]
    threshold_file = os.path.join(base_dir, "thresholds.json")
    historical_file = os.path.join(base_dir, "historical_thresholds.json")
    if not os.path.exists(evalu_dir):
        os.makedirs(evalu_dir)

    # 파일 로드 함수
    def load_json(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    thresholds = load_json(threshold_file)
    historical_thresholds = load_json(historical_file)

    
    report = []

    for col in anomalies.columns:
        anomaly_count = anomaly_counts_df.at["Anomaly_Count", col] if col in anomaly_counts_df.columns else 0
        if anomaly_count == 0:
            continue

        anomaly_ratio = (anomaly_count / total_samples) * 100
        anomaly_values = pd.to_numeric(anomalies[col], errors="coerce").dropna()
        if anomaly_values.empty:
            continue

        historical_col = historical_thresholds.get(col, [])
        combined_ratios = [anomaly_ratio] + historical_col if historical_col else [anomaly_ratio]

        if use_ml:
            model = IsolationForest(contamination=0.05, random_state=42)
            if not anomaly_values.empty and len(anomaly_values) > 1:
                X = anomaly_values.values.reshape(-1, 1)
                model.fit(X)
                predictions = model.predict(X)
                new_threshold = (sum(predictions == -1) / len(X)) * 100
            else:
                new_threshold = anomaly_ratio  # 데이터가 부족하면 기존 비율 유지


        old_threshold = thresholds.get(col)
        change_alert = ""
        if old_threshold and old_threshold != 0:
            change_percent = abs(new_threshold - old_threshold) / old_threshold * 100
            if change_percent > change_threshold:
                change_alert = f"🔴 Threshold 변동 경고: {change_percent:.2f}% 변동 (기존: {old_threshold:.2f})"
        
        thresholds[col] = new_threshold
        historical_thresholds[col] = (historical_col + [new_threshold])[-10:]

        report.append(f"📌 컬럼: {col}")
        report.append(f"   - 적용된 Threshold (비율): {new_threshold:.2f}%")
        report.append(f"   - 결합된 비율 수: {len(combined_ratios)}")
        if use_ml:
            report.append(f"   - 계산 방법: IsolationForest")
        if change_alert:
            report.append(f"   - {change_alert}")
        report.append("-" * 40)

    # JSON 저장 함수
    def save_json(file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f)

    save_json(threshold_file, thresholds)
    save_json(historical_file, historical_thresholds)

    if report:
        report_path = os.path.join(evalu_dir, "threshold_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print(f"✅ Threshold 관리 완료. 결과 저장: {report_path}")
    else:
        print("⚠️ Threshold를 계산할 데이터가 없습니다.")

    return thresholds
