#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📘 1단계: 데이터 수집 및 분석
===========================================

이 파일은 세 개의 CSV 파일을 읽어서 분석하고 병합하는 역할을 합니다.

📁 입력 파일:
- dataFile/area_map.csv: 지역과 좌표 정보를 담은 기본 지도 데이터
- dataFile/area_struct.csv: 구조물의 위치와 종류(ID)를 나타내는 데이터  
- dataFile/area_category.csv: 구조물 종류 ID를 이름으로 매핑해주는 참조 데이터

📊 출력:
- area 1에 대한 필터링된 데이터
- 구조물 종류별 요약 통계 리포트

🔧 주요 기능:
1. CSV 파일 읽기 및 데이터 구조 파악
2. 구조물 ID를 의미있는 이름으로 변환
3. 세 데이터를 하나로 병합
4. area 1 데이터만 필터링
5. 통계 분석 및 리포트 생성

작성자: AI Assistant
날짜: 2024년
"""

import pandas as pd  # 데이터 분석을 위한 라이브러리
from typing import Optional  # 타입 힌트를 위한 라이브러리


def load_and_analyze_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    세 개의 CSV 파일을 불러와서 분석하고 병합하는 함수
    
    이 함수는 다음과 같은 작업을 수행합니다:
    1. 세 개의 CSV 파일을 읽어옵니다
    2. 구조물 ID를 의미있는 이름으로 변환합니다
    3. 데이터를 병합하고 정렬합니다
    4. area 1에 대한 데이터만 필터링합니다
    5. 통계 분석을 수행합니다
    
    Returns:
        Optional[pd.DataFrame]: 병합된 데이터프레임, 실패시 None
    """
    try:
        # ============================================
        # 1단계: CSV 파일들 불러오기
        # ============================================
        print('📂 CSV 파일들을 불러오는 중...')
        print('   이 단계에서는 세 개의 CSV 파일을 읽어서 데이터 구조를 파악합니다.')
        
        # ============================================
        # 1-1. area_map.csv 파일 읽기
        # ============================================
        # pd.read_csv(): CSV 파일을 pandas DataFrame으로 읽어오는 함수
        # 'dataFile/area_map.csv': 파일 경로
        area_map = pd.read_csv('../dataFile/area_map.csv')
        
        # len(area_map): DataFrame의 행 수를 반환
        print(f'✅ area_map.csv 로드 완료: {len(area_map)}행')
        
        # list(area_map.columns): DataFrame의 컬럼명들을 리스트로 반환
        print(f'   컬럼: {list(area_map.columns)}')
        
        # area_map.head(): 처음 5행을 보여주는 함수
        print(f'   샘플 데이터:\n{area_map.head()}\n')
        
        # ============================================
        # 1-2. area_struct.csv 파일 읽기
        # ============================================
        # 이 파일은 구조물의 위치(x, y)와 종류(category), 지역(area) 정보를 담고 있습니다
        area_struct = pd.read_csv('../dataFile/area_struct.csv')
        print(f'✅ area_struct.csv 로드 완료: {len(area_struct)}행')
        print(f'   컬럼: {list(area_struct.columns)}')
        print(f'   샘플 데이터:\n{area_struct.head()}\n')
        
        # ============================================
        # 1-3. area_category.csv 파일 읽기
        # ============================================
        # 이 파일은 구조물 종류 ID와 실제 이름을 매핑해주는 참조 테이블입니다
        area_category = pd.read_csv('../dataFile/area_category.csv')
        
        # 컬럼명에 공백이 있을 수 있으므로 제거합니다
        # .str.strip(): 문자열의 앞뒤 공백을 제거하는 함수
        area_category.columns = area_category.columns.str.strip()
        
        print(f'✅ area_category.csv 로드 완료: {len(area_category)}행')
        print(f'   컬럼: {list(area_category.columns)}')
        print(f'   구조물 종류:\n{area_category}\n')
        
        # ============================================
        # 2단계: 구조물 ID를 이름으로 변환
        # ============================================
        print('🔄 구조물 ID를 이름으로 변환하는 중...')
        print('   숫자로 된 구조물 ID를 사람이 이해하기 쉬운 이름으로 바꿉니다.')
        
        # ============================================
        # 2-1. 매핑 딕셔너리 생성
        # ============================================
        # dict(zip()): 두 리스트를 딕셔너리로 만드는 함수
        # area_category['category']: ID 리스트 (1, 2, 3, 4)
        # area_category['struct']: 이름 리스트 ('Apartment', 'Building', 'MyHome', 'BandalgomCoffee')
        # .str.strip(): 문자열의 앞뒤 공백을 제거
        category_mapping = dict(zip(area_category['category'], area_category['struct'].str.strip()))
        print(f'   매핑 정보: {category_mapping}')
        print('   예시: 1 → Apartment, 2 → Building, 3 → MyHome, 4 → BandalgomCoffee')
        
        # ============================================
        # 2-2. 구조물 이름 컬럼 추가
        # ============================================
        # .map(): Series의 각 값을 딕셔너리에 따라 변환하는 함수
        # category_mapping: 변환 규칙이 담긴 딕셔너리
        area_struct['struct_name'] = area_struct['category'].map(category_mapping)  # type: ignore
        print(f'   구조물 이름 변환 완료\n')
        
        # ============================================
        # 3단계: 세 데이터를 하나의 DataFrame으로 병합
        # ============================================
        print('🔗 데이터 병합 중...')
        print('   area_struct와 area_map을 x, y 좌표를 기준으로 합칩니다.')
        
        # ============================================
        # 3-1. 데이터 병합
        # ============================================
        # pd.merge(): 두 DataFrame을 특정 컬럼을 기준으로 병합하는 함수
        # on=['x', 'y']: x, y 좌표를 기준으로 병합
        # how='left': 왼쪽 DataFrame(area_struct)을 기준으로 병합
        merged_data = pd.merge(area_struct, area_map, on=['x', 'y'], how='left')
        print(f'   병합 완료: {len(merged_data)}행')
        print(f'   병합 후 컬럼: {list(merged_data.columns)}')
        
        # ============================================
        # 3-2. 데이터 정렬
        # ============================================
        # sort_values(): DataFrame을 특정 컬럼을 기준으로 정렬하는 함수
        # ['area', 'x', 'y']: area 먼저, 그 다음 x, 그 다음 y 순서로 정렬
        merged_data = merged_data.sort_values(['area', 'x', 'y'])
        print(f'   area 기준 정렬 완료\n')
        
        # ============================================
        # 4단계: 전체 데이터 분석
        # ============================================
        print('📊 전체 데이터 분석...')
        print('   모든 지역의 데이터를 분석하여 구조물 분포를 파악합니다.')
        
        # ============================================
        # 4-1. 기본 통계
        # ============================================
        print(f'   전체 행 수: {len(merged_data)}')
        
        # area별 데이터 수 계산
        # value_counts(): 각 값의 개수를 세는 함수
        # sort_index(): 인덱스를 기준으로 정렬
        area_counts = merged_data['area'].value_counts().sort_index()  # type: ignore
        print(f'   area별 데이터 수:')
        for area, count in area_counts.items():
            print(f'     area {area}: {count}행')
        
        # ============================================
        # 4-2. 구조물 종류별 분석
        # ============================================
        print(f'\n   구조물 종류별 데이터 수:')
        struct_counts = merged_data['struct_name'].value_counts()  # type: ignore
        for struct, count in struct_counts.items():
            print(f'     {struct}: {count}개')
        
        # ============================================
        # 4-3. 반달곰 커피 위치 확인
        # ============================================
        print(f'\n   반달곰 커피 위치:')
        bandalgom_data = merged_data[merged_data['struct_name'] == 'BandalgomCoffee']
        for _, row in bandalgom_data.iterrows():  # type: ignore
            print(f'     ({row["x"]}, {row["y"]}) - area {row["area"]}')
        
        # ============================================
        # 5단계: area 1에 대한 데이터만 필터링
        # ============================================
        print('\n🎯 area 1 데이터 필터링...')
        print('   요구사항에 따라 area 1에 대한 데이터만 선택합니다.')
        
        # ============================================
        # 5-1. area 1 데이터 선택
        # ============================================
        # merged_data['area'] == 1: area가 1인 행들만 선택하는 조건
        # .copy(): 원본 데이터를 변경하지 않기 위해 복사본 생성
        area1_data = merged_data[merged_data['area'] == 1].copy()
        print(f'   area 1 데이터: {len(area1_data)}행')
        
        # ============================================
        # 5-2. area 1 구조물 분석
        # ============================================
        print(f'   area 1 구조물 종류별 데이터 수:')
        area1_struct_counts = area1_data['struct_name'].value_counts()  # type: ignore
        for struct, count in area1_struct_counts.items():
            print(f'     {struct}: {count}개')
        
        # ============================================
        # 5-3. area 1 주요 구조물 위치
        # ============================================
        # 반달곰 커피 위치
        area1_bandalgom = area1_data[area1_data['struct_name'] == 'BandalgomCoffee']
        print(f'\n   area 1 반달곰 커피 위치:')
        for _, row in area1_bandalgom.iterrows():  # type: ignore
            print(f'     ({row["x"]}, {row["y"]})')
        
        # 내 집 위치 (area 1에는 없을 수 있음)
        area1_myhome = area1_data[area1_data['struct_name'] == 'MyHome']
        print(f'\n   area 1 내 집 위치:')
        if len(area1_myhome) > 0:
            for _, row in area1_myhome.iterrows():  # type: ignore
                print(f'     ({row["x"]}, {row["y"]})')
        else:
            print(f'     area 1에는 내 집이 없습니다.')
        
        # ============================================
        # 6단계: 보너스 - 구조물 종류별 요약 통계
        # ============================================
        print('\n📈 구조물 종류별 요약 통계 리포트')
        print('=' * 50)
        print('   이 섹션에서는 각 구조물의 상세한 통계 정보를 제공합니다.')
        
        # ============================================
        # 6-1. 전체 지역 통계
        # ============================================
        print('전체 지역 통계:')
        # groupby(): 특정 컬럼을 기준으로 그룹화
        # agg(): 각 그룹에 대해 여러 통계 함수를 적용
        total_stats = merged_data.groupby('struct_name').agg({
            'area': ['count', 'nunique'],  # 개수, 고유한 area 수
            'x': ['min', 'max'],           # x 좌표의 최소값, 최대값
            'y': ['min', 'max']            # y 좌표의 최소값, 최대값
        }).round(2)  # type: ignore
        print(total_stats)
        
        # ============================================
        # 6-2. area 1 지역 통계
        # ============================================
        print('\narea 1 지역 통계:')
        area1_stats = area1_data.groupby('struct_name').agg({
            'x': ['min', 'max'],           # x 좌표 범위
            'y': ['min', 'max'],           # y 좌표 범위
            'ConstructionSite': 'sum'      # 건설 현장 개수
        }).round(2)  # type: ignore
        print(area1_stats)
        
        # ============================================
        # 7단계: 결과 반환
        # ============================================
        print('\n✅ 데이터 분석 완료!')
        print(f'   최종 결과: area 1 데이터 {len(area1_data)}행')
        
        return area1_data  # type: ignore
        
    except FileNotFoundError as e:
        # 파일을 찾을 수 없는 경우의 오류 처리
        print(f'❌ 파일을 찾을 수 없습니다: {e}')
        print('   dataFile 폴더에 필요한 CSV 파일들이 있는지 확인해주세요.')
        return None
    except Exception as e:
        # 기타 예상치 못한 오류 처리
        print(f'❌ 오류가 발생했습니다: {e}')
        print('   코드를 다시 확인하거나 데이터 파일의 형식을 점검해주세요.')
        return None


def main() -> None:
    """
    메인 함수 - 프로그램의 시작점
    
    이 함수는 전체 프로그램의 실행 흐름을 관리합니다:
    1. 데이터 분석 함수 호출
    2. 결과 확인 및 출력
    3. 결과 파일 저장
    """
    print('1단계: 데이터 수집 및 분석 시작\n')
    print('이 프로그램은 세 개의 CSV 파일을 분석하여 지도 데이터를 생성합니다.')
    print('=' * 60)
    
    # ============================================
    # 1. 데이터 분석 실행
    # ============================================
    area1_data = load_and_analyze_data()
    
    # ============================================
    # 2. 결과 처리
    # ============================================
    if area1_data is not None:
        print('\n✅ 데이터 분석 완료!')
        print(f'   최종 결과: area 1 데이터 {len(area1_data)}행')
        
        # ============================================
        # 2-1. 최종 데이터 샘플 출력
        # ============================================
        print('\n📋 최종 데이터 샘플:')
        print('   처음 10행의 데이터를 보여줍니다.')
        print(area1_data.head(10))
        
        # ============================================
        # 2-2. 결과를 CSV로 저장 (선택사항)
        # ============================================
        # to_csv(): DataFrame을 CSV 파일로 저장하는 함수
        # index=False: 행 번호는 저장하지 않음
        area1_data.to_csv('area1_analyzed_data.csv', index=False)
        print('\n💾 분석 결과가 area1_analyzed_data.csv로 저장되었습니다.')
        print('   이 파일은 다음 단계에서 사용됩니다.')
        
        # ============================================
        # 2-3. 다음 단계 안내
        # ============================================
        print('\n🎯 다음 단계:')
        print('   2단계: map_draw.py를 실행하여 지도를 시각화하세요.')
        
    else:
        print('\n❌ 데이터 분석에 실패했습니다.')
        print('   오류 메시지를 확인하고 문제를 해결한 후 다시 시도해주세요.')


# ============================================
# 프로그램 실행
# ============================================
if __name__ == '__main__':
    # 이 파일이 직접 실행될 때만 main() 함수를 호출
    # 다른 파일에서 import할 때는 실행되지 않음
    main() 