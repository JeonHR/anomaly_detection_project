import os
import json
import pandas as pd

def load_data(data_file, filter_file=None):
    """
    CSV 파일을 불러와 Header 제거 후, 두 번째 행을 Test Item으로 고정.
    세 번째/네 번째 행을 Upper/Lower Limit으로 저장하고 이후 데이터를 반환.
    선택한 열만 가져오는 기능 포함 (TXT 파일에서 열 목록을 로드).

    :param data_file: 테스트 데이터 CSV 파일 경로
    :param filter_file: 선택할 열이 정의된 TXT 파일 경로
    :return: (정리된 데이터프레임, Upper Limit, Lower Limit, FAIL 데이터)
    """
    
    # ✅ CSV 로드 (첫 행 제거)
    df = pd.read_csv(data_file, skiprows=1)

    # ✅ Upper/Lower Limit 추출 및 데이터프레임에서 제거
    upper_limits = df.iloc[0].to_dict()  # Upper Limit을 딕셔너리로 변환
    lower_limits = df.iloc[1].to_dict()  # Lower Limit을 딕셔너리로 변환

    df = df[2:].reset_index(drop=True)  # 본 데이터만 남기고 인덱스 리셋

    # ✅ 선택할 열 필터링 (필터 파일이 있을 경우)
    if filter_file and os.path.exists(filter_file):
        with open(filter_file, "r", encoding="utf-8") as f:
            selected_columns = f.read().splitlines()  # 줄 단위로 읽어서 리스트 변환
        
        
        df = df.loc[:, selected_columns]  # 데이터프레임 필터링

    # ✅ PASS / FAIL 데이터 분리
    All_df = df[(df['TestResult'] == 'FAIL') | (df['TestResult'] == 'PASS') ].copy()
    fail_data = df[df['TestResult'] == 'FAIL'].copy()
    pass_data = df[df['TestResult'] == 'PASS'].copy()

    # ✅ Upper/Lower Limit을 별도 저장 (속성으로 추가)
    pass_data.attrs["Upper Limits"] = upper_limits
    pass_data.attrs["Lower Limits"] = lower_limits

    print("✅ 데이터 로드 완료")
    print("\n🔍 변환된 Upper Limits:", upper_limits)  
    print("\n🔍 변환된 Lower Limits:", lower_limits)  
    print("\n🔍 필터링 후 PASS 데이터 미리보기:")
    print(pass_data.head())
    print("\n🔍 필터링 후 FAIL 데이터 미리보기:")
    print(fail_data.head())

    # ✅ Upper/Lower Limit을 JSON 파일로 저장 (올바른 경로 설정)
    LIMITS_PATH = os.path.join(os.path.dirname(data_file), "limits.json")

    limits_data = {"Upper": upper_limits, "Lower": lower_limits}
    
    with open(LIMITS_PATH, "w", encoding="utf-8") as f:
        json.dump(limits_data, f, indent=4)

    print(f"\n✅ Upper/Lower Limit이 JSON 파일로 저장됨: {LIMITS_PATH}")

    return All_df, pass_data, fail_data,upper_limits,lower_limits,  LIMITS_PATH
