import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_curve

def optimize_isolation_forest(processed_df, contamination=0.05, random_state=42):
    """
    정규화된 데이터(processed_df)를 활용하여 Isolation Forest 기반 이상 탐지를 수행하고 최적 Threshold를 찾음.
    
    :param processed_df: 정규화된 데이터프레임
    :param contamination: 이상치 비율 (기본값: 5%)
    :param random_state: 랜덤 시드
    :return: 이상 탐지 결과가 추가된 데이터프레임
    """
    print("✅ Isolation Forest 적용 중...")

    # ✅ 모델 학습 시 기존 feature만 사용하도록 처리
    feature_df = processed_df.drop(columns=["anomaly_score", "anomaly_value"], errors="ignore")

    # ✅ Isolation Forest 모델 학습 (정규화된 데이터 사용)
    iso_forest = IsolationForest(contamination=contamination, random_state=random_state)
    processed_df["anomaly_score"] = iso_forest.fit_predict(feature_df)  # (-1: 이상값, 1: 정상)
    processed_df["anomaly_value"] = iso_forest.decision_function(feature_df)  # 이상 탐지 점수 (값이 작을수록 이상)
    
    # ✅ Precision-Recall Curve 기반 최적 Threshold 찾기
    true_labels = (processed_df["anomaly_score"] == -1).astype(int)  # 이상값 여부 (1: 이상, 0: 정상)
    precision, recall, thresholds = precision_recall_curve(true_labels, processed_df["anomaly_value"])

    # ✅ F1-score 계산
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)

    # ✅ 최적 Threshold 선택 (F1-score 최대 지점)
    best_threshold = thresholds[np.argmax(f1_scores)]
    print(f"🎯 최적 Threshold: {best_threshold:.4f}")

    # ✅ 최적 Threshold 적용하여 이상값 분류
    processed_df["is_anomaly"] = processed_df["anomaly_value"] < best_threshold

    # ✅ Precision-Recall Curve 시각화
    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, f1_scores[:-1], label="F1-score", marker="o")
    plt.axvline(best_threshold, color="red", linestyle="--", label=f"Best Threshold = {best_threshold:.4f}")
    plt.xlabel("Threshold")
    plt.ylabel("F1-score")
    plt.legend()
    plt.title("Optimal Threshold Selection using Precision-Recall Curve")
    plt.show()

    print("✅ 최적화된 Isolation Forest 적용 완료!")
    
    return processed_df
