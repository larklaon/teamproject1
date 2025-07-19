import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathfinding_system import PathfindingSystem

def get_user_input():
    """사용자로부터 시작점과 도착점 입력 받기"""
    print("\n=== 경로 탐색 시스템 ===")
    print("시작점과 도착점을 입력해주세요.")
    
    try:
        start_x = int(input("시작점 X 좌표: "))
        start_y = int(input("시작점 Y 좌표: "))
        end_x = int(input("도착점 X 좌표: "))
        end_y = int(input("도착점 Y 좌표: "))
        
        start = (start_x, start_y)
        end = (end_x, end_y)
        
        return start, end
        
    except ValueError:
        print("올바른 숫자를 입력해주세요.")
        return None, None

def select_algorithm():
    """사용자가 알고리즘 선택"""
    print("\n사용할 알고리즘을 선택하세요:")
    print("1. BFS (너비 우선 탐색)")
    print("2. 다익스트라 (Dijkstra)")
    print("3. 둘 다 실행")
    
    try:
        choice = int(input("선택 (1-3): "))
        if choice == 1:
            return ["BFS"]
        elif choice == 2:
            return ["다익스트라"]
        elif choice == 3:
            return ["BFS", "다익스트라"]
        else:
            print("잘못된 선택입니다. BFS를 사용합니다.")
            return ["BFS"]
    except ValueError:
        print("올바른 숫자를 입력해주세요. BFS를 사용합니다.")
        return ["BFS"]

def interactive_demo():
    """인터랙티브 데모 실행"""
    system = PathfindingSystem()
    
    # 데이터 로드 및 격자 생성
    print("데이터 로드 중...")
    data = system.load_and_merge_data()
    if data is None:
        print("데이터 로드에 실패했습니다.")
        return
    
    max_x, max_y = system.create_grid(data)
    
    # 지도 시각화
    print("지도 시각화 중...")
    system.visualize_map(data, max_x, max_y)
    
    while True:
        # 사용자 입력 받기
        start, end = get_user_input()
        if start is None or end is None:
            continue
        
        # 좌표 유효성 검사
        if not system.is_valid_position(start):
            print(f"시작점 ({start[0]}, {start[1]})이 격자 범위를 벗어났습니다.")
            print(f"유효한 범위: X (0-{max_x}), Y (0-{max_y})")
            continue
            
        if not system.is_valid_position(end):
            print(f"도착점 ({end[0]}, {end[1]})이 격자 범위를 벗어났습니다.")
            print(f"유효한 범위: X (0-{max_x}), Y (0-{max_y})")
            continue
        
        # 알고리즘 선택
        algorithms = select_algorithm()
        
        # 경로 탐색 실행
        for algorithm in algorithms:
            print(f"\n--- {algorithm} 알고리즘 실행 ---")
            
            if algorithm == "BFS":
                path = system.bfs_pathfinding(start, end)
            else:
                path = system.dijkstra_pathfinding(start, end)
            
            if path:
                print(f"경로 발견! 길이: {len(path)} 단계")
                
                # 경로 시각화
                system.visualize_path(path, start, end, algorithm, 
                                    f"interactive_path_{algorithm}_{start}_{end}.png")
                
                # CSV 저장
                system.save_path_to_csv(path, algorithm, 
                                      f"interactive_path_{algorithm}_{start}_{end}.csv")
                
                # 경로 상세 정보 출력
                print("\n경로 상세:")
                for i, pos in enumerate(path):
                    print(f"  {i+1:2d}. ({pos[0]:2d}, {pos[1]:2d})")
            else:
                print("경로를 찾을 수 없습니다.")
        
        # 계속할지 묻기
        continue_choice = input("\n다른 경로를 탐색하시겠습니까? (y/n): ").lower()
        if continue_choice != 'y':
            break
    
    print("경로 탐색 시스템을 종료합니다.")

if __name__ == "__main__":
    interactive_demo() 