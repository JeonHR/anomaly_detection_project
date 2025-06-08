import os
from utils.data_loader import load_data
from utils.data_analysis import explore_data
from utils.data_analysis2 import explore_data_by_site
from utils.anomaly_detection import detect_anomalies
from utils.evaluate_anomalies import analyze_anomalies
from utils.commonality_analysis import analyze_site_commonality
from utils.calculate_site_cpk import calculate_site_cpk
from utils.analyze_fail_by_sbin import analyze_fail_by_sbin
from utils.analyze_fail_trend import process_fail_trend
from utils.analyze_fail_trend import plot_fail_trend
from utils.optimize_thresholds import manage_thresholds
from utils.merge_lot_csv import merge_lot_csv_simple
from utils.correlation import correlation_heatmap_by_site



# ✅ 데이터 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filter_file_PATH= os.path.join(BASE_DIR, "2DID_sorting.txt")
DATA_PATH4 = os.path.join(BASE_DIR, "data")
thresholds_PATH = os.path.join(BASE_DIR, "thresholds")

# ✅ Lot 병합 수행
merged_files = merge_lot_csv_simple(DATA_PATH4)

# ✅ 병합된 파일들에 대해 `load_data` 실행
for file_path in merged_files:

# ✅ 데이터 로드 및 전처리
    
    lot_name = os.path.splitext(os.path.basename(file_path))[0]
    
    All_df, pass_data,fail_data, upper_limits,lower_limits,LIMITS_PATH = load_data(file_path ,filter_file_PATH)

   
    

    
    
    EDA_SAVE_DIR = os.path.join(BASE_DIR, "eda_plots", lot_name)
    
    # ✅ 데이터 로드 및 전처리
    explore_data(pass_data, EDA_SAVE_DIR, LIMITS_PATH)
    
    explore_data_by_site(pass_data, EDA_SAVE_DIR, LIMITS_PATH)

    # ✅ 데이터 탐색 및 시각화
    fail_trend = process_fail_trend(fail_data)

    save_path  = os.path.join(BASE_DIR, "anomaly_plots", lot_name, "fail_trend_plot.png")
    
    #  ✅ Fail 트렌드 분석
    plot_fail_trend(fail_trend,save_path)
    
    SAVE_DIR = os.path.join(BASE_DIR, "anomaly_plots", lot_name)
    
    # ✅ 이상 탐지 수행
    pass_data, anomalies,anomaly_counts_df = detect_anomalies(pass_data,LIMITS_PATH,SAVE_DIR)
    
    EVALU_DIR = os.path.join(BASE_DIR, "evaluation_reports",lot_name)
    
    ## ✅ 이상 탐지 결과 분석 
    thresholds = manage_thresholds(All_df, anomalies, anomaly_counts_df, thresholds_PATH, EVALU_DIR)
    
    analyze_anomalies(All_df, anomalies,anomaly_counts_df, thresholds ,EVALU_DIR)
    
    analyze_site_commonality(All_df, anomalies,  site_col="Site", EVALU_DIR=EVALU_DIR)
    calculate_site_cpk(pass_data)
    analyze_fail_by_sbin(fail_data, EVALU_DIR)



print("✅ 모든 Lot 데이터 처리 완료!")
