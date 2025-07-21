# 🗺️ 경로찾기 프로젝트 컬렉션

이 저장소는 두 개의 독립적인 경로찾기 프로젝트를 포함하고 있습니다.

## 📁 프로젝트 구조

```
pathfinding_project/
├── coffee_pathfinding_project/         # ☕ 커피 경로찾기 프로젝트 (새로운 요구사항)
│   ├── dataFile/                       # 데이터 파일들
│   ├── caffee_map_detailed.py          # 1단계: 데이터 분석 (상세 주석)
│   ├── map_draw_detailed.py            # 2단계: 지도 시각화 (상세 주석)
│   ├── map_direct_save_detailed.py     # 3단계: 경로 탐색 (상세 주석)
│   ├── caffee_map.py                   # 1단계: 데이터 분석 (기본 버전)
│   ├── map_draw.py                     # 2단계: 지도 시각화 (기본 버전)
│   ├── map_direct_save.py              # 3단계: 경로 탐색 (기본 버전)
│   ├── map.png                         # 기본 지도
│   ├── map_final.png                   # 경로가 표시된 지도
│   ├── home_to_cafe.csv                # 경로 데이터
│   ├── README.md                       # 프로젝트 설명서
│   └── requirements.txt                # 필요한 라이브러리
├── original_pathfinding_project/       # 🏗️ 원본 경로찾기 프로젝트
│   ├── pathfinding_system.py           # 기본 경로찾기 시스템
│   ├── pathfinding_system_detailed.py  # 상세 주석 버전
│   ├── pathfinding_system_fixed.py     # 오류 수정 버전
│   ├── interactive_pathfinding.py      # 대화형 경로찾기
│   ├── buildings.csv                   # 건물 데이터
│   ├── roads.csv                       # 도로 데이터
│   ├── construction_sites.csv          # 건설 현장 데이터
│   ├── path_*.csv                      # 경로 결과 파일들
│   ├── path_*.png                      # 경로 시각화 파일들
│   ├── map_visualization.png           # 지도 시각화
│   ├── README.md                       # 프로젝트 설명서
│   ├── 코딩_초보자를_위한_상세_가이드.md  # 초보자 가이드
│   ├── 라이브러리_및_프로그램_목록.md    # 라이브러리 설명
│   └── PROJECT_CHECKLIST.md            # 프로젝트 체크리스트
└── dataFile/                           # 공통 데이터 파일들
    ├── area_map.csv                    # 지역 지도 데이터
    ├── area_struct.csv                 # 구조물 데이터
    └── area_category.csv               # 구조물 분류 데이터
```

## ☕ 커피 경로찾기 프로젝트 (새로운 요구사항)

### 📋 프로젝트 개요
내 집에서 반달곰 커피까지의 최단 경로를 찾는 프로그램입니다.

### 🎯 주요 특징
- **3단계 구조**: 데이터 분석 → 지도 시각화 → 경로 탐색
- **상세한 주석**: 코딩 초보자도 이해할 수 있도록 작성
- **BFS 알고리즘**: 최단 경로 탐색 구현
- **실제 데이터**: CSV 파일을 사용한 실용적인 프로젝트

### 🚀 실행 방법
```bash
cd coffee_pathfinding_project

# 1단계: 데이터 분석
python caffee_map_detailed.py

# 2단계: 지도 시각화
python map_draw_detailed.py

# 3단계: 경로 탐색
python map_direct_save_detailed.py
```

### 📊 결과 파일
- `map.png`: 기본 지도 시각화
- `map_final.png`: 경로가 표시된 지도
- `home_to_cafe.csv`: 경로 데이터

### 🎨 시각화 규칙
| 구조물 | 모양 | 색상 | 설명 |
|--------|------|------|------|
| 아파트/빌딩 | 원형 | 갈색 | 장애물 |
| 반달곰 커피 | 사각형 | 녹색 | 목적지 |
| 내 집 | 삼각형 | 녹색 | 시작점 |
| 건설 현장 | 사각형 | 회색 | 장애물 |

## 🏗️ 원본 경로찾기 프로젝트

### 📋 프로젝트 개요
다양한 경로찾기 알고리즘을 구현한 종합적인 시스템입니다.

### 🎯 주요 특징
- **다중 알고리즘**: BFS, 다익스트라 알고리즘 구현
- **대화형 인터페이스**: 사용자 입력을 받는 인터랙티브 모드
- **상세한 문서**: 초보자를 위한 가이드와 라이브러리 설명
- **오류 처리**: 타입 힌트와 예외 처리

### 🚀 실행 방법
```bash
cd original_pathfinding_project

# 기본 시스템 실행
python pathfinding_system_fixed.py

# 대화형 모드
python interactive_pathfinding.py
```

### 📊 결과 파일
- `path_BFS_*.csv/png`: BFS 알고리즘 결과
- `path_다익스트라_*.csv/png`: 다익스트라 알고리즘 결과
- `map_visualization.png`: 지도 시각화

## 🛠️ 기술 스택

### 공통 라이브러리
- **Python 3**: 메인 프로그래밍 언어
- **pandas**: 데이터 처리 및 분석
- **matplotlib**: 그래프 및 지도 시각화

### 추가 라이브러리
- **collections.deque**: BFS 알고리즘용 큐
- **heapq**: 다익스트라 알고리즘용 우선순위 큐

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
- 타입 힌트를 통한 코드 안정성

## 🎓 학습 포인트

### 데이터 처리
- CSV 파일 읽기 및 병합
- 데이터 필터링 및 정렬
- 구조물 ID 매핑

### 시각화
- matplotlib을 사용한 그래프 그리기
- 좌표계 설정 및 변환
- 범례 및 라벨 설정

### 알고리즘
- BFS 알고리즘 구현
- 다익스트라 알고리즘 구현
- 2D 격자에서의 경로 탐색
- 장애물 처리

### Python 프로그래밍
- 함수 정의 및 호출
- 타입 힌트 사용
- 예외 처리
- 파일 입출력
- 클래스와 객체 지향 프로그래밍

## 🔧 설치 및 실행

### 1. 라이브러리 설치
```bash
pip install -r coffee_pathfinding_project/requirements.txt
```

### 2. 프로젝트 실행
각 프로젝트 폴더로 이동하여 해당 README.md 파일을 참조하세요.

## 📚 추가 학습 자료

- [pandas 공식 문서](https://pandas.pydata.org/)
- [matplotlib 공식 문서](https://matplotlib.org/)
- [BFS 알고리즘 설명](https://en.wikipedia.org/wiki/Breadth-first_search)
- [다익스트라 알고리즘 설명](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python 타입 힌트](https://docs.python.org/3/library/typing.html)

## 👨‍💻 작성자

AI Assistant
- 상세한 주석과 설명으로 코딩 초보자도 이해할 수 있도록 작성
- 실제 데이터를 사용한 실용적인 프로젝트
- 단계별 학습이 가능한 구조
- 두 가지 다른 요구사항에 맞춘 독립적인 프로젝트

---

**이 저장소는 데이터 분석, 시각화, 알고리즘 구현을 모두 포함한 종합적인 학습 자료입니다.** 