#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3단계: 최단 경로 탐색
내 집에서 반달곰 커피까지의 최단 경로를 구합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'AppleGothic'  # 한글 폰트 설정 (Mac)
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 깨짐 방지
from collections import deque
from typing import Optional, List, Tuple


def load_analyzed_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    분석된 데이터를 불러오는 함수 (전체 데이터)
    
    Returns:
        Optional[pd.DataFrame]: 분석된 데이터프레임, 실패시 None
    """
    try:
        print('📂 전체 데이터 분석을 실행합니다...')
        
        # 1단계 분석 모듈 임포트 및 실행
        from caffee_map import load_and_analyze_data
        area1_data = load_and_analyze_data()
        if area1_data is None:
            return None
        
        # 전체 데이터를 다시 로드 (area 제한 없음)
        import pandas as pd
        
        # CSV 파일들 불러오기
        area_map = pd.read_csv('dataFile/area_map.csv')
        area_struct = pd.read_csv('dataFile/area_struct.csv')
        area_category = pd.read_csv('dataFile/area_category.csv')
        
        # 컬럼명의 공백 제거
        area_category.columns = area_category.columns.str.strip()
        
        # 구조물 ID를 이름으로 변환 (공백 제거)
        category_mapping = dict(zip(area_category['category'], area_category['struct'].str.strip()))
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
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        
    Returns:
        Tuple[List[List[int]], int, int]: (격자, 최대 x, 최대 y)
    """
    print('🗺️ 격자를 생성하는 중...')
    max_x = int(data['x'].max())
    max_y = int(data['y'].max())
    print(f'   격자 크기: {max_x} x {max_y}')
    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    # 건설 현장 배치 (최고 우선순위)
    construction_sites = data[data['ConstructionSite'] == 1]
    for _, row in construction_sites.iterrows():
        # 내 집, 반달곰 커피는 장애물로 처리하지 않음
        if row.get('struct_name') in ['MyHome', 'BandalgomCoffee']:
            continue
        grid[row['y']][row['x']] = 1
    print(f'   건설 현장 {len(construction_sites)}개 배치 완료')
    # 구조물 배치 (아파트/빌딩만 장애물로 처리)
    structures = data[(data['category'].isin([1, 2])) & (data['ConstructionSite'] == 0)]
    for _, row in structures.iterrows():
        # 내 집, 반달곰 커피는 장애물로 처리하지 않음
        if row.get('struct_name') in ['MyHome', 'BandalgomCoffee']:
            continue
        grid[row['y']][row['x']] = 2
    print(f'   아파트/빌딩 {len(structures)}개 배치 완료')
    return grid, max_x, max_y


def is_valid_position(pos: Tuple[int, int], grid: List[List[int]]) -> bool:
    """
    위치가 유효한지 확인하는 함수
    
    Args:
        pos: Tuple[int, int] - 확인할 위치 (x, y)
        grid: List[List[int]] - 격자
        
    Returns:
        bool: 유효한 위치인지 여부
    """
    x, y = pos
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return False
    return True


def bfs_pathfinding(start: Tuple[int, int], end: Tuple[int, int], 
                   grid: List[List[int]]) -> Optional[List[Tuple[int, int]]]:
    """
    BFS를 사용한 최단 경로 탐색
    
    Args:
        start: Tuple[int, int] - 시작점 (x, y)
        end: Tuple[int, int] - 도착점 (x, y)
        grid: List[List[int]] - 격자
        
    Returns:
        Optional[List[Tuple[int, int]]]: 경로 좌표 리스트, 실패시 None
    """
    # 입력값 유효성 검사
    if not is_valid_position(start, grid) or not is_valid_position(end, grid):
        print("시작점 또는 도착점이 격자 범위를 벗어났습니다.")
        return None
    
    # 시작점이나 도착점이 장애물인지 확인
    if grid[start[1]][start[0]] in [1, 2, 3, 4]:  # 건설 현장, 아파트/빌딩, 내 집, 반달곰 커피
        print(f"시작점 ({start[0]}, {start[1]})이 장애물입니다.")
        return None
    
    if grid[end[1]][end[0]] in [1, 2, 3, 4]:  # 건설 현장, 아파트/빌딩, 내 집, 반달곰 커피
        print(f"도착점 ({end[0]}, {end[1]})이 장애물입니다.")
        return None
    
    # BFS 초기화
    queue = deque([(start, [start])])
    visited = set([start])
    
    # 8방향 이동 정의 (상하좌우 + 대각선)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # 왼쪽 위, 위, 오른쪽 위
        (0, -1), (0, 1),             # 왼쪽, 오른쪽
        (1, -1), (1, 0), (1, 1)      # 왼쪽 아래, 아래, 오른쪽 아래
    ]
    
    # BFS 메인 루프
    while queue:
        current, path = queue.popleft()
        
        # 도착점에 도달했는지 확인
        if current == end:
            print(f"BFS로 경로를 찾았습니다! 길이: {len(path)} 단계")
            return path
        
        # 8방향으로 이동 시도
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)
            
            # 다음 위치가 유효하고 방문하지 않았고 장애물이 아니면
            if (next_pos not in visited and 
                is_valid_position(next_pos, grid) and 
                grid[next_y][next_x] not in [1, 2, 3, 4]):
                
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    print("BFS로 경로를 찾을 수 없습니다.")
    return None


def save_path_to_csv(path: Optional[List[Tuple[int, int]]], 
                    filename: str = 'home_to_cafe.csv') -> None:
    """
    경로를 CSV 파일로 저장하는 함수
    
    Args:
        path: Optional[List[Tuple[int, int]]] - 경로 좌표 리스트
        filename: str - 저장할 파일명
    """
    if path is None:
        print("❌ 경로가 없어서 CSV 파일을 저장할 수 없습니다.")
        return
    
    # 경로 데이터를 DataFrame으로 변환
    path_data = []
    for i, (x, y) in enumerate(path):
        path_data.append({
            'step': i + 1,
            'x': x,
            'y': y,
            'coordinate': f'({x}, {y})'
        })
    
    df = pd.DataFrame(path_data)
    df.to_csv(filename, index=False)
    
    print(f'✅ 경로가 {filename}로 저장되었습니다.')
    print(f'   총 단계 수: {len(path)}')
    print(f'   시작점: {path[0]}')
    print(f'   도착점: {path[-1]}')


def visualize_path_with_map(data: pd.DataFrame, path: Optional[List[Tuple[int, int]]], 
                           start: Tuple[int, int], end: Tuple[int, int],
                           save_path: str = 'map_final.png') -> None:
    """
    경로가 포함된 지도를 시각화하는 함수
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        path: Optional[List[Tuple[int, int]]] - 경로 좌표 리스트
        start: Tuple[int, int] - 시작점
        end: Tuple[int, int] - 도착점
        save_path: str - 저장할 파일 경로
    """
    # ============================================
    # 1. 시각화 설정 정의
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
    # 2. 그래프 창 생성
    # ============================================
    plt.figure(figsize=(12, 10))
    
    # ============================================
    # 3. 격자 그리기
    # ============================================
    plt.grid(True, alpha=0.3, color='gray')
    
    # ============================================
    # 4. 건설 현장 먼저 그리기
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
    # 5. 구조물별로 시각화하기
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
    # 6. 경로 그리기 (빨간 선)
    # ============================================
    if path is not None and len(path) > 1:
        path_x = [pos[0] for pos in path]
        path_y = [pos[1] for pos in path]
        
        plt.plot(
            path_x, path_y,
            color='red',
            linewidth=3,
            alpha=0.8,
            label=f'최단 경로 ({len(path)}단계)',
            marker='o',
            markersize=4
        )
        
        # 시작점과 도착점 강조
        plt.scatter(
            [start[0]], [start[1]],
            c='red',
            marker='*',
            s=200,
            label='시작점 (내 집)',
            edgecolors='black',
            linewidth=2
        )
        
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
    # 7. 그래프 꾸미기
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
    # 8. 그래프 저장 및 표시
    # ============================================
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f'✅ 경로 시각화 완료: {save_path}')


def main() -> None:
    """
    메인 함수
    """
    print('🚶 3단계: 최단 경로 탐색 시작\n')
    
    # 분석된 데이터 불러오기
    data = pd.read_csv('./area1_analyzed_data.csv')
    
    if data is None:
        print('❌ 데이터 로드에 실패했습니다.')
        return
    
    print(f'✅ 데이터 로드 완료: {len(data)}행')
    
    # ============================================
    # 1. 격자 생성
    # ============================================
    print('\n🗺 격자 생성 중...')
    grid, max_x, max_y = create_grid(data)
    print(f'   격자 크기: {max_x} x {max_y}')
    
    # ============================================
    # 2. 시작점과 도착점 찾기
    # ============================================
    print('\n📍 시작점과 도착점 찾는 중...')
    
    # 전체 데이터에서 내 집 위치 찾기 (area 제한 없음)
    myhome = data[(data['struct_name'] == 'MyHome') & (data['category'] != 0)]
    if len(myhome) == 0:
        print('❌ 내 집을 찾을 수 없습니다.')
        return
    
    start = (myhome.iloc[0]['x'], myhome.iloc[0]['y'])
    start_area = myhome.iloc[0]['area']
    print(f'   내 집 (시작점): {start} (area {start_area})')
    
    # 전체 데이터에서 반달곰 커피 위치 찾기 (area 제한 없음)
    coffee = data[(data['struct_name'] == 'BandalgomCoffee') & (data['category'] != 0)]
    if len(coffee) == 0:
        print('❌ 반달곰 커피를 찾을 수 없습니다.')
        return
    
    end = (coffee.iloc[0]['x'], coffee.iloc[0]['y'])
    end_area = coffee.iloc[0]['area']
    print(f'   반달곰 커피 (도착점): {end} (area {end_area})')
    
    # ============================================
    # 3. 최단 경로 탐색 (BFS)
    # ============================================
    print('\n🔍 최단 경로 탐색 중...')
    path = bfs_pathfinding(start, end, grid)
    
    if path is None:
        print('❌ 경로를 찾을 수 없습니다.')
        return
    
    # ============================================
    # 4. 경로를 CSV 파일로 저장
    # ============================================
    print('\n💾 경로 저장 중...')
    save_path_to_csv(path, 'home_to_cafe.csv')
    
    # ============================================
    # 5. 경로가 포함된 지도 시각화
    # ============================================
    print('\n🎨 경로 시각화 중...')
    visualize_path_with_map(data, path, start, end, 'map_final.png')
    
    print('\n🎉 최단 경로 탐색 완료!')
    print('   - home_to_cafe.csv: 경로 데이터')
    print('   - map_final.png: 경로가 표시된 지도')
    print(f'   - 총 {len(path)}단계로 도착')


if __name__ == '__main__':
    main() 