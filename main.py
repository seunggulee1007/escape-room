from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

class DanPyeon:
    def __init__(self):
        self.driver = None

    def open_chrome(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
    def login(self, idx, day):
        #self.driver.get("https://www.dpsnnn.com/reserve_g")
        self.driver.get("https://www.dpsnnn.com/reserve_g/?idx="+idx+"&day="+day)
        self.driver.implicitly_wait(10)
        self.closeAlert()
        self.driver.find_element(By.LINK_TEXT, "로그인").click()
        self.driver.implicitly_wait(10)
        username = self.driver.find_element(By.NAME, "uid")

        username.send_keys("leesg107@naver.com")
        password = self.driver.find_element(By.NAME, "passwd")
        password.send_keys("chldPfls1!")

        password.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(20)
        self.closeAlert()


    def go_reservation_page(self, idx, day):
        self.driver.get("https://www.dpsnnn.com/reserve_g/?idx="+idx+"&day="+day)
        self.driver.implicitly_wait(10)

    def closeAlert(self):
        if EC.alert_is_present():
            try:
                result = self.driver.switch_to.alert
                result.accept()
            except:
                pass
if __name__ == '__main__':
    danPyeon = DanPyeon()
    danPyeon.open_chrome()
    danPyeon.login("25", "2024-09-18")
    # 그림자 없는 상자    사람들은 그것을 행복이라 부르기로 했다
    # 10:00 25          10:20 36
    # 11:30 5           11:50 35
    # 13:00 6           13:20 34
    # 14:30 7           14:50 33
    # 16:00 8           16:20 32
    # 17:30 9           17:50 31
    # 19:00 10          19:20 30
    # 20:30 11          20:50 29
    # 22:00 12          22:20 28
    # danPyeon.go_reservation_page(idx="36", day="2024-09-18")