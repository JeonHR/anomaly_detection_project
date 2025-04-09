import os
import numpy as np


def calculate_site_cpk(df, site_col="Site", EVALU_DIR="evaluation_reports", cpk_threshold=1.33):
    """
    ✅ Site별 Cpk 분석 & 주의 표시 추가
    - Cpk = min(Cpu, Cpl)
    - Cpu = (USL - 평균) / (3 * 표준편차)
    - Cpl = (평균 - LSL) / (3 * 표준편차)
    - Cpk < 1.33 → ⚠️ (위험)
    - Site 간 Cpk 차이 크면 ❗ (주의)
    """

    if not os.path.exists(EVALU_DIR):
        os.makedirs(EVALU_DIR)

    report = []
    

    # ✅ 1. 숫자형 컬럼만 선택
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    # ✅ 2. site_col과 'TestResult' 컬럼 제외
    test_columns = [col for col in numeric_columns if col not in [site_col, "TestResult"]]

    for test_col in test_columns:
        if test_col not in df.attrs["Upper Limits"] or test_col not in df.attrs["Lower Limits"]:
            continue  # 상/하한값 없는 경우 스킵

        usl = df.attrs["Upper Limits"][test_col]  # Upper Spec Limit (USL)
        lsl = df.attrs["Lower Limits"][test_col]  # Lower Spec Limit (LSL)

        site_cpk_results = {}

        for site, site_data in df.groupby(site_col):
            if site_data[test_col].count() < 2:
                continue  # 데이터 부족

            mean = site_data[test_col].mean()
            std_dev = site_data[test_col].std()

            if std_dev == 0:
                site_cpk_results[site] = "⚠️ 표준편차=0 (Cpk 계산 불가)"
                continue

            cpu = (usl - mean) / (3 * std_dev) if usl is not None else np.nan
            cpl = (mean - lsl) / (3 * std_dev) if lsl is not None else np.nan
            cpk = min(cpu, cpl)

            site_cpk_results[site] = cpk

        # ✅ Cpk 차이 계산
        valid_cpk_values = [v for v in site_cpk_results.values() if isinstance(v, float)]
        max_cpk, min_cpk = max(valid_cpk_values, default=0), min(valid_cpk_values, default=0)
        cpk_diff = max_cpk - min_cpk
        diff_flag = "❗ 주의 (Site별 차이 큼)" if cpk_diff > 0.5 else ""

        # ✅ Cpk 결과 저장
        report.append(f"📊 [Test Item: {test_col}] {diff_flag}")
        for site, cpk in site_cpk_results.items():
            if isinstance(cpk, float):
                warning = "⚠️ 위험" if cpk < cpk_threshold else ""
                report.append(f"   - Site: {site} | Cpk: {cpk:.3f} {warning}")
            else:
                report.append(f"   - Site: {site} | {cpk}")
        report.append("-" * 50)

    # ✅ 결과 저장
    report_path = os.path.join(EVALU_DIR, "site_cpk_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"✅ Site별 Cpk 분석 완료. 결과 저장: {report_path}")
