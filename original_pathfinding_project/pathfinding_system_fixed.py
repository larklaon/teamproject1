"""
경로 탐색 알고리즘 프로젝트 - 오류 수정 버전
============================================

이 파일은 linter 오류를 모두 수정한 깔끔한 버전입니다.
코딩 초보자도 이해할 수 있도록 자세한 주석을 포함했습니다.

프로젝트 목표:
1. CSV 파일에서 건물, 도로, 건설현장 데이터를 읽어오기
2. 이 데이터를 2D 지도로 시각화하기
3. 두 지점 사이의 최단 경로를 찾는 알고리즘 구현하기
4. 찾은 경로를 시각화하고 파일로 저장하기

작성자: AI 어시스턴트
날짜: 2024년
"""

# ============================================
# 1. 필요한 라이브러리 가져오기 (import)
# ============================================

import pandas as pd          # CSV 파일을 읽고 쓰기 위한 라이브러리
import numpy as np           # 숫자 계산을 위한 라이브러리
import matplotlib            # 그래프와 그림을 그리기 위한 라이브러리
matplotlib.use('Agg')        # GUI 없이 그림을 파일로 저장하기 위한 설정
import matplotlib.pyplot as plt  # matplotlib의 그래프 그리기 도구
import matplotlib.patches as patches  # 도형을 그리기 위한 도구
from collections import deque, defaultdict  # 큐와 딕셔너리 자료구조
import heapq                 # 우선순위 큐 (다익스트라 알고리즘용)
import os                    # 파일 시스템 관련 작업
from typing import Optional, List, Tuple, Dict, Any  # 타입 힌트

class PathfindingSystem:
    """
    경로 탐색 시스템의 메인 클래스
    
    이 클래스는 다음과 같은 기능을 제공합니다:
    1. CSV 파일에서 데이터 읽기
    2. 2D 격자 지도 만들기
    3. 경로 탐색 알고리즘 실행
    4. 결과 시각화 및 저장
    """
    
    def __init__(self):
        """
        클래스 초기화 함수 (생성자)
        프로그램이 시작될 때 한 번만 실행됩니다.
        """
        
        # ============================================
        # 2. 구조물 타입을 의미있는 이름으로 변환하는 딕셔너리
        # ============================================
        # 딕셔너리: 숫자 키를 문자열 값으로 매핑
        self.structure_types: Dict[int, str] = {
            1: "건물",        # 숫자 1은 "건물"을 의미
            2: "도로",        # 숫자 2는 "도로"를 의미
            3: "건설현장"     # 숫자 3은 "건설현장"을 의미
        }
        
        # ============================================
        # 3. 시각화 설정 - 각 구조물을 어떻게 그릴지 정의
        # ============================================
        self.visual_config: Dict[int, Dict[str, Any]] = {
            1: {  # 건물 설정
                "color": "blue",      # 파란색
                "marker": "s",        # 사각형 모양 (square)
                "size": 100,          # 크기
                "label": "건물"       # 범례에 표시될 이름
            },
            2: {  # 도로 설정
                "color": "gray",      # 회색
                "marker": "o",        # 원형 모양 (circle)
                "size": 50,           # 크기
                "label": "도로"       # 범례에 표시될 이름
            },
            3: {  # 건설현장 설정
                "color": "red",       # 빨간색
                "marker": "^",        # 삼각형 모양 (triangle)
                "size": 120,          # 크기
                "label": "건설현장"   # 범례에 표시될 이름
            }
        }
        
        # ============================================
        # 4. 격자 크기 설정
        # ============================================
        self.grid_size: Tuple[int, int] = (50, 50)  # 기본 격자 크기: 가로 50, 세로 50
        self.grid: Optional[np.ndarray] = None      # 실제 격자 데이터 (나중에 생성됨)
        
    def load_and_merge_data(self) -> Optional[pd.DataFrame]:
        """
        CSV 파일들을 불러와서 하나로 합치는 함수
        
        반환값:
            pandas.DataFrame: 합쳐진 데이터, 실패시 None
        """
        try:
            # ============================================
            # 5. 세 개의 CSV 파일을 각각 읽어오기
            # ============================================
            print("CSV 파일들을 읽어오는 중...")
            
            # pd.read_csv(): CSV 파일을 읽어서 DataFrame으로 변환
            buildings_df = pd.read_csv('buildings.csv')        # 건물 데이터
            roads_df = pd.read_csv('roads.csv')               # 도로 데이터
            construction_df = pd.read_csv('construction_sites.csv')  # 건설현장 데이터
            
            # ============================================
            # 6. 세 개의 DataFrame을 하나로 합치기
            # ============================================
            # pd.concat(): 여러 DataFrame을 세로로 합침
            # ignore_index=True: 인덱스를 새로 번호 매김
            merged_df = pd.concat([buildings_df, roads_df, construction_df], 
                                ignore_index=True)
            
            # ============================================
            # 7. 데이터를 x, y 좌표 순서로 정렬하기
            # ============================================
            # sort_values(): 특정 컬럼을 기준으로 정렬
            # reset_index(): 정렬 후 인덱스를 다시 0부터 시작
            merged_df = merged_df.sort_values(['x', 'y']).reset_index(drop=True)
            
            # ============================================
            # 8. 숫자 타입을 의미있는 이름으로 변환
            # ============================================
            # map(): 각 숫자를 해당하는 이름으로 변환
            # lambda x: ... : 익명 함수 (x를 입력받아서 결과 반환)
            merged_df['type_name'] = merged_df['type'].map(
                lambda x: self.structure_types.get(x, "알 수 없음")
            )
            
            # ============================================
            # 9. 결과 출력
            # ============================================
            print("데이터 로드 완료:")
            print(f"- 총 구조물 수: {len(merged_df)}")
            print(f"- 건물: {len(buildings_df)}개")
            print(f"- 도로: {len(roads_df)}개") 
            print(f"- 건설현장: {len(construction_df)}개")
            
            return merged_df  # 합쳐진 데이터 반환
            
        except FileNotFoundError as e:
            # 파일을 찾을 수 없는 경우
            print(f"파일을 찾을 수 없습니다: {e}")
            print("buildings.csv, roads.csv, construction_sites.csv 파일이")
            print("현재 폴더에 있는지 확인해주세요.")
            return None
            
        except Exception as e:
            # 기타 오류 발생 시
            print(f"데이터 로드 중 오류 발생: {e}")
            return None
    
    def create_grid(self, data: pd.DataFrame) -> Tuple[int, int]:
        """
        2D 격자 공간을 생성하는 함수
        
        매개변수:
            data: pandas.DataFrame - 구조물 데이터
            
        반환값:
            tuple: (최대 x 좌표, 최대 y 좌표)
        """
        # ============================================
        # 10. 격자 크기 계산하기
        # ============================================
        # 데이터에서 가장 큰 x, y 좌표를 찾기
        max_x = int(max(data['x'].max(), self.grid_size[0]))  # 가로 크기
        max_y = int(max(data['y'].max(), self.grid_size[1]))  # 세로 크기
        
        # ============================================
        # 11. 빈 격자 배열 생성하기
        # ============================================
        # np.zeros(): 모든 값이 0인 배열 생성
        # (max_y + 1, max_x + 1): 세로 x 가로 크기
        # dtype=int: 정수형 데이터 타입
        self.grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        
        # ============================================
        # 12. 데이터를 격자에 배치하기
        # ============================================
        # iterrows(): DataFrame의 각 행을 순서대로 처리
        for _, row in data.iterrows():
            x = row['x']              # x 좌표
            y = row['y']              # y 좌표
            structure_type = row['type']  # 구조물 타입 (1, 2, 3)
            
            # 우선순위에 따라 격자에 배치
            if structure_type == 3:  # 건설현장 (최고 우선순위)
                self.grid[y, x] = 3
            elif structure_type == 1 and self.grid[y, x] == 0:  # 건물
                self.grid[y, x] = 1
            elif structure_type == 2 and self.grid[y, x] == 0:  # 도로
                self.grid[y, x] = 2
        
        print(f"격자 생성 완료: {max_x + 1} x {max_y + 1}")
        return max_x, max_y
    
    def visualize_map(self, data: pd.DataFrame, max_x: int, max_y: int, 
                     save_path: str = "map_visualization.png") -> None:
        """
        지도를 시각화하는 함수
        
        매개변수:
            data: pandas.DataFrame - 구조물 데이터
            max_x, max_y: int - 격자의 최대 크기
            save_path: str - 저장할 파일 경로
        """
        # ============================================
        # 13. 그래프 창 생성하기
        # ============================================
        # plt.figure(): 새로운 그래프 창 생성
        # figsize=(15, 12): 창 크기 (가로 15인치, 세로 12인치)
        plt.figure(figsize=(15, 12))
        
        # ============================================
        # 14. 격자 그리기
        # ============================================
        plt.grid(True, alpha=0.3)  # alpha=0.3: 투명도 30%
        
        # ============================================
        # 15. 구조물별로 시각화하기
        # ============================================
        for structure_type in [1, 2, 3]:  # 건물, 도로, 건설현장 순서
            # 해당 타입의 데이터만 필터링
            type_data = data[data['type'] == structure_type]
            
            if len(type_data) > 0:  # 데이터가 있는 경우만
                # 시각화 설정 가져오기
                config = self.visual_config[structure_type]
                
                # plt.scatter(): 점들을 그리기
                plt.scatter(
                    type_data['x'],           # x 좌표
                    type_data['y'],           # y 좌표
                    c=config['color'],        # 색상
                    marker=config['marker'],  # 모양
                    s=config['size'],         # 크기
                    label=config['label'],    # 범례 이름
                    alpha=0.8,                # 투명도
                    edgecolors='black',       # 테두리 색상
                    linewidth=1               # 테두리 두께
                )
        
        # ============================================
        # 16. 그래프 꾸미기
        # ============================================
        # 축 범위 설정
        plt.xlim(0, max_x + 1)  # x축 범위
        plt.ylim(0, max_y + 1)  # y축 범위
        
        # 축 라벨 설정
        plt.xlabel('X 좌표')
        plt.ylabel('Y 좌표')
        
        # 제목 설정
        plt.title('구조물 지도 시각화', fontsize=16, fontweight='bold')
        
        # 범례 표시
        plt.legend(loc='upper right')
        
        # 격자 번호 표시 (5칸마다)
        plt.xticks(range(0, max_x + 1, 5))
        plt.yticks(range(0, max_y + 1, 5))
        
        # ============================================
        # 17. 그래프 저장하기
        # ============================================
        plt.tight_layout()  # 레이아웃 정리
        plt.savefig(save_path, dpi=300, bbox_inches='tight')  # PNG 파일로 저장
        plt.show()  # 그래프 화면에 표시
        print(f"지도 시각화 저장 완료: {save_path}")
    
    def bfs_pathfinding(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        BFS(너비 우선 탐색)를 사용한 최단 경로 탐색
        
        BFS는 시작점에서 가까운 곳부터 차례대로 탐색하여
        최단 경로를 찾는 알고리즘입니다.
        
        매개변수:
            start: tuple - 시작점 (x, y)
            end: tuple - 도착점 (x, y)
            
        반환값:
            list: 경로 좌표 리스트, 실패시 None
        """
        # ============================================
        # 18. 입력값 유효성 검사
        # ============================================
        if not self.is_valid_position(start) or not self.is_valid_position(end):
            print("시작점 또는 도착점이 격자 범위를 벗어났습니다.")
            return None
        
        # ============================================
        # 19. 시작점이 장애물인지 확인
        # ============================================
        if self.grid is None:
            print("격자가 초기화되지 않았습니다.")
            return None
            
        if self.grid[start[1], start[0]] in [1, 3]:  # 건물이나 건설현장
            print(f"시작점 ({start[0]}, {start[1]})이 장애물입니다.")
            return None
        
        # ============================================
        # 20. 도착점이 장애물인지 확인
        # ============================================
        if self.grid[end[1], end[0]] in [1, 3]:  # 건물이나 건설현장
            print(f"도착점 ({end[0]}, {end[1]})이 장애물입니다.")
            return None
        
        # ============================================
        # 21. BFS 알고리즘 초기화
        # ============================================
        # deque(): 양쪽 끝에서 빠르게 추가/제거 가능한 큐
        # (현재위치, 지금까지의경로) 형태로 저장
        queue = deque([(start, [start])])
        
        # visited: 이미 방문한 위치들을 저장하는 집합
        visited = set([start])
        
        # ============================================
        # 22. 8방향 이동 정의 (상하좌우 + 대각선)
        # ============================================
        directions = [
            (-1, -1),  # 왼쪽 위
            (-1, 0),   # 위
            (-1, 1),   # 오른쪽 위
            (0, -1),   # 왼쪽
            (0, 1),    # 오른쪽
            (1, -1),   # 왼쪽 아래
            (1, 0),    # 아래
            (1, 1)     # 오른쪽 아래
        ]
        
        # ============================================
        # 23. BFS 메인 루프
        # ============================================
        while queue:  # 큐에 위치가 남아있는 동안
            # 큐에서 가장 먼저 들어온 위치 꺼내기
            current, path = queue.popleft()
            
            # 도착점에 도달했는지 확인
            if current == end:
                print(f"BFS로 경로를 찾았습니다! 길이: {len(path)} 단계")
                return path
            
            # ============================================
            # 24. 8방향으로 이동 시도
            # ============================================
            for dx, dy in directions:
                # 다음 위치 계산
                next_x = current[0] + dx
                next_y = current[1] + dy
                next_pos = (next_x, next_y)
                
                # 다음 위치가 유효한지 확인
                if (next_pos not in visited and  # 아직 방문하지 않았고
                    self.is_valid_position(next_pos) and  # 격자 범위 내에 있고
                    self.grid is not None and  # 격자가 초기화되었고
                    self.grid[next_y, next_x] not in [1, 3]):  # 장애물이 아니면
                    
                    # 방문 표시
                    visited.add(next_pos)
                    
                    # 큐에 추가 (경로에 현재 위치 추가)
                    queue.append((next_pos, path + [next_pos]))
        
        # 경로를 찾지 못한 경우
        print("BFS로 경로를 찾을 수 없습니다.")
        return None
    
    def dijkstra_pathfinding(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        다익스트라 알고리즘을 사용한 최단 경로 탐색
        
        다익스트라는 각 위치까지의 거리를 계산하여
        가장 짧은 경로를 찾는 알고리즘입니다.
        
        매개변수:
            start: tuple - 시작점 (x, y)
            end: tuple - 도착점 (x, y)
            
        반환값:
            list: 경로 좌표 리스트, 실패시 None
        """
        # ============================================
        # 25. 입력값 유효성 검사
        # ============================================
        if not self.is_valid_position(start) or not self.is_valid_position(end):
            print("시작점 또는 도착점이 격자 범위를 벗어났습니다.")
            return None
        
        # ============================================
        # 26. 시작점과 도착점 장애물 검사
        # ============================================
        if self.grid is None:
            print("격자가 초기화되지 않았습니다.")
            return None
            
        if self.grid[start[1], start[0]] in [1, 3]:
            print(f"시작점 ({start[0]}, {start[1]})이 장애물입니다.")
            return None
        
        if self.grid[end[1], end[0]] in [1, 3]:
            print(f"도착점 ({end[0]}, {end[1]})이 장애물입니다.")
            return None
        
        # ============================================
        # 27. 다익스트라 알고리즘 초기화
        # ============================================
        # distances: 각 위치까지의 최단 거리
        # defaultdict(lambda: float('inf')): 기본값이 무한대인 딕셔너리
        distances = defaultdict(lambda: float('inf'))
        distances[start] = 0  # 시작점까지의 거리는 0
        
        # previous: 최단 경로에서 이전 위치
        previous: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # 우선순위 큐: (거리, 현재위치) 형태로 저장
        # heapq는 가장 작은 값이 먼저 나오는 큐
        pq = [(0, start)]
        
        # visited: 이미 처리한 위치들
        visited = set()
        
        # 8방향 이동 정의
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), 
            (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        
        # ============================================
        # 28. 다익스트라 메인 루프
        # ============================================
        while pq:  # 우선순위 큐에 위치가 남아있는 동안
            # 가장 거리가 짧은 위치 꺼내기
            current_dist, current = heapq.heappop(pq)
            
            # 이미 처리한 위치면 건너뛰기
            if current in visited:
                continue
                
            # 처리 완료 표시
            visited.add(current)
            
            # 도착점에 도달했는지 확인
            if current == end:
                # ============================================
                # 29. 경로 재구성
                # ============================================
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                
                # 경로를 뒤집어서 시작점부터 도착점 순서로 만들기
                path = path[::-1]
                
                print(f"다익스트라로 경로를 찾았습니다! 길이: {len(path)} 단계")
                return path
            
            # ============================================
            # 30. 8방향으로 이동 시도
            # ============================================
            for dx, dy in directions:
                next_x = current[0] + dx
                next_y = current[1] + dy
                next_pos = (next_x, next_y)
                
                # 다음 위치가 유효한지 확인
                if (self.is_valid_position(next_pos) and 
                    self.grid is not None and
                    self.grid[next_y, next_x] not in [1, 3] and
                    next_pos not in visited):
                    
                    # 이동 비용 계산 (대각선은 더 큰 비용)
                    cost = 1.4 if abs(dx) + abs(dy) == 2 else 1.0
                    new_dist = current_dist + cost
                    
                    # 더 짧은 경로를 찾았으면 업데이트
                    if new_dist < distances[next_pos]:
                        distances[next_pos] = new_dist
                        previous[next_pos] = current
                        # 우선순위 큐에 추가 (정수로 변환하여 타입 오류 방지)
                        heapq.heappush(pq, (int(new_dist * 10), next_pos))
        
        print("다익스트라로 경로를 찾을 수 없습니다.")
        return None
    
    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        위치가 격자 범위 내에 있는지 확인하는 함수
        
        매개변수:
            pos: tuple - 확인할 위치 (x, y)
            
        반환값:
            bool: 유효하면 True, 아니면 False
        """
        if self.grid is None:
            return False
        
        x, y = pos
        # x, y가 모두 0 이상이고 격자 크기보다 작은지 확인
        return 0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]
    
    def visualize_path(self, path: Optional[List[Tuple[int, int]]], 
                      start: Tuple[int, int], end: Tuple[int, int], 
                      algorithm_name: str, save_path: Optional[str] = None) -> None:
        """
        찾은 경로를 시각화하는 함수
        
        매개변수:
            path: list - 경로 좌표 리스트
            start: tuple - 시작점
            end: tuple - 도착점
            algorithm_name: str - 알고리즘 이름
            save_path: str - 저장할 파일 경로 (선택사항)
        """
        if path is None:
            print("시각화할 경로가 없습니다.")
            return
        
        # ============================================
        # 31. 그래프 창 생성
        # ============================================
        plt.figure(figsize=(15, 12))
        
        # 격자 그리기
        plt.grid(True, alpha=0.3)
        
        # ============================================
        # 32. 원본 데이터 다시 로드하여 구조물 표시
        # ============================================
        data = self.load_and_merge_data()
        if data is None:
            print("데이터를 로드할 수 없습니다.")
            return
        
        # 구조물별로 시각화
        for structure_type in [1, 2, 3]:
            type_data = data[data['type'] == structure_type]
            if len(type_data) > 0:
                config = self.visual_config[structure_type]
                plt.scatter(type_data['x'], type_data['y'], 
                           c=config['color'], marker=config['marker'], 
                           s=config['size'], label=config['label'], 
                           alpha=0.8, edgecolors='black', linewidth=1)
        
        # ============================================
        # 33. 경로 그리기
        # ============================================
        if len(path) > 1:
            # 경로의 x, y 좌표를 분리
            path_x = [pos[0] for pos in path]
            path_y = [pos[1] for pos in path]
            
            # 경로를 녹색 선으로 그리기
            plt.plot(path_x, path_y, 'g-', linewidth=3, alpha=0.8, label='탐색 경로')
            
            # 경로상의 점들을 작은 녹색 원으로 표시
            plt.scatter(path_x, path_y, c='green', s=30, alpha=0.6, zorder=5)
        
        # ============================================
        # 34. 시작점과 도착점 표시
        # ============================================
        # 시작점: 라임색 원
        plt.scatter(start[0], start[1], c='lime', marker='o', s=200, 
                   label='시작점', edgecolors='black', linewidth=2, zorder=6)
        
        # 도착점: 주황색 별
        plt.scatter(end[0], end[1], c='orange', marker='*', s=300, 
                   label='도착점', edgecolors='black', linewidth=2, zorder=6)
        
        # ============================================
        # 35. 그래프 꾸미기
        # ============================================
        if self.grid is None:
            print("격자가 초기화되지 않았습니다.")
            return
            
        max_x, max_y = self.grid.shape[1] - 1, self.grid.shape[0] - 1
        plt.xlim(0, max_x + 1)
        plt.ylim(0, max_y + 1)
        plt.xlabel('X 좌표')
        plt.ylabel('Y 좌표')
        plt.title(f'{algorithm_name} 경로 탐색 결과', fontsize=16, fontweight='bold')
        plt.legend(loc='upper right')
        
        # 격자 번호 표시
        plt.xticks(range(0, max_x + 1, 5))
        plt.yticks(range(0, max_y + 1, 5))
        
        plt.tight_layout()
        
        # ============================================
        # 36. 파일로 저장 (선택사항)
        # ============================================
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"경로 시각화 저장 완료: {save_path}")
        
        plt.show()
    
    def save_path_to_csv(self, path: Optional[List[Tuple[int, int]]], 
                        algorithm_name: str, filename: Optional[str] = None) -> None:
        """
        경로 결과를 CSV 파일로 저장하는 함수
        
        매개변수:
            path: list - 경로 좌표 리스트
            algorithm_name: str - 알고리즘 이름
            filename: str - 저장할 파일명 (선택사항)
        """
        if path is None:
            print("저장할 경로가 없습니다.")
            return
        
        # ============================================
        # 37. 파일명 생성
        # ============================================
        if filename is None:
            filename = f"path_result_{algorithm_name}.csv"
        
        # ============================================
        # 38. 경로 데이터를 DataFrame으로 변환
        # ============================================
        path_data = []
        for i, pos in enumerate(path):
            path_data.append({
                'step': i + 1,                    # 단계 번호
                'x': pos[0],                      # x 좌표
                'y': pos[1],                      # y 좌표
                'coordinates': f"({pos[0]}, {pos[1]})"  # 좌표 문자열
            })
        
        # DataFrame 생성
        path_df = pd.DataFrame(path_data)
        
        # ============================================
        # 39. CSV 파일로 저장
        # ============================================
        # encoding='utf-8-sig': 한글이 포함된 파일을 위해 UTF-8 인코딩 사용
        path_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # ============================================
        # 40. 저장 결과 출력
        # ============================================
        print(f"경로 결과 저장 완료: {filename}")
        print(f"- 총 단계 수: {len(path)}")
        print(f"- 시작점: ({path[0][0]}, {path[0][1]})")
        print(f"- 도착점: ({path[-1][0]}, {path[-1][1]})")
    
    def run_demo(self) -> None:
        """
        전체 시스템을 데모로 실행하는 함수
        이 함수는 프로그램의 메인 실행 부분입니다.
        """
        print("=== 경로 탐색 시스템 데모 ===\n")
        
        # ============================================
        # 41. 1단계: 데이터 로드 및 병합
        # ============================================
        print("1. 데이터 로드 및 병합 중...")
        data = self.load_and_merge_data()
        if data is None:
            print("데이터 로드에 실패했습니다. 프로그램을 종료합니다.")
            return
        
        # ============================================
        # 42. 2단계: 격자 생성
        # ============================================
        print("\n2. 격자 생성 중...")
        max_x, max_y = self.create_grid(data)
        
        # ============================================
        # 43. 3단계: 지도 시각화
        # ============================================
        print("\n3. 지도 시각화 중...")
        self.visualize_map(data, max_x, max_y)
        
        # ============================================
        # 44. 4단계: 경로 탐색 테스트
        # ============================================
        print("\n4. 경로 탐색 테스트...")
        
        # 테스트할 경로들 정의
        test_cases = [
            ((2, 2), (15, 15), "BFS"),           # 테스트 케이스 1
            ((2, 2), (15, 15), "다익스트라"),     # 테스트 케이스 1 (다른 알고리즘)
            ((10, 5), (40, 20), "BFS"),          # 테스트 케이스 2
            ((10, 5), (40, 20), "다익스트라"),    # 테스트 케이스 2 (다른 알고리즘)
        ]
        
        # 각 테스트 케이스 실행
        for start, end, algorithm in test_cases:
            print(f"\n--- {algorithm} 알고리즘 테스트 ---")
            print(f"시작점: {start}, 도착점: {end}")
            
            # 알고리즘 선택에 따라 경로 탐색 실행
            if algorithm == "BFS":
                path = self.bfs_pathfinding(start, end)
            else:
                path = self.dijkstra_pathfinding(start, end)
            
            # 경로를 찾았으면 시각화하고 저장
            if path:
                print(f"경로 길이: {len(path)} 단계")
                
                # 경로 시각화
                self.visualize_path(path, start, end, algorithm, 
                                  f"path_{algorithm}_{start}_{end}.png")
                
                # CSV 저장
                self.save_path_to_csv(path, algorithm, 
                                    f"path_{algorithm}_{start}_{end}.csv")
            else:
                print("경로를 찾을 수 없습니다.")

# ============================================
# 45. 메인 함수 (프로그램 시작점)
# ============================================
def main() -> None:
    """
    프로그램의 시작점
    이 함수가 호출되면 경로 탐색 시스템이 실행됩니다.
    """
    # PathfindingSystem 클래스의 인스턴스 생성
    system = PathfindingSystem()
    
    # 데모 실행
    system.run_demo()

# ============================================
# 46. 프로그램 실행 조건
# ============================================
# 이 파일이 직접 실행될 때만 main() 함수 호출
# 다른 파일에서 import될 때는 실행되지 않음
if __name__ == "__main__":
    main() 