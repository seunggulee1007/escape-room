from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import argparse

from selenium.common.exceptions import NoAlertPresentException

# 정각까지 대기하는 함수
def wait_until_midnight():
    while True:
        # 현재 시간을 확인
        now = datetime.now()
        # 00:00:00 정각인지 확인
        if now.hour == 17 and now.minute == 33 and now.second == 0:
            print("It's midnight! Executing the next code...")
            break
        # 1초 대기 후 다시 확인
        time.sleep(1)

def get_room_time(time_str: str) -> str:
    match time_str:
        case "10:30":
            return "25"
        case "10:15":
            return "36"
        case "10:00":
            return "47"
        case "12:00":
            return "5"
        case "11:45":
            return "35"
        case "11:30":
            return "46"
        case "13:30":
            return "6"
        case "13:15":
            return "34"
        case "13:00":
            return "45"
        case "15:00":
            return "7"
        case "14:45":
            return "33"
        case "14:30":
            return "44"
        case "16:30":
            return "8"
        case "16:15":
            return "32"
        case "16:00":
            return "43"
        case "18:00":
            return "9"
        case "17:45":
            return "31"
        case "17:30":
            return "42"
        case "19:30":
            return "10"
        case "19:15":
            return "30"
        case "19:00":
            return "41"
        case "21:00":
            return "11"
        case "20:45":
            return "29"
        case "20:30":
            return "40"
        case "22:30":
            return "12"
        case "22:15":
            return "28"
        case "22:00":
            return "39"
        case _:
            return "Time not found"

def get_room_time_kangnam(time_str):
    match time_str:
        case "10:00":
            return "25"
        case "10:20":
            return "36"
        case "11:30":
            return "5"
        case "11:50":
            return "35"
        case "13:00":
            return "6"
        case "13:20":
            return "34"
        case "14:30":
            return "7"
        case "14:50":
            return "33"
        case "16:00":
            return "8"
        case "16:20":
            return "32"
        case "17:30":
            return "9"
        case "17:50":
            return "31"
        case "19:00":
            return "10"
        case "19:20":
            return "30"
        case "20:30":
            return "11"
        case "20:50":
            return "29"
        case "22:00":
            return "12"
        case "22:20":
            return "28"
        case _:
            return "Invalid time"


class DanPyeon:
    def __init__(self):
        self.driver = None

    def open_chrome(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
    def login(self, idx, day, user_id, pwd, is_kangnam=True):
        idx = self.get_by_room_time(idx, is_kangnam)
        url = self.get_url_by_kangnam(day, idx, is_kangnam)

        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.close_alert_until_none()
        self.driver.find_element(By.LINK_TEXT, "로그인").click()
        self.driver.implicitly_wait(10)
        username = self.driver.find_element(By.NAME, "uid")

        username.send_keys(user_id)
        input_password = self.driver.find_element(By.NAME, "passwd")
        input_password.send_keys(pwd)

        input_password.send_keys(Keys.RETURN)
        time.sleep(1)
        self.close_alert_until_none()

    def get_url_by_kangnam(self, day, idx, is_kangnam):
        url = "https://dpsnnn-s.imweb.me/reserve_ss"
        if is_kangnam:
            url = "https://www.dpsnnn.com/reserve_g"
        parameter = "?idx=" + idx + "&day=" + day
        return url + parameter

    def get_by_room_time(self, idx, is_kangnam):
        if is_kangnam:
            idx = get_room_time_kangnam(idx)
        else:
            idx = get_room_time(idx)
        return idx

    # alert 창이 모두 닫힐때 까지 닫음
    def close_alert_until_none(self, is_click=False, max_attempts=10, wait_time=1):
        attempts = 0
        while attempts < max_attempts:
            try:
                if is_click:
                    # 버튼 클릭
                    button = self.driver.find_element(By.LINK_TEXT, "예약하기")
                    button.click()
                    print("Button clicked.")
                # alert 창으로 전환
                alert = self.driver.switch_to.alert
                # alert 닫기
                alert.accept()  # 또는 alert.dismiss()를 사용할 수 있다.
                print("Alert was closed.")
                # 일정 시간 대기 (alert 창이 다시 나타날 수 있으니 대기)
                time.sleep(wait_time)
            except NoAlertPresentException:
                # 더 이상 alert 창이 없을 때 루프를 종료
                print("No more alert found.")
                break
            attempts += 1
        if attempts == max_attempts:
            print("Max attempts reached. Alert may still be present.")

    def reservation(self, phone_number, person, is_kangnam=True):

        self.close_alert_until_none(is_click=True)

        self.driver.implicitly_wait(10)

        call = self.driver.find_element(By.NAME, "orderer_call")
        call.send_keys(phone_number)
        person_cnt = str(int(person)+1)
        radio_path = '//*[@id="shopFormWrap"]/div/div['+person_cnt+']/label'
        if is_kangnam:
            radio_path = '//*[@id="shopFormWrap"]/div/div['+str(int(person)+1)+']/label/span'
        # //*[@id="shopFormWrap"]/div/div[6]/label/span

        radio_button = self.driver.find_element(By.XPATH, radio_path)
        radio_button.click()

        # //*[@id="order_form_wrap"]/div[1]/div[4]/div/div/div/div/div/label/span
        # name 속성이 'agree_cancel'인 체크박스 선택 및 클릭
        agree_cancel = self.driver.find_element(By.XPATH, '//*[@id="order_form_wrap"]/div[1]/div[4]/div/div/div/div/div/label/span')
        agree_cancel.click()

        # id 속성이 'paymentAllCheck'인 체크박스 선택 및 클릭
        payment_all_check = self.driver.find_element(By.XPATH, '//*[@id="order_form_wrap"]/div[2]/div[4]/div/div[1]/label/span')
        payment_all_check.click()

        # self.driver.find_element(By.LINK_TEXT, "결제하기").click()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process multiple arguments.")

    parser.add_argument("time", help="방탈출 시간을 입력합니다.")
    parser.add_argument("day", help="방탈출 날짜를 입력해 줍니다. 포맷은 'yyyy-MM-dd'")
    parser.add_argument("user_id", help="단편선 로그인 아이디를 입력합니다.")
    parser.add_argument("password", help="단편선 로그인 비밀번호를 입력합니다.")
    parser.add_argument("phone_number", help="예약시 입력할 전화번호를 입력합니다.('-'을 제외하고 입력합니다).")
    parser.add_argument("person", help="예약시 입력할 전화번호를 입력합니다.('-'을 제외하고 입력합니다).")
    parser.add_argument("is_kangnam", help="강남인지 여부를 입력합니다. 기본값은 True입니다.")
    args = parser.parse_args()
    request_time = args.time

    request_day = args.day
    user = args.user_id
    password = args.password
    response_phone = args.phone_number
    request_person = args.person
    kangnam = args.is_kangnam == "True"

    danPyeon = DanPyeon()
    danPyeon.open_chrome()
    danPyeon.login(idx=request_time, day=request_day, user_id=user, pwd=password, is_kangnam=kangnam)
    # 정각까지 대기
    wait_until_midnight()

    # 예약 프로세스 시작
    danPyeon.reservation(response_phone, request_person, kangnam)