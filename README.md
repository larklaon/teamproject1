# 경로 탐색 알고리즘 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 실질적인 데이터를 분석하고 이를 지도화하며, 최종적으로 경로 탐색 알고리즘을 구현하는 완전한 시스템입니다.

## 🎯 주요 기능

### 1. CSV 데이터 처리
- **buildings.csv**: 건물 데이터 (10개)
- **roads.csv**: 도로 데이터 (20개)  
- **construction_sites.csv**: 건설현장 데이터 (6개)
- 세 개의 CSV 파일을 자동으로 병합 및 정렬

### 2. 카테고리 변환
- 숫자로 된 구조물 ID를 의미 있는 이름으로 변환
- 딕셔너리 기반 매핑 시스템
- 타입별: 1=건물, 2=도로, 3=건설현장

### 3. 시각화 좌표계 설계
- (1,1)이 좌상단, (x_max, y_max)가 우하단인 2D 격자 공간
- 50x50 기본 격자 크기 (데이터에 따라 자동 확장)
- 격자 번호 표시 및 그리드 라인

### 4. 도형별 조건 시각화
- **건물**: 파란색 사각형 (■)
- **도로**: 회색 원형 (●)  
- **건설현장**: 빨간색 삼각형 (▲)
- 겹침 우선순위: 건설현장 > 건물 > 도로

### 5. 이미지 저장
- matplotlib을 사용한 고해상도 PNG 파일 저장
- 지도 시각화 및 경로 탐색 결과 저장
- 300 DPI 고품질 출력

### 6. 최단 경로 알고리즘 구현
- **BFS (너비 우선 탐색)**: 직접 구현
- **다익스트라 알고리즘**: 직접 구현
- 외부 라이브러리 사용 금지
- 8방향 이동 지원 (상하좌우 + 대각선)

### 7. 장애물 처리
- 건물과 건설현장은 통과 불가
- 도로는 통과 가능
- 시작점/도착점이 장애물인 경우 오류 처리

### 8. 결과 저장
- 경로 결과를 CSV 파일로 출력
- 단계별 좌표 목록 저장
- UTF-8 인코딩 지원

## 🚀 실행 방법

### 1. 환경 설정
```bash
pip install -r requirements.txt
```

### 2. 자동 데모 실행
```bash
python pathfinding_system.py
```

### 3. 인터랙티브 모드 실행
```bash
python interactive_pathfinding.py
```

## 📁 파일 구조

```
pathfinding_project/
├── buildings.csv              # 건물 데이터
├── roads.csv                  # 도로 데이터
├── construction_sites.csv     # 건설현장 데이터
├── requirements.txt           # Python 패키지 의존성
├── pathfinding_system.py      # 메인 경로 탐색 시스템
├── interactive_pathfinding.py # 인터랙티브 사용자 인터페이스
└── README.md                  # 프로젝트 설명서
```

## 🔧 기술 스택

- **Python 3.8+**
- **Pandas**: CSV 데이터 처리 및 병합
- **NumPy**: 격자 배열 처리
- **Matplotlib**: 시각화 및 이미지 저장
- **Collections**: BFS용 deque, 다익스트라용 defaultdict
- **Heapq**: 다익스트라 알고리즘용 우선순위 큐

## 📊 알고리즘 비교

| 알고리즘 | 시간복잡도 | 공간복잡도 | 특징 |
|---------|-----------|-----------|------|
| BFS | O(V+E) | O(V) | 최단 경로 보장, 단순함 |
| 다익스트라 | O((V+E)logV) | O(V) | 가중치 고려, 최적 경로 |

## 🎨 시각화 예시

### 지도 시각화
- 격자 기반 2D 지도
- 구조물별 색상 및 도형 구분
- 범례 및 축 라벨 포함

### 경로 시각화  
- 녹색 선으로 경로 표시
- 시작점: 라임색 원형
- 도착점: 주황색 별표
- 경로상 점들: 작은 녹색 원형

## 📈 출력 파일

### 이미지 파일
- `map_visualization.png`: 기본 지도 시각화
- `path_BFS_(x1,y1)_(x2,y2).png`: BFS 경로 결과
- `path_다익스트라_(x1,y1)_(x2,y2).png`: 다익스트라 경로 결과

### CSV 파일
- `path_result_BFS.csv`: BFS 경로 좌표
- `path_result_다익스트라.csv`: 다익스트라 경로 좌표
- 컬럼: step, x, y, coordinates

## 🔍 사용 예시

### 1. 기본 데모 실행
```python
from pathfinding_system import PathfindingSystem

system = PathfindingSystem()
system.run_demo()
```

### 2. 특정 경로 탐색
```python
system = PathfindingSystem()
data = system.load_and_merge_data()
system.create_grid(data)

# BFS로 경로 탐색
path = system.bfs_pathfinding((2, 2), (15, 15))
if path:
    system.visualize_path(path, (2, 2), (15, 15), "BFS")
    system.save_path_to_csv(path, "BFS")
```

### 3. 인터랙티브 모드
```python
python interactive_pathfinding.py
# 프롬프트에 따라 시작점, 도착점, 알고리즘 선택
```

## 🎓 학습 요소

### Pandas DataFrame 활용
- 여러 CSV 파일 병합 및 전처리
- 데이터 정렬 및 타입 변환
- 결과 데이터프레임 생성 및 저장

### 좌표 기반 데이터 처리
- 2D 격자 공간 설계
- 구조물 좌표 시각화
- 격자 기반 경로 탐색

### 알고리즘 이해
- BFS 구현을 통한 최단 경로 탐색
- 다익스트라 구현을 통한 가중치 기반 경로 탐색
- 8방향 이동 및 장애물 처리

### 시각화 도구 익히기
- matplotlib을 활용한 지도 시각화
- 경로 및 구조물 시각화
- 고품질 이미지 저장

### 파일 저장과 로딩
- CSV 파일 읽기/쓰기
- PNG 이미지 저장
- UTF-8 인코딩 처리

## 🐛 문제 해결

### 일반적인 오류
1. **파일을 찾을 수 없습니다**: CSV 파일이 올바른 위치에 있는지 확인
2. **경로를 찾을 수 없습니다**: 시작점/도착점이 장애물이 아닌지 확인
3. **좌표 범위 오류**: 입력 좌표가 격자 범위 내에 있는지 확인

### 성능 최적화
- 대용량 데이터의 경우 격자 크기 조정
- 알고리즘 선택 시 데이터 특성 고려
- 메모리 사용량 모니터링

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 👥 팀 프로젝트

이 프로젝트는 팀 프로젝트 과제로 제작되었으며, 다음 요구사항을 모두 충족합니다:
- ✅ CSV 데이터 처리 및 병합
- ✅ 카테고리 변환 (딕셔너리 매핑)
- ✅ 2D 격자 좌표계 설계
- ✅ 구조물별 시각화 (도형, 색상)
- ✅ PNG 이미지 저장
- ✅ 직접 구현한 경로 탐색 알고리즘
- ✅ 장애물 처리
- ✅ CSV 결과 저장 