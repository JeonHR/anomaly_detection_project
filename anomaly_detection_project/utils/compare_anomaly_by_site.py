import seaborn as sns
import matplotlib.pyplot as plt

def compare_anomaly_by_site(processed_df, site_column="Site"):
    """
    Site별 이상 탐지 비율 비교

    :param processed_df: 이상 탐지가 완료된 데이터프레임
    :param site_column: Site 정보를 포함하는 컬럼명 (기본값: "Site")
    """
    if site_column not in processed_df.columns:
        print(f"⚠️ '{site_column}' 컬럼이 존재하지 않습니다. Site 분석이 불가능합니다.")
        return

    # ✅ Site별 이상 탐지 개수 및 비율 계산
    site_anomaly_stats = processed_df.groupby(site_column)["is_anomaly"].mean().reset_index()
    site_anomaly_stats["is_anomaly"] *= 100  # 비율을 %로 변환

    # ✅ 그래프 시각화
    plt.figure(figsize=(10, 5))
    sns.barplot(data=site_anomaly_stats, x=site_column, y="is_anomaly", palette="coolwarm")
    plt.xlabel("Site")
    plt.ylabel("Anomaly Detection Rate (%)")
    plt.title("📊 Site별 이상 탐지 비율 비교")
    plt.xticks(rotation=45)
    plt.show()
