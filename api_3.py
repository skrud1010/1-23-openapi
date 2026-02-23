import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATE_KEY")

class ExchangeRateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("실시간 환율 계산기 (KRW ⮕ EUR)")
        self.root.geometry("450x450")
        self.root.configure(bg="#f8f9fa")

        # UI 스타일
        title_font = ("Apple SD Gothic Neo", 20, "bold")
        label_font = ("Apple SD Gothic Neo", 11)
        result_font = ("Arial", 16, "bold")

        # 1. 제목
        tk.Label(root, text="💶 환율 계산기 (수수료 설정)", font=title_font, bg="#f8f9fa", pady=20).pack()

        # 2. 원화 입력
        tk.Label(root, text="변환할 원화(KRW) 금액:", font=label_font, bg="#f8f9fa").pack()
        self.entry_krw = tk.Entry(root, font=("Arial", 14), justify='center', width=20)
        self.entry_krw.pack(pady=5)
        self.entry_krw.insert(0, "1000000")

        # 3. 수수료 설정 (0% ~ 1.5%)
        tk.Label(root, text="\n수수료 설정 (%):", font=label_font, bg="#f8f9fa").pack()
        self.fee_slider = tk.Scale(root, from_=0, to=1.5, resolution=0.1, orient="horizontal", 
                                   length=300, bg="#f8f9fa", highlightthickness=0)
        self.fee_slider.pack(pady=5)
        self.fee_slider.set(0.5)  # 기본값 0.5%

        # 4. 결과창
        self.result_frame = tk.Frame(root, bg="#e9ecef", padx=20, pady=15, relief="groove", bd=1)
        self.result_frame.pack(pady=20, fill="x", padx=40)
        
        self.result_label = tk.Label(self.result_frame, text="금액을 입력하고 변환하세요", 
                                     font=result_font, bg="#e9ecef", fg="#2c3e50")
        self.result_label.pack()
        
        self.fee_info_label = tk.Label(self.result_frame, text="수수료: 0 EUR", 
                                       font=label_font, bg="#e9ecef", fg="#e74c3c")
        self.fee_info_label.pack()

        # 5. 변환 버튼
        self.calc_button = tk.Button(root, text="실시간 환율로 변환하기", command=self.calculate_exchange, 
                                     bg="#007bff", fg="white", font=("Apple SD Gothic Neo", 12, "bold"), 
                                     padx=30, pady=10, cursor="hand2")
        self.calc_button.pack(pady=10)

    def get_exchange_rate(self):
        """API 호출: KRW 기준 EUR 환율 가져오기"""
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/KRW"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                return data["conversion_rates"]["EUR"]
            return None
        except:
            return None

    def calculate_exchange(self):
        krw_text = self.entry_krw.get().replace(",", "") # 쉼표 제거
        
        if not krw_text.replace(".", "").isdigit():
            messagebox.showwarning("입력 오류", "숫자만 입력해주세요.")
            return

        rate = self.get_exchange_rate()
        if rate is None:
            messagebox.showerror("오류", "환율 정보를 가져올 수 없습니다.")
            return

        # 계산 로직
        krw_amount = float(krw_text)
        raw_eur = krw_amount * rate
        
        # 수수료 계산
        fee_percent = self.fee_slider.get()
        fee_amount = raw_eur * (fee_percent / 100)
        final_eur = raw_eur - fee_amount

        # 화면 업데이트
        self.result_label.config(text=f"{final_eur:,.2f} EUR")
        self.fee_info_label.config(text=f"(적용 환율: {rate:.8f} | 수수료 {fee_percent}%: {fee_amount:.2f} EUR 제외)")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExchangeRateApp(root)
    root.mainloop()