from setuptools import setup

APP = ['bitforbia.py']  # 메인 스크립트 파일
DATA_FILES = []    # 필요한 리소스 파일 (예: 이미지, 텍스트 파일 등)
OPTIONS = {
    'argv_emulation': True,          # 명령줄 출력 지원
    'packages': ['tkinter'],         # 추가 패키지 명시
    # 'iconfile': 'app_icon.icns',     # (선택) 아이콘 파일 설정
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)