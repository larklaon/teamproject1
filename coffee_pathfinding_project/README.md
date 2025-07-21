# ☕ 커피 경로찾기 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 내 집에서 반달곰 커피까지의 최단 경로를 찾는 프로그램입니다. 
실제 지도 데이터를 분석하고, 시각화하며, 최단 경로 알고리즘을 구현하여 경로를 찾습니다.

## 🎯 프로젝트 목표

1. **데이터 분석**: CSV 파일들을 읽고 분석하여 지도 데이터 생성
2. **지도 시각화**: 구조물들을 구분하여 지도에 표시
3. **경로 탐색**: BFS 알고리즘으로 최단 경로 찾기

## 📁 파일 구조

```
coffee_pathfinding_project/
├── dataFile/                          # 데이터 파일들 (상위 디렉토리에 위치)
│   ├── area_map.csv                   # 지역과 좌표 정보
│   ├── area_struct.csv                # 구조물 위치와 종류
│   └── area_category.csv              # 구조물 종류 매핑
├── caffee_map_detailed.py             # 1단계: 데이터 분석 (상세 주석)
├── map_draw_detailed.py               # 2단계: 지도 시각화 (상세 주석)
├── map_direct_save_detailed.py        # 3단계: 경로 탐색 (상세 주석)
├── caffee_map.py                      # 1단계: 데이터 분석 (기본 버전)
├── map_draw.py                        # 2단계: 지도 시각화 (기본 버전)
├── map_direct_save.py                 # 3단계: 경로 탐색 (기본 버전)
├── test_all.py                        # 전체 테스트 스크립트
├── map.png                            # 기본 지도
├── map_final.png                      # 경로가 표시된 지도
├── home_to_cafe.csv                   # 경로 데이터
├── area1_analyzed_data.csv            # 분석된 데이터
├── README.md                          # 프로젝트 설명서
└── requirements.txt                   # 필요한 라이브러리
```

## 🚀 실행 방법

### 방법 1: 개별 실행 (권장)
```bash
# 상위 디렉토리에서 실행
cd pathfinding_project

# 1단계: 데이터 분석
python coffee_pathfinding_project/caffee_map_detailed.py

# 2단계: 지도 시각화
python coffee_pathfinding_project/map_draw_detailed.py

# 3단계: 경로 탐색
python coffee_pathfinding_project/map_direct_save_detailed.py
```

### 방법 2: 전체 테스트
```bash
# 모든 단계를 한 번에 실행
python coffee_pathfinding_project/test_all.py
```

## 📊 데이터 구조

### area_map.csv
- **x, y**: 좌표
- **ConstructionSite**: 건설 현장 여부 (0: 없음, 1: 있음)

### area_struct.csv
- **x, y**: 좌표
- **category**: 구조물 종류 ID
- **area**: 지역 번호

### area_category.csv
- **category**: 구조물 종류 ID
- **struct**: 구조물 이름

## 🎨 시각화 규칙

| 구조물 | 모양 | 색상 | 설명 |
|--------|------|------|------|
| 아파트/빌딩 | 원형 | 갈색 | 장애물 (이동 불가) |
| 반달곰 커피 | 사각형 | 녹색 | 목적지 |
| 내 집 | 삼각형 | 녹색 | 시작점 |
| 건설 현장 | 사각형 | 회색 | 장애물 (이동 불가) |

## 🔍 알고리즘 설명

### BFS (Breadth-First Search)
- **개념**: 시작점에서 가까운 곳부터 차례대로 탐색
- **특징**: 최단 경로를 보장
- **이동**: 8방향 (상하좌우 + 대각선)
- **장애물**: 건설 현장, 아파트, 빌딩

### 알고리즘 동작 과정
1. 시작점을 큐에 넣고 방문 표시
2. 큐에서 위치를 꺼내서 8방향으로 이동 시도
3. 유효하고 방문하지 않은 위치를 큐에 추가
4. 도착점에 도달하면 경로 반환

## 📈 결과 파일

### home_to_cafe.csv
경로 데이터를 담은 CSV 파일
- **step**: 단계 번호
- **x, y**: 좌표
- **coordinate**: 좌표 문자열

### map.png
기본 지도 시각화

### map_final.png
경로가 표시된 최종 지도

### area1_analyzed_data.csv
1단계에서 생성된 분석 데이터

## 🛠️ 기술 스택

- **Python 3**: 메인 프로그래밍 언어
- **pandas**: 데이터 처리 및 분석
- **matplotlib**: 그래프 및 지도 시각화
- **collections.deque**: BFS 알고리즘용 큐

## 📝 코드 특징

### 상세한 주석
- 모든 함수와 주요 코드 블록에 설명 추가
- 코딩 초보자도 이해할 수 있도록 작성
- 알고리즘 동작 과정 상세 설명

### 모듈화
- 각 단계별로 독립적인 파일로 구성
- 함수별로 명확한 역할 분담
- 재사용 가능한 코드 구조

### 오류 처리
- 파일 없음, 데이터 오류 등 예외 상황 처리
- 사용자 친화적인 오류 메시지
- Windows 환경 호환성 (유니코드 이모지 제거)

## 🎓 학습 포인트

### 데이터 처리
- CSV 파일 읽기 및 병합
- 데이터 필터링 및 정렬
- 구조물 ID 매핑
- 공백 처리 및 데이터 정제

### 시각화
- matplotlib을 사용한 그래프 그리기
- 좌표계 설정 및 변환
- 범례 및 라벨 설정

### 알고리즘
- BFS 알고리즘 구현
- 2D 격자에서의 경로 탐색
- 장애물 처리

### Python 프로그래밍
- 함수 정의 및 호출
- 타입 힌트 사용
- 예외 처리
- 파일 입출력

## 🔧 문제 해결

### 자주 발생하는 문제

1. **파일을 찾을 수 없음**
   - `dataFile` 폴더가 상위 디렉토리에 있는지 확인
   - 파일 경로가 올바른지 확인

2. **경로를 찾을 수 없음**
   - 시작점이나 도착점이 장애물 위에 있는지 확인
   - 격자 범위를 벗어나지 않았는지 확인

3. **시각화가 안 됨**
   - matplotlib 백엔드 설정 확인
   - 필요한 라이브러리 설치 확인

4. **유니코드 오류**
   - Windows 환경에서 이모지 사용 시 발생
   - 해결: 이모지를 제거하고 텍스트로 대체

## 📚 추가 학습 자료

- [pandas 공식 문서](https://pandas.pydata.org/)
- [matplotlib 공식 문서](https://matplotlib.org/)
- [BFS 알고리즘 설명](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python 타입 힌트](https://docs.python.org/3/library/typing.html)

## 🖥️ 운영체제별 설치/실행 안내 (Mac/Windows/Ubuntu)

### Mac (맥)
- 설치 체크리스트: 맥_설치_체크리스트.md 참고
- 설치 가이드: 맥_환경_설치_가이드.md 참고

### Windows
- Python 3.x 설치 (Add to PATH 체크)
- 명령 프롬프트에서 python --version 확인
- 가상환경 생성: python -m venv coffee_env
- 활성화: coffee_env\Scripts\activate
- pip install --upgrade pip
- pip install pandas matplotlib
- 실행: python caffee_map.py, python map_draw.py, python map_direct_save.py
- 결과 파일: home_to_cafe.csv, map.png, map_final.png
- 문제 해결: PermissionError(관리자 권한), UnicodeError(경로/이모지 주의)

### Ubuntu
- sudo apt update && sudo apt install python3 python3-venv python3-pip
- python3 -m venv coffee_env
- source coffee_env/bin/activate
- pip install --upgrade pip
- pip install pandas matplotlib
- 실행: python3 caffee_map.py, python3 map_draw.py, python3 map_direct_save.py
- 결과 파일: home_to_cafe.csv, map.png, map_final.png
- 문제 해결: chmod +x *.py, pip install pandas matplotlib

## 🧹 불필요한 파일/결과 정리
- __pycache__, .DS_Store, coffee_env, .venv 등은 삭제해도 무방
- 결과 파일(home_to_cafe.csv, map.png, map_final.png, area1_analyzed_data.csv)은 필요시 삭제 가능

## 👨‍💻 작성자

AI Assistant
- 상세한 주석과 설명으로 코딩 초보자도 이해할 수 있도록 작성
- 실제 데이터를 사용한 실용적인 프로젝트
- 단계별 학습이 가능한 구조
- Windows 환경 호환성 고려

## ✅ 최근 수정사항

### 버그 수정
1. **구조물 이름 공백 문제**: CSV 파일의 구조물 이름에 있는 공백을 제거하여 매핑이 제대로 되도록 수정
2. **파일 경로 문제**: 상위 디렉토리에서 실행하도록 경로 설정
3. **유니코드 오류**: Windows 환경에서 이모지 사용 시 발생하는 오류 수정
4. **import 경로 문제**: 모듈 임포트 경로를 올바르게 설정
5. **타입 힌트 오류**: pandas map 함수 사용 시 발생하는 타입 힌트 오류 수정
6. **value_counts 오류**: pandas Series의 value_counts 메서드 사용 시 발생하는 타입 힌트 오류 수정
7. **iterrows 오류**: pandas DataFrame의 iterrows 메서드 사용 시 발생하는 타입 힌트 오류 수정
8. **agg 오류**: pandas groupby().agg() 메서드 사용 시 발생하는 타입 힌트 오류 수정
9. **반환 타입 오류**: 함수 반환 타입과 실제 반환값 간의 타입 힌트 불일치 오류 수정

### 기능 개선
1. **테스트 스크립트 추가**: `test_all.py`로 전체 프로젝트 테스트 가능
2. **오류 처리 강화**: 더 자세한 오류 메시지와 해결 방법 제공
3. **문서화 개선**: README 파일에 최신 정보 반영
4. **코드 안정성 향상**: 타입 힌트 오류 해결로 더 안정적인 코드

---

**이 프로젝트는 데이터 분석, 시각화, 알고리즘 구현을 모두 포함한 종합적인 학습 자료입니다.** 