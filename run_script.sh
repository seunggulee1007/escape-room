#! /bin/bash

# 그림자 없는 상자    사람들은 그것을 행복이라 부르기로 했다
# 10:00           10:20
# 11:30           11:50
# 13:00           13:20
# 14:30           14:50
# 16:00           16:20
# 17:30           17:50
# 19:00           19:20
# 20:30           20:50
# 22:00           22:20

# 매개변수 설정
TIME="" # 위의 시간을 입력
DAY="" # 원하는 날짜 입력. 보통 현재 일자 기준 1주일 뒤가 열림
USER_ID="" # 단편선 아이디
PASSWORD="" # 단편선 비밀번호
PHONE_NUMBER="" # 예약시 입력할 휴대폰 번호
PERSON=4 # 입장할 인원

./dist/main "$TIME" "$DAY" "$USER_ID" "$PASSWORD" "$PHONE_NUMBER" "$PERSON"