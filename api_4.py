import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import matplotlib.font_manager as fm
import yfinance as yf # 역사적 데이터 수집에 용이
import numpy as np




# <차트 1: 특정 통화(예: USD/KRW)의 30일간 추이를 보여주는 라인 차트 (평균 선 포함).>
# [설정 1] 한글 폰트 깨짐 방지 초기 설정
def setup_korean_font():
    # Windows: Malgun Gothic, Mac: AppleGothic, Colab/Linux: NanumGothic
    font_names = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR']
    font_found = False
    
    for font in font_names:
        if font in [f.name for f in fm.fontManager.ttflist]:
            plt.rcParams['font.family'] = font
            font_found = True
            break
    
    if not font_found:
        print("경고: 시스템에서 적절한 한글 폰트를 찾지 못했습니다. 폰트를 설치하거나 경로를 지정해주세요.")
        
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

setup_korean_font()

# [설정 2] API 및 데이터 연동
# 사용자가 언급한 EXCHANGE_RATE_KEY (환경 변수 등에서 가져온다고 가정)
EXCHANGE_RATE_KEY = os.getenv('EXCHANGE_RATE_KEY', 'YOUR_DEFAULT_API_KEY_HERE')

def get_exchange_rate_data(ticker="USDKRW=X", period="30d"):
    """
    yfinance를 사용하여 USD/KRW 30일 데이터를 가져옵니다.
    만약 특정 API(Alpha Vantage 등)를 사용한다면 requests를 사용하도록 수정 가능합니다.
    """
    print(f"{ticker} 데이터를 가져오는 중...")
    data = yf.download(ticker, period=period, interval="1d")
    
    # 데이터 정리
    df = data[['Close']].copy()
    df.columns = ['Rate']
    df.index = pd.to_datetime(df.index)
    return df

# 3. 차트 생성 함수
def plot_exchange_rate_trend(df):
    mean_val = df['Rate'].mean()
    
    plt.figure(figsize=(12, 6))
    
    # 메인 라인 차트
    plt.plot(df.index, df['Rate'], marker='o', color='#1f77b4', linewidth=2, label='USD/KRW 환율')
    
    # 평균 선 추가
    plt.axhline(mean_val, color='red', linestyle='--', alpha=0.7, 
                label=f'30일 평균: {mean_val:.2f}원')
    
    # 차트 꾸미기
    plt.title('최근 30일간 USD/KRW 환율 추이', fontsize=16, pad=20)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('환율 (원)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='best')
    
    # 날짜 가독성 개선
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 파일 저장 및 출력
    plt.savefig('exchange_rate_trend.png')
    plt.show()

# 실행
try:
    exchange_df = get_exchange_rate_data()
    if not exchange_df.empty:
        plot_exchange_rate_trend(exchange_df)
    else:
        print("데이터를 가져오지 못했습니다.")
except Exception as e:
    print(f"오류 발생: {e}")











#<차트2,3>

def get_free_exchange_data(days=30, base="USD", symbols="KRW,EUR,JPY,CNY"):
    # 1. 날짜 설정 (최근 30일)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # 2. Frankfurter API URL (키 없이 호출 가능)
    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base}&to={symbols}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 3. 데이터프레임 변환
        if 'rates' in data:
            # { '날짜': {'KRW': 1300, ...} } 구조를 DataFrame으로 변환
            df = pd.DataFrame.from_dict(data['rates'], orient='index')
            df.index = pd.to_datetime(df.index)
            return df.sort_index()
        else:
            print("데이터 수집 실패:", data)
            return None
    except Exception as e:
        print(f"네트워크 오류: {e}")
        return None

# 데이터 호출
df_final = get_free_exchange_data()

if df_final is not None:
    # <차트 2: 여러 통화의 변동률을 비교하기 위해 첫날을 100으로 잡고 정규화한 비교 차트.>
    plt.figure(figsize=(12, 5))
    df_norm = df_final.div(df_final.iloc[0]) * 100
    for col in df_norm.columns:
        plt.plot(df_norm.index, df_norm[col], label=f"{col} (100 -> {df_norm[col].iloc[-1]:.1f})", marker='o', markersize=3)
    
    plt.title('Normalized Currency Comparison (Starting from 100)', fontsize=14)
    plt.axhline(100, color='black', linestyle='--', alpha=0.5)
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig('chart_2_normalized.png')
    plt.savefig('chart_2_normalized.png')
    plt.show()  # <--- 이 줄을 추가하면 창이 뜹니다!







    #<차트 3: 날짜별 변동폭을 보여주는 히트맵(Heatmap)>
    plt.figure(figsize=(14, 6))
    # 일일 변동률(%) 계산
    df_pct = df_final.pct_change().dropna() * 100
    # 날짜 가독성을 위해 형식 변경
    df_pct.index = df_pct.index.strftime('%m-%d')
    
    sns.heatmap(df_pct.T, annot=True, fmt=".2f", cmap='RdYlGn', center=0)
    plt.title('Daily Change Percentage Heatmap (%)', fontsize=14)
    plt.tight_layout()
    plt.savefig('chart_3_heatmap.png')
    plt.savefig('chart_3_heatmap.png')
    plt.show()
    
    print("차트 생성 완료: chart_2_normalized.png, chart_3_heatmap.png")





#<차트 4: 통화별 최소/평균/최대 환율을 보여주는 막대 차트.>

def draw_min_avg_max_chart(df):
    if df is None or df.empty:
        print("데이터가 없어 차트를 그릴 수 없습니다.")
        return

    # 1. 통계 데이터 계산 (최소, 평균, 최대)
    stats = df.agg(['min', 'mean', 'max']).T
    stats.columns = ['Minimum', 'Average', 'Maximum']

    # 2. 시각화 설정
    x = np.arange(len(stats.index))  # 통화별 위치 (KRW, EUR 등)
    width = 0.25  # 막대 너비

    fig, ax = plt.subplots(figsize=(12, 7))

    # 3. 막대 그리기
    rects1 = ax.bar(x - width, stats['Minimum'], width, label='Min', color='#3498db')
    rects2 = ax.bar(x, stats['Average'], width, label='Avg', color='#9b59b6')
    rects3 = ax.bar(x + width, stats['Maximum'], width, label='Max', color='#e74c3c')

    # 4. 스타일링 및 라벨 추가
    ax.set_ylabel('Exchange Rate Value')
    ax.set_title('Currency Statistics: Min, Avg, Max (Last 30 Days)', fontsize=15)
    ax.set_xticks(x)
    ax.set_xticklabels(stats.index)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 5. 막대 위에 수치 표시 (선택 사항)
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3포인트 위로 띄움
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.savefig('chart_4_statistics.png')
    plt.show()  # 화면에 즉시 표시
    print("차트 4 저장 완료: chart_4_statistics.png")

# 앞서 수집한 df_final이 있다고 가정하고 실행
draw_min_avg_max_chart(df_final)