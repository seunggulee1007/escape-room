
import argparse
from datetime import datetime
import time

def wait_until_midnight():
    while True:
        # 현재 시간을 확인
        now = datetime.now()
        # 00:00:00 정각인지 확인
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            print("It's midnight! Executing the next code...")
            break
        # 1초 대기 후 다시 확인
        time.sleep(1)
from danpyeon import DanPyeon

# 정각까지 대기하는 함수


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