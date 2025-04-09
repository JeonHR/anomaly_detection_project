import os

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
                if f.endswith(".csv")
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
                with open(merged_csv_path, 'w', encoding='utf-8') as outfile:
                    # 첫 번째 파일 전체 복사 (헤더 포함)
                    with open(csv_files[0], 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        print(f"📌 첫 파일 복사: {csv_files[0]}")

                    # 나머지 파일은 헤더 제외하고 데이터만 추가
                    for csv_file in csv_files[1:]:
                        with open(csv_file, 'r', encoding='utf-8') as infile:
                            next(infile)  # 헤더 건너뛰기
                            outfile.write(infile.read())
                        print(f"📌 데이터 추가: {csv_file}")

                merged_files.append(merged_csv_path)
                print(f"✅ 병합 완료: {merged_csv_path}")
            except Exception as e:
                print(f"❌ 병합 실패: {e}")

    return merged_files
