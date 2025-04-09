import sys
import os
import pandas as pd
import csv

# 필드 크기 제한을 최대로 설정
csv.field_size_limit(sys.maxsize)

def merge_lot_csv(base_dir):
    merged_files = []

    for lot_folder in os.listdir(base_dir):
        lot_path = os.path.join(base_dir, lot_folder)

        if os.path.isdir(lot_path):
            csv_files = [os.path.join(lot_path, f) for f in os.listdir(lot_path) if f.endswith(".csv")]

            if not csv_files:
                print(f"⚠️ {lot_folder} 폴더에 CSV 파일이 없음")
                continue

            # Lot 이름 추출
            first_file_name = os.path.basename(csv_files[0])
            parts = first_file_name.split("_")
            if len(parts) < 4:
                print(f"⚠️ {first_file_name}에서 Lot 정보를 찾을 수 없음")
                continue
            lot_name = parts[3]
            merged_csv_path = os.path.join(lot_path, f"{lot_name}.csv")

            df_list = []
            column_order = None

            for csv_file in csv_files:
                try:
                    with open(csv_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    # 첫 줄이 열 하나면 무시하고 두 번째 줄부터 읽기
                    if len(lines) >= 2 and len(lines[0].strip().split(",")) < 2:
                        df = pd.read_csv(csv_file, skiprows=1, engine="python")
                    else:
                        df = pd.read_csv(csv_file, engine="python")

                    # 컬럼 정렬
                    if column_order is None:
                        column_order = df.columns.tolist()
                    else:
                        df = df[column_order] if set(df.columns) == set(column_order) else None

                    if df is not None:
                        df_list.append(df)

                except Exception as e:
                    print(f"❌ {csv_file} 읽는 중 오류: {e}")
                    continue

            if not df_list:
                print(f"⚠️ {lot_folder}에서 병합할 수 있는 CSV가 없음")
                continue

            merged_df = pd.concat(df_list, ignore_index=True)
            print(f"📝 병합된 컬럼 확인: {list(merged_df.columns)}")
            merged_df.to_csv(merged_csv_path, index=True)
            merged_files.append(merged_csv_path)
            print(f"✅ 병합 완료: {merged_csv_path}")

    return merged_files
