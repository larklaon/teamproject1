import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 없이 사용
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque, defaultdict
import heapq
import os

class PathfindingSystem:
    def __init__(self):
        # 구조물 타입 매핑 딕셔너리
        self.structure_types = {
            1: "건물",
            2: "도로", 
            3: "건설현장"
        }
        
        # 시각화 색상 및 도형 매핑
        self.visual_config = {
            1: {"color": "blue", "marker": "s", "size": 100, "label": "건물"},
            2: {"color": "gray", "marker": "o", "size": 50, "label": "도로"},
            3: {"color": "red", "marker": "^", "size": 120, "label": "건설현장"}
        }
        
        # 격자 크기 설정
        self.grid_size = (50, 50)
        self.grid = None
        
    def load_and_merge_data(self):
        """CSV 파일들을 불러와서 병합하고 정렬"""
        try:
            # 세 개의 CSV 파일 로드
            buildings_df = pd.read_csv('buildings.csv')
            roads_df = pd.read_csv('roads.csv')
            construction_df = pd.read_csv('construction_sites.csv')
            
            # 데이터 병합
            merged_df = pd.concat([buildings_df, roads_df, construction_df], ignore_index=True)
            
            # 좌표 기준으로 정렬
            merged_df = merged_df.sort_values(['x', 'y']).reset_index(drop=True)
            
            # 구조물 타입을 의미있는 이름으로 변환
            merged_df['type_name'] = merged_df['type'].map(lambda x: self.structure_types.get(x, "알 수 없음"))
            
            print("데이터 로드 완료:")
            print(f"- 총 구조물 수: {len(merged_df)}")
            print(f"- 건물: {len(buildings_df)}개")
            print(f"- 도로: {len(roads_df)}개") 
            print(f"- 건설현장: {len(construction_df)}개")
            
            return merged_df
            
        except FileNotFoundError as e:
            print(f"파일을 찾을 수 없습니다: {e}")
            return None
        except Exception as e:
            print(f"데이터 로드 중 오류 발생: {e}")
            return None
    
    def create_grid(self, data):
        """2D 격자 공간 생성 (1,1이 좌상단, x_max, y_max가 우하단)"""
        max_x = max(data['x'].max(), self.grid_size[0])
        max_y = max(data['y'].max(), self.grid_size[1])
        
        # 격자 초기화 (0: 빈 공간, 1: 건물, 2: 도로, 3: 건설현장)
        self.grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        
        # 데이터를 격자에 배치 (우선순위: 건설현장 > 건물 > 도로)
        for _, row in data.iterrows():
            x, y, structure_type = row['x'], row['y'], row['type']
            if structure_type == 3:  # 건설현장 (최고 우선순위)
                self.grid[y, x] = 3
            elif structure_type == 1 and self.grid[y, x] == 0:  # 건물
                self.grid[y, x] = 1
            elif structure_type == 2 and self.grid[y, x] == 0:  # 도로
                self.grid[y, x] = 2
        
        print(f"격자 생성 완료: {max_x + 1} x {max_y + 1}")
        return max_x, max_y
    
    def visualize_map(self, data, max_x, max_y, save_path="map_visualization.png"):
        """지도 시각화 - 구조물 종류별로 다른 도형과 색상 사용"""
        plt.figure(figsize=(15, 12))
        
        # 격자 그리기
        plt.grid(True, alpha=0.3)
        
        # 구조물별로 시각화
        for structure_type in [1, 2, 3]:
            type_data = data[data['type'] == structure_type]
            if len(type_data) > 0:
                config = self.visual_config[structure_type]
                plt.scatter(type_data['x'], type_data['y'], 
                           c=config['color'], marker=config['marker'], 
                           s=config['size'], label=config['label'], 
                           alpha=0.8, edgecolors='black', linewidth=1)
        
        # 축 설정
        plt.xlim(0, max_x + 1)
        plt.ylim(0, max_y + 1)
        plt.xlabel('X 좌표')
        plt.ylabel('Y 좌표')
        plt.title('구조물 지도 시각화', fontsize=16, fontweight='bold')
        plt.legend(loc='upper right')
        
        # 격자 번호 표시
        plt.xticks(range(0, max_x + 1, 5))
        plt.yticks(range(0, max_y + 1, 5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"지도 시각화 저장 완료: {save_path}")
    
    def bfs_pathfinding(self, start, end):
        """BFS를 사용한 최단 경로 탐색"""
        if not self.is_valid_position(start) or not self.is_valid_position(end):
            return None
        
        # 시작점이 장애물인지 확인
        if self.grid[start[1], start[0]] in [1, 3]:  # 건물이나 건설현장
            print(f"시작점 ({start[0]}, {start[1]})이 장애물입니다.")
            return None
        
        # 도착점이 장애물인지 확인  
        if self.grid[end[1], end[0]] in [1, 3]:  # 건물이나 건설현장
            print(f"도착점 ({end[0]}, {end[1]})이 장애물입니다.")
            return None
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        # 8방향 이동 (상하좌우 + 대각선)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                return path
            
            for dx, dy in directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if (next_pos not in visited and 
                    self.is_valid_position(next_pos) and 
                    self.grid[next_y, next_x] not in [1, 3]):  # 건물이나 건설현장이 아닌 경우
                    
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        print("경로를 찾을 수 없습니다.")
        return None
    
    def dijkstra_pathfinding(self, start, end):
        """다익스트라 알고리즘을 사용한 최단 경로 탐색"""
        if not self.is_valid_position(start) or not self.is_valid_position(end):
            return None
        
        # 시작점이 장애물인지 확인
        if self.grid[start[1], start[0]] in [1, 3]:
            print(f"시작점 ({start[0]}, {start[1]})이 장애물입니다.")
            return None
        
        # 도착점이 장애물인지 확인
        if self.grid[end[1], end[0]] in [1, 3]:
            print(f"도착점 ({end[0]}, {end[1]})이 장애물입니다.")
            return None
        
        # 거리와 이전 노드 추적
        distances = defaultdict(lambda: float('inf'))
        distances[start] = 0
        previous = {}
        
        # 우선순위 큐 (거리, 현재 위치)
        pq = [(0, start)]
        visited = set()
        
        # 8방향 이동
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == end:
                # 경로 재구성
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                return path[::-1]
            
            for dx, dy in directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if (self.is_valid_position(next_pos) and 
                    self.grid[next_y, next_x] not in [1, 3] and
                    next_pos not in visited):
                    
                    # 대각선 이동은 더 큰 비용
                    cost = 1.4 if abs(dx) + abs(dy) == 2 else 1.0
                    new_dist = current_dist + cost
                    
                    if new_dist < distances[next_pos]:
                        distances[next_pos] = new_dist
                        previous[next_pos] = current
                        heapq.heappush(pq, (int(new_dist * 10), next_pos))  # 정수로 변환
        
        print("경로를 찾을 수 없습니다.")
        return None
    
    def is_valid_position(self, pos):
        """위치가 격자 범위 내에 있는지 확인"""
        if self.grid is None:
            return False
        x, y = pos
        return 0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]
    
    def visualize_path(self, path, start, end, algorithm_name, save_path=None):
        """경로 시각화"""
        if path is None:
            print("시각화할 경로가 없습니다.")
            return
        
        plt.figure(figsize=(15, 12))
        
        # 격자 그리기
        plt.grid(True, alpha=0.3)
        
        # 원본 데이터 다시 로드하여 구조물 표시
        data = self.load_and_merge_data()
        
        # 구조물별로 시각화
        for structure_type in [1, 2, 3]:
            type_data = data[data['type'] == structure_type]
            if len(type_data) > 0:
                config = self.visual_config[structure_type]
                plt.scatter(type_data['x'], type_data['y'], 
                           c=config['color'], marker=config['marker'], 
                           s=config['size'], label=config['label'], 
                           alpha=0.8, edgecolors='black', linewidth=1)
        
        # 경로 그리기
        if len(path) > 1:
            path_x = [pos[0] for pos in path]
            path_y = [pos[1] for pos in path]
            plt.plot(path_x, path_y, 'g-', linewidth=3, alpha=0.8, label='탐색 경로')
            
            # 경로상의 점들 표시
            plt.scatter(path_x, path_y, c='green', s=30, alpha=0.6, zorder=5)
        
        # 시작점과 도착점 표시
        plt.scatter(start[0], start[1], c='lime', marker='o', s=200, 
                   label='시작점', edgecolors='black', linewidth=2, zorder=6)
        plt.scatter(end[0], end[1], c='orange', marker='*', s=300, 
                   label='도착점', edgecolors='black', linewidth=2, zorder=6)
        
        # 축 설정
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
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"경로 시각화 저장 완료: {save_path}")
        
        plt.show()
    
    def save_path_to_csv(self, path, algorithm_name, filename=None):
        """경로 결과를 CSV 파일로 저장"""
        if path is None:
            print("저장할 경로가 없습니다.")
            return
        
        if filename is None:
            filename = f"path_result_{algorithm_name}.csv"
        
        # 경로 데이터를 DataFrame으로 변환
        path_data = []
        for i, pos in enumerate(path):
            path_data.append({
                'step': i + 1,
                'x': pos[0],
                'y': pos[1],
                'coordinates': f"({pos[0]}, {pos[1]})"
            })
        
        path_df = pd.DataFrame(path_data)
        path_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"경로 결과 저장 완료: {filename}")
        print(f"- 총 단계 수: {len(path)}")
        print(f"- 시작점: ({path[0][0]}, {path[0][1]})")
        print(f"- 도착점: ({path[-1][0]}, {path[-1][1]})")
    
    def run_demo(self):
        """데모 실행"""
        print("=== 경로 탐색 시스템 데모 ===\n")
        
        # 1. 데이터 로드 및 병합
        print("1. 데이터 로드 및 병합 중...")
        data = self.load_and_merge_data()
        if data is None:
            return
        
        # 2. 격자 생성
        print("\n2. 격자 생성 중...")
        max_x, max_y = self.create_grid(data)
        
        # 3. 지도 시각화
        print("\n3. 지도 시각화 중...")
        self.visualize_map(data, max_x, max_y)
        
        # 4. 경로 탐색 테스트
        print("\n4. 경로 탐색 테스트...")
        
        # 테스트 케이스들
        test_cases = [
            ((2, 2), (15, 15), "BFS"),
            ((2, 2), (15, 15), "다익스트라"),
            ((10, 5), (40, 20), "BFS"),
            ((10, 5), (40, 20), "다익스트라"),
        ]
        
        for start, end, algorithm in test_cases:
            print(f"\n--- {algorithm} 알고리즘 테스트 ---")
            print(f"시작점: {start}, 도착점: {end}")
            
            if algorithm == "BFS":
                path = self.bfs_pathfinding(start, end)
            else:
                path = self.dijkstra_pathfinding(start, end)
            
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

def main():
    """메인 함수"""
    system = PathfindingSystem()
    system.run_demo()

if __name__ == "__main__":
    main() 