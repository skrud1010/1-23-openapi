"""
open_api_key 테스트.env
.env에서 api키를 가져와서 작동하는지 여부 확인
"""
import os 
from dotenv import load_dotenv
from openai import OpenAI
import json



print("="*60)
print("openai 테스트 시작")
print("="*60)

#1. env 로드 
print("\n .env 파일 로드 중...")
load_dotenv()  #env파일을 로드하겠다

#2. API 키 확인
api_key=os.getenv("open_api_key") 

if not api_key :
    print("실패 : open_api_key 찾을 수 없습니다.")
    print(".env 파일에 open_api_key 설정되어 있는지 확인하세요.")
    exit()


#3. openai 클라이언트 생성
print("\n openai 클라이언트 생성 중..")
try : 
    client=OpenAI(api_key = api_key)
    print("\n openai 클라이언트 성공")

except Exception as e : 
    print("클라이언트 생성 실패")
    exit()





[
    {"hscode": "8542.31", "description": "Electronic integrated circuits: Processors and controllers"},
    {"hscode": "8471.30", "description": "Portable automatic data processing machines (Laptops)"},
    {"hscode": "8517.13", "description": "Smartphones and other wireless network telephones"}
]




load_dotenv()
client = OpenAI(api_key=os.getenv("open_api_key"))

# 4. HS Code 마스터 데이터 (예시)
hs_data = [
    {"hscode": "8542.31", "description": "Electronic integrated circuits: Processors and controllers"},
    {"hscode": "8471.30", "description": "Portable automatic data processing machines (Laptops)"},
    {"hscode": "8517.13", "description": "Smartphones and other wireless network telephones"}
]

def analyze_hs_code(product_name):
    print(f"\n🔍 '{product_name}'에 대한 HS Code 분석을 시작합니다...")
    
    # 5. OpenAI를 이용한 의미론적 매핑
    prompt = f"""
    당신은 20년 경력의 관세사 및 무역 데이터 분석 전문가입니다.
    다음 상품 설명에 가장 적합한 HS Code를 아래 제공된 리스트에서 찾아 출력하고 이유를 설명하세요.
    
    리스트: {json.dumps(hs_data)}
    상품명: {product_name}
    
    형식:
    - 추천 HS Code: 
    - 근거: 
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"분석 중 오류 발생: {e}"

# 6.실행 테스트
user_input = "Next-generation AI semiconductor chips for servers"
result = analyze_hs_code(user_input)

print("\n" + "="*60)
print(result)
print("="*60)