import threading
import time
import tkinter as tk
from io import BytesIO
from tkinter import ttk, messagebox

import requests
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from tkcalendar import Calendar
from webdriver_manager.chrome import ChromeDriverManager

# 예약 정보를 저장할 변수
reservation_data = {}
waiting = False  # 대기 상태를 나타내는 플래그

# 테마별 예약 시간
theme_times = {
    "데스티니 앤드 타로": [
        "10:30", "11:35", "12:40", "13:45", "14:50", "15:55",
        "17:00", "18:05", "19:10", "20:15", "21:20", "22:25"
    ],
    "響 : 향": [
        "10:00", "11:30", "13:00", "14:30", "16:00",
        "17:30", "19:00", "20:30", "22:00"
    ],
    "TIENTANG CITY": [
        "09:50", "11:25", "13:00", "14:35", "16:10",
        "17:45", "19:20", "20:55", "22:30"
    ],
}

# 테마별 이미지 URL
theme_images = {
    "데스티니 앤드 타로": "https://xdungeon.net/file/theme/50/50_7745391062.jpg",
    "響 : 향": "https://xdungeon.net/file/theme/51/51_9344952071.png",
    "TIENTANG CITY": "https://xdungeon.net/file/theme/59/59_4338951469.png",
}

# 선택된 값의 인덱스를 가져오는 함수
def get_selected_index():
    index = combo_time.current()  # 선택된 값의 인덱스 가져오기
    selected_value = combo_time.get()  # 선택된 값 가져오기
    print(f"선택된 값: {selected_value}, 인덱스: {index}")
    return index


# URL에서 이미지를 로드하여 표시하는 함수
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((280, 180), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("이미지 로드 오류", f"이미지를 로드할 수 없습니다.\n{e}")
        return None

# 테마 선택 시 시간 및 이미지 업데이트
def update_theme(event):
    selected_theme = combo_theme.get()
    times = theme_times[selected_theme]
    combo_time['values'] = times
    combo_time.set(times[0])  # 첫 번째 값을 선택

    # 이미지 업데이트
    image_url = theme_images[selected_theme]
    photo = load_image_from_url(image_url)
    if photo:
        theme_image_label.config(image=photo)
        theme_image_label.image = photo

# 입력 필드 검증
def validate_inputs():
    if not entry_name.get() or not entry_phone2.get() or not entry_phone3.get():
        messagebox.showwarning("입력 오류", "모든 필수 정보를 입력해주세요.")
        return False
    if len(entry_phone2.get()) != 4 or len(entry_phone3.get()) != 4:
        messagebox.showwarning("입력 오류", "전화번호는 4자리여야 합니다.")
        return False
    return True

# 예약 저장 및 대기 시작
def start_waiting():
    """7시까지 대기 후 크롤링 실행"""
    global waiting
    waiting = True

    if not validate_inputs():
        return

    # 예약 정보 저장
    reservation_data["theme"] = combo_theme.get()
    reservation_data["name"] = entry_name.get()
    reservation_data["phone"] = f"010-{entry_phone2.get()}-{entry_phone3.get()}"
    reservation_data["date"] = calendar.get_date()
    reservation_data["time"] = combo_time.get()
    reservation_data["people"] = combo_people.get()

    # 대기 시작 시 남은 시간 업데이트
    update_countdown()
    # 스레드에서 대기 실행
    thread = threading.Thread(target=wait_until_seven)
    thread.daemon = True
    thread.start()

def wait_until_seven():
    perform_crawling()
    """7시까지 대기"""
    global waiting
    while waiting:
        current_time = time.strftime("%H:%M")
        if current_time == "19:00":
            perform_crawling()
            waiting = False  # 대기 종료
        time.sleep(10)  # 10초 간격으로 확인

    if not waiting:
        print("대기 취소됨")

# 크롤링 작업 수행
def perform_crawling():
    """입력된 예약 정보를 POST 요청으로 전송"""
    try:
        url = "https://xdungeon.net/layout/res/home.php?go=rev.main&s_zizum=9&rev_days=" + calendar.get_date()
        index = 1
        if combo_theme.get() == '響 : 향':
            index = 2
        elif combo_theme.get() == 'TIENTANG CITY':
            index = 3

        combo_idx = get_selected_index()
        options = Options()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.implicitly_wait(30)
        # 단축키로 개발자 도구 열기 (F12)
        ActionChains(driver).send_keys(Keys.F12).perform()
        xpath = '//*[@id="contents"]/div/div[1]/div/div[1]/div[2]/div/div[3]/div[' + str(
            index) + ']/div[2]/ul/li[' + str(combo_idx + 1) + ']/a'
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)
        driver.find_element(By.XPATH,
                            '//*[@id="contents"]/div/div/div[1]/div[2]/div[2]/form/div[1]/table/tbody/tr[2]/td[2]/input').send_keys(
            entry_name.get())

        driver.find_element(By.XPATH,
                            '//*[@id="contents"]/div/div/div[1]/div[2]/div[2]/form/div[1]/table/tbody/tr[3]/td[2]/input[2]').send_keys(
            entry_phone2.get())
        driver.find_element(By.XPATH,
                            '//*[@id="contents"]/div/div/div[1]/div[2]/div[2]/form/div[1]/table/tbody/tr[3]/td[2]/input[3]').send_keys(
            entry_phone3.get())
        select_element = driver.find_element(By.XPATH, '//*[@id="person"]')  # select box의 name 속성 사용
        select = Select(select_element)
        select.select_by_value(combo_people.get())
        if entry_coupon.get() != '':
            driver.find_element(By.XPATH, '//*[@id="coupon"]').send_keys(entry_coupon.get())
            coupon_button = driver.find_element(By.XPATH, '//*[@id="coupon_exe"]/button')
            driver.execute_script("arguments[0].click();", coupon_button)

        check_box = driver.find_element(By.XPATH,
                                        '//*[@id="contents"]/div/div/div[1]/div[2]/div[2]/form/div[2]/div[1]/label/div/input')
        driver.execute_script("arguments[0].click();", check_box)

        spam = driver.find_element(By.XPATH, '//*[@id="spam"]')
        driver.execute_script("arguments[0].focus();", spam)
    except Exception as e:
        messagebox.showerror("크롤링 실패", f"에러 발생: {e}")

# 대기 취소
def cancel_waiting():
    """대기 상태를 취소"""
    global waiting
    waiting = False
    messagebox.showinfo("대기 취소", "대기가 취소되었습니다.")
    countdown_label.config(text="")  # 남은 시간 표시 초기화

# 전화번호 입력 검증
def validate_phone_input(new_value):
    if new_value.isdigit() and len(new_value) <= 4:
        return True
    return new_value == ""  # 빈 입력도 허용

def update_countdown():
    """남은 시간을 계산하고 표시"""
    global waiting
    if not waiting:  # 대기 상태가 아니면 업데이트 중단
        countdown_label.config(text="")
        return

    current_time = time.strftime("%H:%M:%S")
    target_time = "19:00:00"

    # 현재 시간과 목표 시간 비교
    current_struct = time.strptime(current_time, "%H:%M:%S")
    target_struct = time.strptime(target_time, "%H:%M:%S")
    remaining_seconds = time.mktime(target_struct) - time.mktime(current_struct)

    if remaining_seconds <= 0:
        countdown_label.config(text="예약 시간이 되었습니다!")
        waiting = False
        return

    # 남은 시간을 시:분:초로 계산
    hours, remainder = divmod(int(remaining_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown_label.config(text=f"남은 시간: {hours}시간 {minutes}분 {seconds}초")

    # 1초마다 업데이트
    countdown_label.after(1000, update_countdown)

# tkinter 창 생성
root = tk.Tk()
root.title("방탈출 예약 프로그램")
root.geometry("1000x1000")
root.configure(bg="#343a40")

# ttk 스타일 설정
style = ttk.Style(root)
style.theme_use('clam')  # 기본 테마 설정

# 선택된 날짜 스타일 변경
style.map('TButton', background=[('active', '#0056b3')])  # 활성화 시 색상
style.configure('Calendar.TButton',
                background="#0056b3",  # 선택된 날짜 배경색
                foreground="#cd231d",  # 선택된 날짜 텍스트 색상
                font=('Arial', 12, 'bold'))  # 폰트 스타일

main_frame = tk.Frame(root, bg="#212529", padx=20, pady=20, relief="solid", bd=1)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# 테마 선택
tk.Label(main_frame, text="테마 선택:", font=("Arial", 14), bg="#212529", fg="#ffffff").pack(anchor="w", pady=10)
combo_theme = ttk.Combobox(main_frame, values=list(theme_times.keys()), font=("Arial", 12), state="readonly")
combo_theme.pack(fill="x")
combo_theme.bind("<<ComboboxSelected>>", update_theme)
combo_theme.set(list(theme_times.keys())[0])

# 테마 이미지
theme_image_label = tk.Label(main_frame, bg="#212529")
theme_image_label.pack(pady=20)

# 예약자 정보
tk.Label(main_frame, text="예약자 성함:", font=("Arial", 12), bg="#212529",state="normal", fg="#ffffff").pack(anchor="w")
entry_name = tk.Entry(main_frame, font=("Arial", 12))
entry_name.pack(fill="x", pady=5)

# 전화번호 입력
tk.Label(main_frame, text="전화번호:", font=("Arial", 12), bg="#212529", fg="#ffffff").pack(anchor="w")
frame_phone = tk.Frame(main_frame, bg="#212529")
frame_phone.pack(fill="x", pady=5)

entry_phone1 = tk.Entry(frame_phone, font=("Arial", 12), width=6, justify="center")
entry_phone1.insert(0, "010")
entry_phone1.pack(side="left", padx=2)

validate_command = main_frame.register(validate_phone_input)
entry_phone2 = tk.Entry(frame_phone, font=("Arial", 12), width=5, justify="center", validate="key", validatecommand=(validate_command, "%P"))
entry_phone2.pack(side="left", padx=2)

entry_phone3 = tk.Entry(frame_phone, font=("Arial", 12), width=5, justify="center", validate="key", validatecommand=(validate_command, "%P"))
entry_phone3.pack(side="left", padx=2)

# 예약 날짜
tk.Label(main_frame, text="예약 날짜:", font=("Arial", 12), bg="#212529", fg="#ffffff").pack(anchor="w", pady=5)
calendar = Calendar(main_frame, selectmode='day', date_pattern='yyyy-mm-dd', # 달력 헤더 배경색 (월, 연도 표시 부분) (기본: 'lightgray')
                    background="#343a40",  # 헤더 배경색
                    foreground="#ac1dae")
calendar.pack(fill="x", pady=5)

# 예약 시간
tk.Label(main_frame, text="예약 시간:", font=("Arial", 12), bg="#212529", fg="#ffffff").pack(anchor="w", pady=5)
combo_time = ttk.Combobox(main_frame, font=("Arial", 12), state="readonly")
combo_time.pack(fill="x")

# 예약 인원
tk.Label(main_frame, text="예약 인원:", font=("Arial", 12), bg="#212529", fg="#ffffff").pack(anchor="w", pady=5)
combo_people = ttk.Combobox(main_frame, values=["2", "3", "4", "5", "6"], font=("Arial", 12), state="readonly")
combo_people.pack(fill="x", pady=5)
combo_people.set("2")  # 기본값 설정

# 쿠폰
tk.Label(main_frame, text="쿠폰(선택):", font=("Arial", 12), bg="#212529",state="normal", fg="#ffffff").pack(anchor="w")
entry_coupon = tk.Entry(main_frame, font=("Arial", 12))
entry_coupon.pack(fill="x", pady=5)

# 남은 시간 표시 라벨 추가
countdown_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#212529", fg="#ffffff")
countdown_label.pack(pady=10)


# 대기 시작 버튼
btn_start = tk.Button(
    main_frame,
    text="대기 시작",
    command=start_waiting,  # 대기 시작 함수 호출
    font=("Arial", 14, "bold"),
    bg="#007bff",  # 파란색 버튼
    fg="#ffffff",  # 흰색 텍스트
    padx=20,
    pady=10,
    relief="raised",
    activebackground="#0056b3",  # 클릭 시 진한 파란색
    activeforeground="#ffffff"
)
btn_start.pack(pady=10)


# 대기 취소 버튼
btn_cancel_waiting = tk.Button(
    main_frame,
    text="대기 취소",
    command=cancel_waiting,  # 대기 취소 함수 호출
    font=("Arial", 14, "bold"),
    bg="#ffc107",  # 노란색 버튼
    fg="#212529",  # 어두운 텍스트
    padx=20,
    pady=10,
    relief="raised",
    activebackground="#e0a800",  # 클릭 시 진한 노란색
    activeforeground="#212529"
)
btn_cancel_waiting.pack(pady=10)

update_theme(None)

root.mainloop()