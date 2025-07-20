#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗺 2단계: 지도 시각화
===========================================

이 파일은 분석된 데이터를 기반으로 지역 지도를 시각화하는 역할을 합니다.

📁 입력:
- 1단계에서 생성된 분석 데이터 (area1_analyzed_data.csv 또는 caffee_map.py)

📊 출력:
- map.png: 시각화된 지도 이미지

🎨 시각화 규칙:
- 좌측 상단이 (1,1), 우측 하단이 가장 큰 좌표
- 아파트/빌딩: 갈색 원형
- 반달곰 커피: 녹색 사각형  
- 내 집: 녹색 삼각형
- 건설 현장: 회색 사각형
- 건설 현장이 다른 구조물과 겹치면 건설 현장 우선

🔧 주요 기능:
1. 분석된 데이터 로드
2. 구조물별 시각화 설정
3. matplotlib을 사용한 지도 그리기
4. 격자 및 범례 표시
5. PNG 파일로 저장

작성자: AI Assistant
날짜: 2024년
"""

import pandas as pd  # 데이터 처리를 위한 라이브러리
import matplotlib.pyplot as plt  # 그래프 그리기를 위한 라이브러리
import numpy as np  # 수치 계산을 위한 라이브러리
from typing import Optional, Tuple  # 타입 힌트를 위한 라이브러리


def load_analyzed_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    분석된 데이터를 불러오는 함수
    
    이 함수는 다음과 같은 우선순위로 데이터를 로드합니다:
    1. 기존에 저장된 area1_analyzed_data.csv 파일이 있으면 불러옴
    2. 없으면 1단계 분석을 실행하여 데이터 생성
    
    Returns:
        Optional[pd.DataFrame]: 분석된 데이터프레임, 실패시 None
    """
    try:
        # ============================================
        # 1단계: 기존 분석 데이터 확인
        # ============================================
        try:
            # 기존에 저장된 분석 데이터가 있는지 확인
            data = pd.read_csv('area1_analyzed_data.csv')
            print('✅ 기존 분석 데이터를 불러왔습니다.')
            print('   area1_analyzed_data.csv 파일에서 데이터를 읽어왔습니다.')
        except FileNotFoundError:
            # 기존 파일이 없으면 1단계 분석 실행
            print('📂 1단계 분석을 실행합니다...')
            print('   기존 분석 데이터가 없어서 새로 분석을 시작합니다.')
            
            # 1단계 분석 모듈 임포트 및 실행
            import sys
            import os
            # 상위 디렉토리를 Python 경로에 추가
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from coffee_pathfinding_project.caffee_map_detailed import load_and_analyze_data
            data = load_and_analyze_data()
            if data is None:
                return None
        
        return data
        
    except Exception as e:
        print(f'❌ 데이터 로드 오류: {e}')
        print('   데이터 파일이나 1단계 분석에 문제가 있을 수 있습니다.')
        return None


def create_map_visualization(data: pd.DataFrame, save_path: str = 'map.png') -> None:
    """
    지도를 시각화하는 함수
    
    이 함수는 다음과 같은 단계로 지도를 그립니다:
    1. 시각화 설정 정의
    2. 그래프 창 생성
    3. 격자 그리기
    4. 건설 현장 먼저 그리기
    5. 구조물별로 시각화
    6. 그래프 꾸미기
    7. 파일 저장
    
    Args:
        data: pd.DataFrame - 분석된 데이터
        save_path: str - 저장할 파일 경로
    """
    # ============================================
    # 1단계: 시각화 설정 정의
    # ============================================
    print('🎨 시각화 설정을 정의하는 중...')
    
    # 구조물별 시각화 설정을 딕셔너리로 정의
    # 각 구조물마다 색상, 모양, 크기, 라벨을 지정
    visual_config = {
        'Apartment': {
            'color': 'brown',      # 갈색
            'marker': 'o',         # 원형 (circle)
            'size': 100,           # 크기
            'label': '아파트/빌딩'  # 범례에 표시될 이름
        },
        'Building': {
            'color': 'brown',      # 갈색 (아파트와 동일)
            'marker': 'o',         # 원형
            'size': 100,           # 크기
            'label': '아파트/빌딩'  # 범례에 표시될 이름
        },
        'BandalgomCoffee': {
            'color': 'green',      # 녹색
            'marker': 's',         # 사각형 (square)
            'size': 120,           # 크기
            'label': '반달곰 커피'  # 범례에 표시될 이름
        },
        'MyHome': {
            'color': 'green',      # 녹색
            'marker': '^',         # 삼각형 (triangle)
            'size': 150,           # 크기
            'label': '내 집'       # 범례에 표시될 이름
        }
    }
    
    # ============================================
    # 2단계: 그래프 창 생성
    # ============================================
    print('📐 그래프 창을 생성하는 중...')
    
    # plt.figure(): 새로운 그래프 창을 생성하는 함수
    # figsize=(12, 10): 창의 크기를 가로 12인치, 세로 10인치로 설정
    plt.figure(figsize=(12, 10))
    
    # ============================================
    # 3단계: 격자 그리기
    # ============================================
    print('🔲 격자를 그리는 중...')
    
    # plt.grid(): 격자 선을 그리는 함수
    # True: 격자 표시
    # alpha=0.3: 투명도 30% (선이 연하게 보임)
    # color='gray': 격자 색상을 회색으로 설정
    plt.grid(True, alpha=0.3, color='gray')
    
    # ============================================
    # 4단계: 건설 현장 먼저 그리기 (회색 사각형)
    # ============================================
    print('🏗️ 건설 현장을 그리는 중...')
    
    # 건설 현장 데이터만 필터링
    # ConstructionSite == 1인 행들만 선택
    construction_sites = data[data['ConstructionSite'] == 1]
    
    if len(construction_sites) > 0:
        # plt.scatter(): 점들을 그리는 함수
        plt.scatter(
            construction_sites['x'],        # x 좌표
            construction_sites['y'],        # y 좌표
            c='gray',                       # 색상: 회색
            marker='s',                     # 모양: 사각형
            s=80,                           # 크기
            label='건설 현장',              # 범례 이름
            alpha=0.7,                      # 투명도 70%
            edgecolors='black',             # 테두리 색상: 검정
            linewidth=1                     # 테두리 두께
        )
        print(f'   건설 현장 {len(construction_sites)}개를 그렸습니다.')
    else:
        print('   건설 현장이 없습니다.')
    
    # ============================================
    # 5단계: 구조물별로 시각화하기
    # ============================================
    print('🏠 구조물들을 그리는 중...')
    
    # 구조물 종류별로 순서대로 그리기
    # 순서가 중요한 이유: 나중에 그린 것이 위에 표시됨
    for struct_type in ['Apartment', 'Building', 'BandalgomCoffee', 'MyHome']:
        # 해당 타입의 데이터만 필터링
        # category가 0이 아닌 경우만 (실제 구조물이 있는 경우)
        type_data = data[(data['struct_name'] == struct_type) & (data['category'] != 0)]
        
        if len(type_data) > 0:  # 데이터가 있는 경우만
            # 시각화 설정 가져오기
            config = visual_config[struct_type]
            
            # plt.scatter(): 점들을 그리기
            plt.scatter(
                type_data['x'],             # x 좌표
                type_data['y'],             # y 좌표
                c=config['color'],          # 색상
                marker=config['marker'],    # 모양
                s=config['size'],           # 크기
                label=config['label'],      # 범례 이름
                alpha=0.8,                  # 투명도 80%
                edgecolors='black',         # 테두리 색상
                linewidth=1.5               # 테두리 두께
            )
            print(f'   {config["label"]} {len(type_data)}개를 그렸습니다.')
        else:
            print(f'   {struct_type}이(가) 없습니다.')
    
    # ============================================
    # 6단계: 그래프 꾸미기
    # ============================================
    print('🎨 그래프를 꾸미는 중...')
    
    # ============================================
    # 6-1. 좌표계 설정
    # ============================================
    # 데이터에서 가장 큰 x, y 좌표를 찾기
    max_x = data['x'].max()
    max_y = data['y'].max()
    
    # 좌표계 설정 (좌측 상단이 (1,1)이 되도록)
    # plt.xlim(): x축 범위 설정
    # plt.ylim(): y축 범위 설정 (y축을 뒤집어서 좌측 상단이 (1,1)이 되도록)
    plt.xlim(0, max_x + 1)
    plt.ylim(max_y + 1, 0)  # y축 뒤집기
    
    # ============================================
    # 6-2. 축 라벨 설정
    # ============================================
    # plt.xlabel(): x축 라벨 설정
    # plt.ylabel(): y축 라벨 설정
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')
    
    # ============================================
    # 6-3. 제목 설정
    # ============================================
    # plt.title(): 그래프 제목 설정
    # fontsize=16: 글자 크기
    # fontweight='bold': 굵은 글씨
    plt.title('Area 1 지도 시각화', fontsize=16, fontweight='bold')
    
    # ============================================
    # 6-4. 범례 표시
    # ============================================
    # plt.legend(): 범례 표시
    # loc='upper right': 오른쪽 위에 위치
    # fontsize=10: 글자 크기
    plt.legend(loc='upper right', fontsize=10)
    
    # ============================================
    # 6-5. 격자 번호 표시
    # ============================================
    # plt.xticks(): x축 눈금 설정
    # plt.yticks(): y축 눈금 설정
    # range(1, max_x + 1, 2): 1부터 max_x까지 2씩 증가
    plt.xticks(range(1, max_x + 1, 2))
    plt.yticks(range(1, max_y + 1, 2))
    
    # ============================================
    # 7단계: 그래프 저장 및 표시
    # ============================================
    print('💾 그래프를 저장하는 중...')
    
    # plt.tight_layout(): 그래프 요소들을 자동으로 정렬
    plt.tight_layout()
    
    # plt.savefig(): 그래프를 파일로 저장
    # dpi=300: 해상도 (높을수록 선명)
    # bbox_inches='tight': 여백을 자동으로 조정
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # plt.show(): 그래프를 화면에 표시
    plt.show()
    
    print(f'✅ 지도 시각화 완료: {save_path}')
    print(f'   지도 크기: {max_x} x {max_y}')
    
    # ============================================
    # 8단계: 구조물 위치 정보 출력
    # ============================================
    print('\n📍 주요 구조물 위치:')
    
    # 내 집 위치
    myhome = data[(data['struct_name'] == 'MyHome') & (data['category'] != 0)]
    if len(myhome) > 0:
        for _, row in myhome.iterrows():
            print(f'   내 집: ({row["x"]}, {row["y"]})')
    else:
        print('   내 집: area 1에 없습니다.')
    
    # 반달곰 커피 위치
    coffee = data[(data['struct_name'] == 'BandalgomCoffee') & (data['category'] != 0)]
    if len(coffee) > 0:
        for _, row in coffee.iterrows():
            print(f'   반달곰 커피: ({row["x"]}, {row["y"]})')
    else:
        print('   반달곰 커피: area 1에 없습니다.')
    
    # 건설 현장 개수
    construction_count = len(construction_sites)
    print(f'   건설 현장: {construction_count}개')


def main() -> None:
    """
    메인 함수 - 프로그램의 시작점
    
    이 함수는 전체 프로그램의 실행 흐름을 관리합니다:
    1. 분석된 데이터 로드
    2. 지도 시각화 실행
    3. 결과 안내
    """
    print('2단계: 지도 시각화 시작\n')
    print('이 프로그램은 분석된 데이터를 기반으로 지도를 시각화합니다.')
    print('=' * 60)
    
    # ============================================
    # 1. 분석된 데이터 불러오기
    # ============================================
    data = load_analyzed_data()
    
    # ============================================
    # 2. 데이터 로드 결과 확인
    # ============================================
    if data is not None:
        print(f'✅ 데이터 로드 완료: {len(data)}행')
        
        # ============================================
        # 3. 지도 시각화 실행
        # ============================================
        create_map_visualization(data, 'map.png')
        
        # ============================================
        # 4. 완료 메시지
        # ============================================
        print('\n🎉 지도 시각화 완료!')
        print('   - map.png 파일이 생성되었습니다.')
        print('   - 좌측 상단이 (1,1) 좌표입니다.')
        print('   - 각 구조물이 지정된 모양과 색상으로 표시됩니다.')
        print('   - 건설 현장이 다른 구조물과 겹치면 건설 현장이 우선 표시됩니다.')
        
        # ============================================
        # 5. 다음 단계 안내
        # ============================================
        print('\n🎯 다음 단계:')
        print('   3단계: map_direct_save.py를 실행하여 최단 경로를 찾으세요.')
        
    else:
        print('\n❌ 데이터 로드에 실패했습니다.')
        print('   먼저 1단계(caffee_map_detailed.py)를 실행해주세요.')


# ============================================
# 프로그램 실행
# ============================================
if __name__ == '__main__':
    # 이 파일이 직접 실행될 때만 main() 함수를 호출
    # 다른 파일에서 import할 때는 실행되지 않음
    main() 