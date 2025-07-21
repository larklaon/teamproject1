#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2단계: 지도 시각화
분석된 데이터를 기반으로 지역 지도를 시각화합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def load_analyzed_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    분석된 데이터를 불러오는 함수
    
    Returns:
        Optional[pd.DataFrame]: 분석된 데이터프레임, 실패시 None
    """
    try:
        # area1_analyzed_data.csv가 있으면 불러오고, 없으면 1단계 분석 실행
        try:
            data = pd.read_csv('area1_analyzed_data.csv')
            print('✅ 기존 분석 데이터를 불러왔습니다.')
        except FileNotFoundError:
            print('📂 1단계 분석을 실행합니다...')
            # 1단계 분석 모듈 임포트 및 실행
            from caffee_map import load_and_analyze_data
            data = load_and_analyze_data()
            if data is None:
                return None
        
        return data
        
    except Exception as e:
        print(f'❌ 데이터 로드 오류: {e}')
        return None


def create_map_visualization(data: pd.DataFrame, save_path: str = 'map.png') -> None:
    """
    지도를 시각화하는 함수
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        save_path: str - 저장할 파일 경로
    """
    # ============================================
    # 1. 시각화 설정 정의
    # ============================================
    # 구조물별 시각화 설정
    visual_config = {
        'Apartment': {
            'color': 'brown',
            'marker': 'o',  # 원형
            'size': 100,
            'label': '아파트/빌딩'
        },
        'Building': {
            'color': 'brown',
            'marker': 'o',  # 원형
            'size': 100,
            'label': '아파트/빌딩'
        },
        'BandalgomCoffee': {
            'color': 'green',
            'marker': 's',  # 사각형
            'size': 120,
            'label': '반달곰 커피'
        },
        'MyHome': {
            'color': 'green',
            'marker': '^',  # 삼각형
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
    # 4. 건설 현장 먼저 그리기 (회색 사각형)
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
    # 구조물 종류별로 순서대로 그리기
    for struct_type in ['Apartment', 'Building', 'BandalgomCoffee', 'MyHome']:
        # 해당 타입의 데이터만 필터링 (category가 0이 아닌 경우)
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
    # 6. 그래프 꾸미기
    # ============================================
    # 좌표계 설정 (좌측 상단이 (1,1))
    max_x = data['x'].max()
    max_y = data['y'].max()
    
    # y축을 뒤집어서 좌측 상단이 (1,1)이 되도록 설정
    plt.xlim(0, max_x + 1)
    plt.ylim(max_y + 1, 0)  # y축 뒤집기
    
    # 축 라벨 설정
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')
    
    # 제목 설정
    plt.title('Area 1 지도 시각화', fontsize=16, fontweight='bold')
    
    # 범례 표시
    plt.legend(loc='upper right', fontsize=10)
    
    # 격자 번호 표시
    plt.xticks(range(1, max_x + 1, 2))
    plt.yticks(range(1, max_y + 1, 2))
    
    # ============================================
    # 7. 그래프 저장 및 표시
    # ============================================
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f'✅ 지도 시각화 완료: {save_path}')
    print(f'   지도 크기: {max_x} x {max_y}')
    
    # ============================================
    # 8. 구조물 위치 정보 출력
    # ============================================
    print('\n📍 주요 구조물 위치:')
    
    # 내 집 위치
    myhome = data[(data['struct_name'] == 'MyHome') & (data['category'] != 0)]
    if len(myhome) > 0:
        for _, row in myhome.iterrows():
            print(f'   내 집: ({row["x"]}, {row["y"]})')
    
    # 반달곰 커피 위치
    coffee = data[(data['struct_name'] == 'BandalgomCoffee') & (data['category'] != 0)]
    if len(coffee) > 0:
        for _, row in coffee.iterrows():
            print(f'   반달곰 커피: ({row["x"]}, {row["y"]})')
    
    # 건설 현장 개수
    construction_count = len(construction_sites)
    print(f'   건설 현장: {construction_count}개')


def main() -> None:
    """
    메인 함수
    """
    print('🗺 2단계: 지도 시각화 시작\n')
    
    # 분석된 데이터 불러오기
    data = load_analyzed_data()
    
    if data is not None:
        print(f'✅ 데이터 로드 완료: {len(data)}행')
        
        # 지도 시각화 실행
        create_map_visualization(data, 'map.png')
        
        print('\n🎉 지도 시각화 완료!')
        print('   - map.png 파일이 생성되었습니다.')
        print('   - 좌측 상단이 (1,1) 좌표입니다.')
        print('   - 각 구조물이 지정된 모양과 색상으로 표시됩니다.')
    else:
        print('\n❌ 데이터 로드에 실패했습니다.')


if __name__ == '__main__':
    main() 