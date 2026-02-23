import requests
import os    #운영체제
from dotenv import load_dotenv  #env에서 변수

#1. 환경변수 로드
load_dotenv()
API_KEY=os.getenv("EXCHANGE_RATE_KEY") 

def get_global_exchange_rate() :
    #2. exchangerate-api 전용 주소
    url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"   #여기에 진짜 내 주소 쓰면 안되고 변수명 써야함

    #3. api 응답 결과 성공인지 확인
    try :
        response=requests.get(url)
        data=response.json()
        if data["result"] == "success" :
         #필요한 데이터만 추출하는 작업 
        # 마지막 업데이트 시간 보여줄 것
            rate=data["conversion_rates"]["KRW"]    #필요한 업데이트만 추출
            last_update=data['time_last_update_utc']  #마지막 업데이트 시간
            return  rate , last_update
        else :
           # 오류메시지
           print(f"❌ API 오류 : {data.get('error-type')}")
           return None, None

    except Exception as e: 
        # 시스템오류
        print(f"❌시스템 오류{e}")
        return None, None


url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
response=requests.get(url)
data=response.json()
print(data)



rate, update_time = get_global_exchange_rate()
print("="*60)
print(f"🌏글로벌 실시간 환율 정보 (출처 : ExchangeRate-API)")
print(f"🕑데이터 업데이트 시간(UTC) : {update_time}")
print(f"🪙현재 1달러(%)당 환율 : {rate:,.2f}원")
print("="*60)


#1000달러 수입 시 수입 총 원가
usd_price = 1000  #임의의 가격
total_cost=(usd_price * rate)*1.1   #1.1부가세
print(f"{usd_price:,}달러 물품 수입 총 원가 : {total_cost:,.0f}원")
print("="*60)

