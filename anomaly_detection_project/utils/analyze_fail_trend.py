import pandas as pd
import matplotlib.pyplot as plt
import os

def process_fail_trend(fail_data):
    """
    Site별로 Fail 비율 트렌드를 분석하여 시간 단위로 그룹핑.
    
    :param fail_data: Fail 데이터만 포함된 DataFrame
    :return: 시간 단위로 Fail 개수가 집계된 DataFrame
    """
    # ✅ 시간 컬럼을 datetime 형식으로 변환
    fail_data['Timestamp'] = pd.to_datetime(fail_data['startTime'])  
    
    # ✅ 시간 단위로 그룹화하여 Site별 Fail 카운트 계산
    fail_trend = (fail_data
                  .groupby(['Site', pd.Grouper(key='Timestamp', freq='H')])
                  .size()
                  .reset_index(name='FailCount'))
   
    return fail_trend

def plot_fail_trend(fail_trend, save_path=None):
    """
    Site별 시간 단위 Fail 개수를 그래프로 시각화 (자동 크기 조정 포함)
    """
    num_timestamps = fail_trend['Timestamp'].nunique()  # X축 시간 개수
    num_sites = fail_trend['Site'].nunique()  # Y축 Site 개수

    # ✅ 그래프 크기 자동 조정 (최소 8x5, 최대 20x10)
    width = min(max(num_timestamps // 5, 8), 20)
    height = min(max(num_sites, 5), 10)
    
    plt.figure(figsize=(width, height))

    for site in fail_trend['Site'].unique():
        site_data = fail_trend[fail_trend['Site'] == site]
        plt.plot(site_data['Timestamp'], site_data['FailCount'], marker='o', label=f"Site {site}")

    plt.xlabel("Time")
    plt.ylabel("Fail Count")
    plt.title("Fail Count Trend per Hour (by Site)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"✅ 그래프 저장 완료: {save_path}")
    plt.close()