import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class KeyEscape:
    def __init__(self):
        self.driver = None

    def open_chrome(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def reservation(self):
        driver = self.driver
        driver.get('https://www.keyescape.co.kr/web/home.php?go=rev.make')
        driver.implicitly_wait(10) # 화면이 다 뜰때까지 대기
        target_day = 27
        store = driver.find_element(By.XPATH, "//li[text()='강남 더오름']")
        store.click()
        time.sleep(1)
        day_element = driver.find_element(By.XPATH, f"//a[text()='{target_day}']")
        day_element.click()
        driver.implicitly_wait(15)  # 화면이 다 뜰때까지 대기
        driver.find_element(By.XPATH, '//*[@id="theme_data"]/a[2]/li').click()
        driver.implicitly_wait(15)  # 화면이 다 뜰때까지 대기
        time_element = driver.find_element(By.XPATH, "//li[@class='possible' and text()='19:00  ']")
        time_element.click()

        form = driver.find_element(By.NAME, "register")  # 폼의 name 속성이 'register'
        form.submit()

        name = driver.find_element(By.NAME, 'name')
        name.send_keys('이승구')
        driver.find_element(By.NAME, 'mobile2').send_keys('2432')
        driver.find_element(By.NAME, 'mobile3').send_keys('9232')
        select_element = driver.find_element(By.NAME, 'person')
        select = Select(select_element)
        select.select_by_value('4')  # value가 '4'인 옵션 선택

        # 1. CAPTCHA 이미지 다운로드
        captcha_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha_img"))
        )
        time.sleep(2)  # 이미지를 완전히 렌더링할 시간을 주기 위해 대기


        # 3. 이미지 요소의 위치와 크기를 가져옴
        location = captcha_img.location
        size = captcha_img.size

        # 4. 페이지 전체 스크린샷 찍기
        driver.save_screenshot('full_screenshot.png')

        # 5. 스크린샷에서 CAPTCHA 이미지 부분만 자르기
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        # 이미지를 열고 해당 영역을 자름
        full_img = Image.open('full_screenshot.png')
        img = full_img.crop((x, y, x + width, y + height))
        img.save('/Users/nhn/Desktop/DEV/captcha.png')
        # 2. 이미지 전처리 (흑백 변환 및 선명도 조정)
        # 흑백 변환
        img = img.convert('L')

        # 대비 증가
        img = ImageEnhance.Contrast(img).enhance(2)

        # 노이즈 제거
        img = img.filter(ImageFilter.MedianFilter())

        # 이미지 크기 확대 (해상도 증가)
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)

        # 3. Tesseract 설정 (숫자만 인식하도록 제한)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

        # 4. OCR 수행
        captcha_text = pytesseract.image_to_string(img, config=custom_config)

        # 결과 출력
        print("추출된 숫자:", captcha_text.strip())

        # 3. 추출한 숫자를 입력란에 입력
        captcha_input = driver.find_element(By.NAME, "input_captcha")  # 실제 캡차 입력 필드의 name이나 id로 변경
        captcha_input.send_keys(captcha_text.strip())  # 추출된 텍스트를 입력란에 입력


if __name__ == '__main__':
    key_escape = KeyEscape()
    key_escape.open_chrome()
    key_escape.reservation()
