import os

def analyze_fail_by_sbin(fail_data, data_file):
    """
    SBIN(Soft Bin) 및 Site 기준으로 FAIL 개수 및 비율을 분석하여 CSV 저장.

    :param fail_data: FAIL 데이터프레임
    :param data_file: 원본 CSV 파일 경로
    :return: (SBIN별 FAIL 분석 데이터프레임, Site별 SBIN 분석 데이터프레임)
    """
    if "sbin" not in fail_data.columns or "Site" not in fail_data.columns:
        print("⚠️ FAIL 데이터에 'sbin' 또는 'Site' 컬럼이 없습니다.")
        return None, None

    # ✅ SBIN별 FAIL 개수 집계
    sbin_fail_counts = fail_data["sbin"].value_counts().reset_index()
    sbin_fail_counts.columns = ["sbin", "Fail_Count"]

    # ✅ FAIL 비율(%) 계산
    total_fail_count = sbin_fail_counts["Fail_Count"].sum()
    sbin_fail_counts["Fail_Rate(%)"] = (sbin_fail_counts["Fail_Count"] / total_fail_count) * 100

    print("\n🔍 SBIN 기준 FAIL 분석 결과:")
    print(sbin_fail_counts)

    # ✅ Site별 SBIN 분석
    site_sbin_fail_counts = fail_data.groupby(["Site", "sbin"]).size().reset_index(name="Fail_Count")
    site_sbin_fail_counts["Fail_Rate(%)"] = (site_sbin_fail_counts["Fail_Count"] / total_fail_count) * 100


    print("\n🔍 Site별 SBIN 분석 결과:")
    print(site_sbin_fail_counts)

    # ✅ CSV로 저장
    
    SBIN_CSV_PATH = os.path.join(data_file, "sbin_fail_analysis.csv")
    SITE_SBIN_CSV_PATH = os.path.join(data_file, "site_sbin_fail_analysis.csv")

    sbin_fail_counts.to_csv(SBIN_CSV_PATH, index=False, encoding="utf-8-sig")
    site_sbin_fail_counts.to_csv(SITE_SBIN_CSV_PATH, index=False, encoding="utf-8-sig")

    print(f"\n✅ SBIN 분석 결과 저장: {SBIN_CSV_PATH}")
    print(f"✅ Site별 SBIN 분석 결과 저장: {SITE_SBIN_CSV_PATH}")

    return sbin_fail_counts, site_sbin_fail_counts
