import os    #운영체제
import requests
from dotenv import load_dotenv  #env에서 변수


load_dotenv()  #함수를 호출해서 env에서 가져온다
API_KEY=os.getenv("EXCHANGE_RATE_KEY")
url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"  #여기에 진짜 내 주소 쓰면 안되고 변수명 써야함

# response=requests.get(url)  #이 url에서 가져오는 정보를 response에 저장
# df=response.json()   #그 정보를 데이터화
# print(df)


def currency_invoice(price_dict) :
    url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD" 
    df=requests.get(url).json()['conversion_rates']  #df=response.jason()을 합침. 해당 데이터만 갖고와도 된다(conversion_rates만 가져오기)
    print("\n" + "-"*70)
    print("🛳️실시간 API 연동 수입 견적 리포트")
    print("-"*70)

    # item_krw= (price*df["KRW"])
    # print(f"수입 총 원가 : {item_krw:,.2f}원")



    for item, (price, unit) in price_dict.items() :  #items는 키와 벨류. 
        # 외화 가격  *한국 환율=원화가격  100
        #(외화가격/해당국가환율)*한국환율
        item_krw=(price /df[unit])* df["KRW"]    
        print(f"{item :<8} | {price:>10}{unit} => {item_krw:>12,.2f}원")


# currency_invoice(10000)    수입 총 원가 사용할때


#샘플 데이터
sample_items={
    "미국 사과" : (100, "USD"),   #100달러치
    "일본 자동차" : (10000, "JPY"), #10000엔치
    "유럽 가방" : (300, "EUR")
}
currency_invoice(sample_items)