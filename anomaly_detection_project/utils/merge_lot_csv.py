import os
import pandas as pd

def merge_lot_csv_simple(base_dir):
    """
    Lot 폴더 내의 CSV 파일을 단순히 텍스트로 병합 (copy *.csv 방식 모방).
    - 첫 번째 파일은 헤더 포함, 나머지는 데이터만.
    """
    merged_files = []

    for lot_folder in os.listdir(base_dir):
        lot_path = os.path.join(base_dir, lot_folder)

        if os.path.isdir(lot_path):
            csv_files = [
                os.path.join(lot_path, f) 
                for f in os.listdir(lot_path) 
                if f.lower().endswith(".csv")
            ]

            if not csv_files:
                print(f"⚠️ {lot_folder} 폴더에 CSV 파일이 없음")
                continue

            first_file_name = os.path.basename(csv_files[0])
            parts = first_file_name.split("_")

            if len(parts) < 4:
                print(f"⚠️ {first_file_name}에서 Lot 정보를 찾을 수 없음")
                continue

            lot_name = parts[3]
            merged_csv_path = os.path.join(lot_path, f"{lot_name}.csv")

            try:
                # 첫 번째 파일 읽기 (헤더 포함)
                df_main = pd.read_csv(csv_files[0],skiprows=1, encoding='utf-8-sig')
                base_columns = df_main.columns.tolist()  # 헤더 저장
                base_dtype = df_main.dtypes.to_dict()    # dtype 저장
                print(f"📌 첫 파일 로딩: {csv_files[0]}, 컬럼: {base_columns}")

                # 두 번째 이후 파일들 병합
                for csv_file in csv_files[1:]:
                    # 3행 스킵 후 읽기, 첫 파일의 헤더 사용
                    df_temp = pd.read_csv(
                        csv_file,
                        skiprows=4,              # 상위 3행 스킵
                        header=None,             # 헤더 없음
                        names=base_columns,      # 첫 파일의 컬럼 이름 사용
                        dtype=base_dtype,        # 첫 파일의 dtype 적용
                        encoding='utf-8-sig',    # 일관된 인코딩
                        on_bad_lines='warn'      # 문제 행 경고 후 스킵
                    )
                    # 컬럼 수 검증
                    if len(df_temp.columns) != len(base_columns):
                        print(f"⚠️ {csv_file} 컬럼 수 불일치: 예상 {len(base_columns)}, 실제 {len(df_temp.columns)}")
                        continue
                    df_main = pd.concat([df_main, df_temp], ignore_index=True)
                    print(f"📌 데이터 추가 (3행 제거): {csv_file}")

                # 저장 (BOM 포함 UTF-8로, Excel 호환성)
                df_main.to_csv(merged_csv_path, index=False, encoding='utf-8-sig')
                merged_files.append(merged_csv_path)
                print(f"✅ 병합 완료: {merged_csv_path}")

            except Exception as e:
                print(f"❌ 병합 실패: {csv_file} - {e}")
                continue


    return merged_files
