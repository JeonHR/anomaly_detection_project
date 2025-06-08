import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.spatial.distance import squareform


def correlation_heatmap_by_site(df, site_col='Site', save_dir='correlation_by_site', method='pearson'):
    os.makedirs(save_dir, exist_ok=True)
    grouped = df.groupby(site_col)

    for site, group in grouped:
        numeric = group.select_dtypes(include=[np.number]).dropna()
        if numeric.shape[1] < 2: # 열의 개수 / 행의 개수라면 shape[0]를 사용
            print(f"❌ {site}는 유효한 숫자 데이터 부족")
            continue

        corr_matrix = numeric.corr(method=method)

        plt.figure(figsize=(14, 12))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0) # center=0는 색상 맵의 중심을 0으로 설정
        plt.title(f"[Site {site}] Correlation Heatmap ({method})") 
        plt.tight_layout() # 자동으로 레이아웃 조정

        save_path = os.path.join(save_dir, f"site_{site}_correlation.png") 
        plt.savefig(save_path)
        plt.close()
        print(f"✅ 저장 완료: {save_path}")
