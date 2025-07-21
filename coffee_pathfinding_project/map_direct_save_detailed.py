#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚶 3단계: 최단 경로 탐색
===========================================

이 파일은 내 집에서 반달곰 커피까지의 최단 경로를 찾는 역할을 합니다.  

📁 입력:
- 1단계에서 생성된 분석 데이터 (전체 데이터)

📊 출력:
- home_to_cafe.csv: 경로 데이터
- map_final.png: 경로가 표시된 지도

🔍 알고리즘:
- BFS (Breadth-First Search): 너비 우선 탐색
- 8방향 이동 (상하좌우 + 대각선)
- 건설 현장과 아파트/빌딩은 장애물로 처리

🎯 목표:
- 내 집(시작점)에서 반달곰 커피(도착점)까지의 최단 경로 찾기
- 경로를 CSV 파일로 저장
- 경로가 표시된 지도를 PNG 파일로 저장

작성자: AI Assistant
날짜: 2024년
"""

import pandas as pd  # 데이터 처리를 위한 라이브러리
import matplotlib.pyplot as plt  # 그래프 그리기를 위한 라이브러리
plt.rcParams['font.family'] = 'AppleGothic'  # 한글 폰트 설정 (Mac)
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 깨짐 방지
from collections import deque  # 큐 자료구조를 위한 라이브러리
from typing import Optional, List, Tuple  # 타입 힌트를 위한 라이브러리


def load_analyzed_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    분석된 데이터를 불러오는 함수 (전체 데이터)
    
    이 함수는 전체 데이터를 로드합니다 (area 제한 없음).
    내 집이 area 2에 있을 수 있으므로 전체 데이터가 필요합니다.
    
    Returns:
        Optional[pd.DataFrame]: 분석된 데이터프레임, 실패시 None
    """
    try:
        print('📂 전체 데이터 분석을 실행합니다...')
        print('   내 집과 반달곰 커피가 서로 다른 area에 있을 수 있어서 전체 데이터를 사용합니다.')
        
        # ============================================
        # 1단계: 1단계 분석 모듈 임포트 및 실행
        # ============================================
        # 1단계 분석 모듈 임포트 및 실행
        import sys
        import os
        # 상위 디렉토리를 Python 경로에 추가
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from coffee_pathfinding_project.caffee_map_detailed import load_and_analyze_data
        area1_data = load_and_analyze_data()
        if area1_data is None:
            return None
        
        # ============================================
        # 2단계: 전체 데이터를 다시 로드 (area 제한 없음)
        # ============================================
        print('   전체 데이터를 로드하는 중...')
        
        # CSV 파일들 불러오기
        area_map = pd.read_csv('dataFile/area_map.csv')
        area_struct = pd.read_csv('dataFile/area_struct.csv')
        area_category = pd.read_csv('dataFile/area_category.csv')
        
        # 컬럼명의 공백 제거
        area_category.columns = area_category.columns.str.strip()
        
        # 구조물 ID를 이름으로 변환 (공백 제거)
        category_mapping = dict(zip(area_category['category'], area_category['struct'].str.strip()))
        # pandas Series의 map 함수를 사용하여 category를 struct_name으로 변환
        # type: ignore 주석으로 타입 힌트 오류 무시
        area_struct['struct_name'] = area_struct['category'].map(category_mapping)  # type: ignore
        
        # 데이터 병합
        merged_data = pd.merge(area_struct, area_map, on=['x', 'y'], how='left')
        merged_data = merged_data.sort_values(['area', 'x', 'y'])
        
        print(f'✅ 전체 데이터 로드 완료: {len(merged_data)}행')
        return merged_data
        
    except Exception as e:
        print(f'❌ 데이터 로드 오류: {e}')
        return None


def create_grid(data: pd.DataFrame) -> Tuple[List[List[int]], int, int]:
    """
    2D 격자를 생성하는 함수
    
    이 함수는 데이터를 기반으로 2차원 격자를 생성합니다.
    격자는 경로 탐색에서 장애물을 판단하는 데 사용됩니다.
    
    격자 값의 의미:
    - 0: 빈 공간 (이동 가능)
    - 1: 건설 현장 (이동 불가)
    - 2: 아파트/빌딩 (이동 불가)
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        
    Returns:
        Tuple[List[List[int]], int, int]: (격자, 최대 x, 최대 y)
    """
    print('🗺️ 격자를 생성하는 중...')
    
    # ============================================
    # 1단계: 격자 크기 계산
    # ============================================
    # 데이터에서 가장 큰 x, y 좌표를 찾기
    max_x = int(data['x'].max())
    max_y = int(data['y'].max())
    print(f'   격자 크기: {max_x} x {max_y}')
    
    # ============================================
    # 2단계: 빈 격자 생성
    # ============================================
    # 리스트 컴프리헨션을 사용하여 2D 배열 생성
    # 모든 값이 0인 (max_y + 1) x (max_x + 1) 크기의 격자 생성
    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # ============================================
    # 3단계: 건설 현장 배치 (최고 우선순위)
    # ============================================
    # ConstructionSite == 1인 행들만 선택
    construction_sites = data[data['ConstructionSite'] == 1]
    for _, row in construction_sites.iterrows():
        grid[row['y'], row['x']] = 1  # 건설 현장은 값 1
    print(f'   건설 현장 {len(construction_sites)}개 배치 완료')
    
    # ============================================
    # 4단계: 구조물 배치 (아파트와 빌딩만 장애물로 처리)
    # ============================================
    # category가 1(아파트) 또는 2(빌딩)이고 건설 현장이 아닌 경우
    structures = data[(data['category'].isin([1, 2])) & (data['ConstructionSite'] == 0)]
    for _, row in structures.iterrows():
        grid[row['y'], row['x']] = 2  # 아파트/빌딩은 값 2
    print(f'   아파트/빌딩 {len(structures)}개 배치 완료')
    
    # 내 집과 반달곰 커피는 장애물로 처리하지 않음 (이동 가능)
    
    return grid, max_x, max_y


def is_valid_position(pos: Tuple[int, int], grid: List[List[int]]) -> bool:
    """
    위치가 유효한지 확인하는 함수
    
    이 함수는 주어진 위치가 격자 범위 내에 있는지 확인합니다.
    
    Args:
        pos: Tuple[int, int] - 확인할 위치 (x, y)
        grid: List[List[int]] - 격자
        
    Returns:
        bool: 유효한 위치인지 여부
    """
    x, y = pos
    
    # 격자 범위를 벗어나는지 확인
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return False
    
    return True


def bfs_pathfinding(start: Tuple[int, int], end: Tuple[int, int], 
                   grid: List[List[int]]) -> Optional[List[Tuple[int, int]]]:
    """
    BFS를 사용한 최단 경로 탐색
    
    BFS (Breadth-First Search)는 시작점에서 가까운 곳부터 차례대로 탐색하여
    최단 경로를 찾는 알고리즘입니다.
    
    알고리즘 동작 과정:
    1. 시작점을 큐에 넣고 방문 표시
    2. 큐에서 위치를 꺼내서 8방향으로 이동 시도
    3. 유효하고 방문하지 않은 위치를 큐에 추가
    4. 도착점에 도달하면 경로 반환
    
    Args:
        start: Tuple[int, int] - 시작점 (x, y)
        end: Tuple[int, int] - 도착점 (x, y)
        grid: List[List[int]] - 격자
        
    Returns:
        Optional[List[Tuple[int, int]]]: 경로 좌표 리스트, 실패시 None
    """
    print('🔍 BFS 알고리즘으로 최단 경로를 탐색하는 중...')
    
    # ============================================
    # 1단계: 입력값 유효성 검사
    # ============================================
    if not is_valid_position(start, grid) or not is_valid_position(end, grid):
        print("❌ 시작점 또는 도착점이 격자 범위를 벗어났습니다.")
        return None
    
    # ============================================
    # 2단계: 시작점이나 도착점이 장애물인지 확인
    # ============================================
    if grid[start[1], start[0]] in [1, 2]:  # 건설 현장이나 아파트/빌딩
        print(f"❌ 시작점 ({start[0]}, {start[1]})이 장애물입니다.")
        return None
    
    if grid[end[1], end[0]] in [1, 2]:  # 건설 현장이나 아파트/빌딩
        print(f"❌ 도착점 ({end[0]}, {end[1]})이 장애물입니다.")
        return None
    
    # ============================================
    # 3단계: BFS 초기화
    # ============================================
    # deque(): 양쪽 끝에서 빠르게 추가/제거 가능한 큐
    # (현재위치, 지금까지의경로) 형태로 저장
    queue = deque([(start, [start])])
    
    # visited: 이미 방문한 위치들을 저장하는 집합
    # set(): 중복을 허용하지 않는 자료구조
    visited = set([start])
    
    # ============================================
    # 4단계: 8방향 이동 정의 (상하좌우 + 대각선)
    # ============================================
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # 왼쪽 위, 위, 오른쪽 위
        (0, -1), (0, 1),             # 왼쪽, 오른쪽
        (1, -1), (1, 0), (1, 1)      # 왼쪽 아래, 아래, 오른쪽 아래
    ]
    
    # ============================================
    # 5단계: BFS 메인 루프
    # ============================================
    step_count = 0  # 탐색 단계 수 카운트
    while queue:  # 큐에 위치가 남아있는 동안
        step_count += 1
        if step_count % 1000 == 0:  # 1000단계마다 진행상황 출력
            print(f"   탐색 중... {step_count}단계 완료")
        
        # 큐에서 가장 먼저 들어온 위치 꺼내기
        current, path = queue.popleft()
        
        # 도착점에 도달했는지 확인
        if current == end:
            print(f"✅ BFS로 경로를 찾았습니다! 길이: {len(path)} 단계")
            print(f"   총 탐색 단계: {step_count}")
            return path
        
        # ============================================
        # 6단계: 8방향으로 이동 시도
        # ============================================
        for dx, dy in directions:
            # 다음 위치 계산
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)
            
            # 다음 위치가 유효하고 방문하지 않았고 장애물이 아니면
            if (next_pos not in visited and 
                is_valid_position(next_pos, grid) and 
                grid[next_y, next_x] not in [1, 2]):  # 건설 현장이나 아파트/빌딩이 아니면
                
                # 방문 표시
                visited.add(next_pos)
                
                # 큐에 추가 (경로에 현재 위치 추가)
                queue.append((next_pos, path + [next_pos]))
    
    # 경로를 찾지 못한 경우
    print("❌ BFS로 경로를 찾을 수 없습니다.")
    print(f"   총 탐색 단계: {step_count}")
    return None


def save_path_to_csv(path: Optional[List[Tuple[int, int]]], 
                    filename: str = 'home_to_cafe.csv') -> None:
    """
    경로를 CSV 파일로 저장하는 함수
    
    이 함수는 찾은 경로를 CSV 파일로 저장합니다.
    각 단계별로 x, y 좌표와 좌표 문자열을 포함합니다.
    
    Args:
        path: Optional[List[Tuple[int, int]]] - 경로 좌표 리스트
        filename: str - 저장할 파일명
    """
    if path is None:
        print("❌ 경로가 없어서 CSV 파일을 저장할 수 없습니다.")
        return
    
    print('💾 경로를 CSV 파일로 저장하는 중...')
    
    # ============================================
    # 1단계: 경로 데이터를 DataFrame으로 변환
    # ============================================
    path_data = []
    for i, (x, y) in enumerate(path):
        path_data.append({
            'step': i + 1,                    # 단계 번호 (1부터 시작)
            'x': x,                           # x 좌표
            'y': y,                           # y 좌표
            'coordinate': f'({x}, {y})'       # 좌표 문자열
        })
    
    # DataFrame 생성
    df = pd.DataFrame(path_data)
    
    # ============================================
    # 2단계: CSV 파일로 저장
    # ============================================
    # to_csv(): DataFrame을 CSV 파일로 저장
    # index=False: 행 번호는 저장하지 않음
    df.to_csv(filename, index=False)
    
    # ============================================
    # 3단계: 저장 결과 출력
    # ============================================
    print(f'✅ 경로가 {filename}로 저장되었습니다.')
    print(f'   총 단계 수: {len(path)}')
    print(f'   시작점: {path[0]}')
    print(f'   도착점: {path[-1]}')


def visualize_path_with_map(data: pd.DataFrame, path: Optional[List[Tuple[int, int]]], 
                           start: Tuple[int, int], end: Tuple[int, int],
                           save_path: str = 'map_final.png') -> None:
    """
    경로가 포함된 지도를 시각화하는 함수
    
    이 함수는 기존 지도에 찾은 경로를 빨간 선으로 표시합니다.
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        path: Optional[List[Tuple[int, int]]] - 경로 좌표 리스트
        start: Tuple[int, int] - 시작점
        end: Tuple[int, int] - 도착점
        save_path: str - 저장할 파일 경로
    """
    print('🎨 경로가 포함된 지도를 시각화하는 중...')
    
    # ============================================
    # 1단계: 시각화 설정 정의
    # ============================================
    visual_config = {
        'Apartment': {
            'color': 'brown',
            'marker': 'o',
            'size': 100,
            'label': '아파트/빌딩'
        },
        'Building': {
            'color': 'brown',
            'marker': 'o',
            'size': 100,
            'label': '아파트/빌딩'
        },
        'BandalgomCoffee': {
            'color': 'green',
            'marker': 's',
            'size': 120,
            'label': '반달곰 커피'
        },
        'MyHome': {
            'color': 'green',
            'marker': '^',
            'size': 150,
            'label': '내 집'
        }
    }
    
    # ============================================
    # 2단계: 그래프 창 생성
    # ============================================
    plt.figure(figsize=(12, 10))
    
    # ============================================
    # 3단계: 격자 그리기
    # ============================================
    plt.grid(True, alpha=0.3, color='gray')
    
    # ============================================
    # 4단계: 건설 현장 먼저 그리기
    # ============================================
    construction_sites = data[data['ConstructionSite'] == 1]
    if len(construction_sites) > 0:
        plt.scatter(
            construction_sites['x'],
            construction_sites['y'],
            c='gray',
            marker='s',
            s=80,
            label='건설 현장',
            alpha=0.7,
            edgecolors='black',
            linewidth=1
        )
    
    # ============================================
    # 5단계: 구조물별로 시각화하기
    # ============================================
    for struct_type in ['Apartment', 'Building', 'BandalgomCoffee', 'MyHome']:
        type_data = data[(data['struct_name'] == struct_type) & (data['category'] != 0)]
        
        if len(type_data) > 0:
            config = visual_config[struct_type]
            
            plt.scatter(
                type_data['x'],
                type_data['y'],
                c=config['color'],
                marker=config['marker'],
                s=config['size'],
                label=config['label'],
                alpha=0.8,
                edgecolors='black',
                linewidth=1.5
            )
    
    # ============================================
    # 6단계: 경로 그리기 (빨간 선)
    # ============================================
    if path is not None and len(path) > 1:
        # 경로의 x, y 좌표를 분리
        path_x = [pos[0] for pos in path]
        path_y = [pos[1] for pos in path]
        
        # 경로를 빨간 선으로 그리기
        plt.plot(
            path_x, path_y,
            color='red',
            linewidth=3,
            alpha=0.8,
            label=f'최단 경로 ({len(path)}단계)',
            marker='o',
            markersize=4
        )
        
        # ============================================
        # 6-1. 시작점과 도착점 강조
        # ============================================
        # 시작점 강조
        plt.scatter(
            [start[0]], [start[1]],
            c='red',
            marker='*',
            s=200,
            label='시작점 (내 집)',
            edgecolors='black',
            linewidth=2
        )
        
        # 도착점 강조
        plt.scatter(
            [end[0]], [end[1]],
            c='red',
            marker='*',
            s=200,
            label='도착점 (반달곰 커피)',
            edgecolors='black',
            linewidth=2
        )
    
    # ============================================
    # 7단계: 그래프 꾸미기
    # ============================================
    max_x = data['x'].max()
    max_y = data['y'].max()
    
    # y축을 뒤집어서 좌측 상단이 (1,1)이 되도록 설정
    plt.xlim(0, max_x + 1)
    plt.ylim(max_y + 1, 0)
    
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')
    plt.title('내 집에서 반달곰 커피까지의 최단 경로', fontsize=16, fontweight='bold')
    plt.legend(loc='upper right', fontsize=10)
    
    # 격자 번호 표시
    plt.xticks(range(1, max_x + 1, 2))
    plt.yticks(range(1, max_y + 1, 2))
    
    # ============================================
    # 8단계: 그래프 저장 및 표시
    # ============================================
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f'✅ 경로 시각화 완료: {save_path}')


def main() -> None:
    """
    메인 함수 - 프로그램의 시작점
    
    이 함수는 전체 프로그램의 실행 흐름을 관리합니다:
    1. 분석된 데이터 로드
    2. 격자 생성
    3. 시작점과 도착점 찾기
    4. 최단 경로 탐색
    5. 경로 저장 및 시각화
    """
    print('3단계: 최단 경로 탐색 시작\n')
    print('이 프로그램은 내 집에서 반달곰 커피까지의 최단 경로를 찾습니다.')
    print('=' * 60)
    
    # ============================================
    # 1단계: 분석된 데이터 불러오기
    # ============================================
    data = pd.read_csv('../area1_analyzed_data.csv')
    
    if data is None:
        print('❌ 데이터 로드에 실패했습니다.')
        return
    
    print(f'✅ 데이터 로드 완료: {len(data)}행')
    
    # ============================================
    # 2단계: 격자 생성
    # ============================================
    print('\n🗺 격자 생성 중...')
    grid, max_x, max_y = create_grid(data)
    print(f'   격자 크기: {max_x} x {max_y}')
    
    # ============================================
    # 3단계: 시작점과 도착점 찾기
    # ============================================
    print('\n📍 시작점과 도착점 찾는 중...')
    
    # 내 집 위치 찾기 (전체 데이터에서)
    myhome = data[(data['struct_name'] == 'MyHome') & (data['category'] != 0)]
    if len(myhome) == 0:
        print('❌ 내 집을 찾을 수 없습니다.')
        return
    
    start = (myhome.iloc[0]['x'], myhome.iloc[0]['y'])
    start_area = myhome.iloc[0]['area']
    print(f'   내 집 (시작점): {start} (area {start_area})')
    
    # 반달곰 커피 위치 찾기 (전체 데이터에서)
    coffee = data[(data['struct_name'] == 'BandalgomCoffee') & (data['category'] != 0)]
    if len(coffee) == 0:
        print('❌ 반달곰 커피를 찾을 수 없습니다.')
        return
    
    end = (coffee.iloc[0]['x'], coffee.iloc[0]['y'])
    end_area = coffee.iloc[0]['area']
    print(f'   반달곰 커피 (도착점): {end} (area {end_area})')
    
    # ============================================
    # 4단계: 최단 경로 탐색 (BFS)
    # ============================================
    print('\n🔍 최단 경로 탐색 중...')
    path = bfs_pathfinding(start, end, grid)
    
    if path is None:
        print('❌ 경로를 찾을 수 없습니다.')
        return
    
    # ============================================
    # 5단계: 경로를 CSV 파일로 저장
    # ============================================
    print('\n💾 경로 저장 중...')
    save_path_to_csv(path, 'home_to_cafe.csv')
    
    # ============================================
    # 6단계: 경로가 포함된 지도 시각화
    # ============================================
    print('\n🎨 경로 시각화 중...')
    visualize_path_with_map(data, path, start, end, 'map_final.png')
    
    # ============================================
    # 7단계: 완료 메시지
    # ============================================
    print('\n🎉 최단 경로 탐색 완료!')
    print('   - home_to_cafe.csv: 경로 데이터')
    print('   - map_final.png: 경로가 표시된 지도')
    print(f'   - 총 {len(path)}단계로 도착')
    print('   - BFS 알고리즘을 사용하여 최단 경로를 찾았습니다.')


# ============================================
# 프로그램 실행
# ============================================
if __name__ == '__main__':
    # 이 파일이 직접 실행될 때만 main() 함수를 호출
    # 다른 파일에서 import할 때는 실행되지 않음
    main() 