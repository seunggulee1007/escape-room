# escape-room

방탈출 예약 하는 프로젝트<br/>

현재는 단편선 하나만 예약을 할 수 있다.

## 1. 강남

### 1-1 시간표
| 순번 | 그림자 없는 상자 | 사람들은 그것을 행복이라 부르기로 했다|
|----|-----------|--|
| 1  | 10:00     |           10:20|
| 2  | 11:30     |           11:50|
| 3  | 13:00     |           13:20|
| 4  | 14:30     |           14:50|
| 5  | 16:00     |           16:20|
| 6  | 17:30     |           17:50|
| 7  | 19:00     |           19:20|
| 8  | 20:30     |           20:50|
| 9  | 22:00     |           22:20|

## 2. 성수
| 순번 | 쓰여진 문장 속에 구원이 없다면 | 존재할 자격| 뱃사람의 별 |
|----|-------------------|--|--|
| 1  | 10:30| 10:15| 10:00|
| 2  | 12:00 | 11:45| 11:30|
| 3  | 13:30 | 13:15| 13:00|
| 4  | 15:00 | 14:45| 14:30|
| 5  | 16:30 | 16:15| 16:00|
| 6  | 18:00 | 17:45| 17:30|
| 7  | 19:30 | 19:15| 19:00|
| 8  | 21:00 | 20:45| 20:30|
| 9  | 22:30 | 22:15| 22:00|

## 3 실행파일 위치
dist/main <br/>
`run_script.sh`내부에 매개변수를 설정하고 실행하면 된다.
### 매개변수 설정
``` bash
TIME="" # 위의 시간을 입력
DAY="" # 원하는 날짜 입력. 보통 현재 일자 기준 1주일 뒤가 열림
USER_ID="" # 단편선 아이디
PASSWORD="" # 단편선 비밀번호
PHONE_NUMBER="" # 예약시 입력할 휴대폰 번호
PERSON=4 # 입장할 인원 ( 강남은 최대 5명, 성수는 최대 6명 까지 가능 )
IS_KANGNAM=True # 강남 여부
```