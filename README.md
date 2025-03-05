# Calendar

이 프로젝트는 Flask를 사용하여 만든 일정 관리 애플리케이션입니다. 사용자는 일정을 추가, 수정, 삭제할 수 있으며, 검색 및 카테고리 필터링 기능도 제공합니다.

## 설치 및 실행 방법

1. 저장소를 클론합니다:
    ```sh
    git clone https://github.com/your-repo/calendar.git
    cd calendar
    ```

2. 가상 환경을 생성하고 활성화합니다:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```
    - Windows에서는 `venv\Scripts\activate` 실행

3. 필요한 패키지를 설치합니다:
    ```sh
    pip install -r requirements.txt
    ```

4. 환경 변수를 설정합니다:  
   `.env` 파일을 생성하고 다음 내용을 추가합니다.
    ```env
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///your-database.db
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_password
    ```

5. 데이터베이스를 초기화합니다:
    ```sh
    flask db upgrade
    ```

6. 애플리케이션을 실행합니다:
    ```sh
    flask run
    ```

## 📂 파일 구조
```sh
📂 프로젝트 루트
├── app.py             # Flask 애플리케이션 설정 및 라우팅
├── create_user.py     # 사용자 생성 스크립트
├── example.py         # SQLite 예제 스크립트
├── extensions.py      # 확장 모듈 (SQLAlchemy)
├── forms.py           # Flask-WTF 폼 정의
├── models.py          # 데이터베이스 모델 정의
├── requirements.txt   # 필요한 패키지 목록
├── migrations/        # 데이터베이스 마이그레이션 파일
│
├── static/            # 정적 파일 (CSS, JS)
│   ├── fullcalendar.js  # FullCalendar 라이브러리
│   └── styles.css       # 스타일 시트
│
├── templates/         # HTML 템플릿
│   ├── base.html        # 기본 템플릿
│   ├── calendar.html    # 캘린더 페이지
│   ├── event_form.html  # 일정 추가/수정 폼
│   ├── login.html       # 로그인 페이지
│   ├── profile.html     # 프로필 수정 페이지
│   └── register.html    # 회원가입 페이지
```

## 주요 기능

- **회원가입 및 로그인**: 사용자는 회원가입 후 로그인할 수 있습니다.
- **일정 관리**: 일정을 추가, 수정, 삭제할 수 있습니다.
- **검색 및 필터링**: 일정 제목, 설명, 태그를 검색하고 카테고리로 필터링할 수 있습니다.
- **다크 모드**: 다크 모드와 라이트 모드를 전환할 수 있습니다.

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 만듭니다:
    ```sh
    git checkout -b feature/your-feature
    ```
3. 변경 사항을 커밋합니다:
    ```sh
    git commit -am "Add some feature"
    ```
4. 브랜치에 푸시합니다:
    ```sh
    git push origin feature/your-feature
    ```
5. 풀 리퀘스트를 생성합니다.
