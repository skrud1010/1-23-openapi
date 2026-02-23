"""
open_api_key 테스트.env
.env에서 api키를 가져와서 작동하는지 여부 확인
"""
import os 
from dotenv import load_dotenv
from openai import OpenAI
import requests


# print("="*60)
# print("openai 테스트 시작")
# print("="*60)

# #1. env 로드 
# print("\n .env 파일 로드 중...")
# load_dotenv()  #env파일을 로드하겠다

# #2. API 키 확인
# api_key=os.getenv("api_key") 

# if not api_key :
#     print("실패 : api_key 찾을 수 없습니다.")
#     print(".env 파일에 api_key 설정되어 있는지 확인하세요.")
#     exit()


# #3. openai 클라이언트 생성
# print("\n openai 클라이언트 생성 중..")
# try : 
#     client=OpenAI(api_key = api_key)
#     print("\n openai 클라이언트 성공")

# except Exception as e : 
#     print("클라이언트 생성 실패")
#     exit()



load_dotenv()

# 1. 각 서비스에 맞는 API 키 로드
OPENAI_KEY = os.getenv("open_api_key")
WEATHER_KEY = os.getenv("weather_api_key") # OpenWeatherMap 등에서 받은 키

client = OpenAI(api_key=OPENAI_KEY)

def get_realtime_weather(city="Seoul"):
    # 2. 실시간 날씨 API 호출 (OpenWeatherMap 예시)
    # API 키가 유효해야 작동합니다.
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric&lang=kr"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"현재 {city}의 날씨는 {weather_desc}이며, 기온은 {temp}도입니다."
    else:
        return "날씨 정보를 가져올 수 없습니다. 키를 확인하세요."

# --- 실행 부분 ---

# 3. 실제 데이터 가져오기
current_weather = get_realtime_weather("Seoul")
print(f"조회된 데이터: {current_weather}")

# 4. OpenAI에게 날씨 데이터를 주고 문장 작성을 요청
try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 기상 캐스터야. 제공된 날씨 데이터를 바탕으로 친절하게 옷차림을 추천해줘."},
            {"role": "user", "content": f"오늘의 날씨 데이터: {current_weather}"}
        ]
    )
    
    print("\n" + "="*60)
    print("[🌡️AI 기상 캐스터의 추천🌞]")
    print(response.choices[0].message.content)
    print("="*60)

except Exception as e:
    print(f"OpenAI 호출 오류: {e}")