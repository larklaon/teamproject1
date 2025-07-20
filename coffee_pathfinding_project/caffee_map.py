#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1단계: 데이터 수집 및 분석
area_map.csv, area_struct.csv, area_category.csv 파일을 불러와 분석합니다.
"""

import pandas as pd
from typing import Optional


def load_and_analyze_data() -> Optional[pd.DataFrame]:  # type: ignore
    """
    세 개의 CSV 파일을 불러와서 분석하고 병합하는 함수
    
    Returns:
        Optional[pd.DataFrame]: 병합된 데이터프레임, 실패시 None
    """
    try:
        # ============================================
        # 1. CSV 파일들 불러오기
        # ============================================
        print('📂 CSV 파일들을 불러오는 중...')
        
        # area_map.csv: 지역과 좌표 정보를 담은 기본 지도 데이터
        area_map = pd.read_csv('dataFile/area_map.csv')
        print(f'✅ area_map.csv 로드 완료: {len(area_map)}행')
        print(f'   컬럼: {list(area_map.columns)}')
        print(f'   샘플 데이터:\n{area_map.head()}\n')
        
        # area_struct.csv: 구조물의 위치와 종류(ID)를 나타내는 데이터
        area_struct = pd.read_csv('dataFile/area_struct.csv')
        print(f'✅ area_struct.csv 로드 완료: {len(area_struct)}행')
        print(f'   컬럼: {list(area_struct.columns)}')
        print(f'   샘플 데이터:\n{area_struct.head()}\n')
        
        # area_category.csv: 구조물 종류 ID를 이름으로 매핑해주는 참조 데이터
        area_category = pd.read_csv('dataFile/area_category.csv')
        # 컬럼명의 공백 제거
        area_category.columns = area_category.columns.str.strip()
        print(f'✅ area_category.csv 로드 완료: {len(area_category)}행')
        print(f'   컬럼: {list(area_category.columns)}')
        print(f'   구조물 종류:\n{area_category}\n')
        
        # ============================================
        # 2. 구조물 ID를 이름으로 변환
        # ============================================
        print('🔄 구조물 ID를 이름으로 변환하는 중...')
        
        # category ID를 이름으로 매핑하는 딕셔너리 생성
        category_mapping = dict(zip(area_category['category'], area_category['struct']))
        print(f'   매핑 정보: {category_mapping}')
        
        # area_struct에 구조물 이름 컬럼 추가
        area_struct['struct_name'] = area_struct['category'].map(category_mapping)  # type: ignore
        print(f'   구조물 이름 변환 완료\n')
        
        # ============================================
        # 3. 세 데이터를 하나의 DataFrame으로 병합
        # ============================================
        print('🔗 데이터 병합 중...')
        
        # area_struct와 area_map을 x, y 좌표 기준으로 병합
        merged_data = pd.merge(area_struct, area_map, on=['x', 'y'], how='left')
        print(f'   병합 완료: {len(merged_data)}행')
        print(f'   병합 후 컬럼: {list(merged_data.columns)}')
        
        # area 기준으로 정렬
        merged_data = merged_data.sort_values(['area', 'x', 'y'])
        print(f'   area 기준 정렬 완료\n')
        
        # ============================================
        # 4. 전체 데이터 분석
        # ============================================
        print('📊 전체 데이터 분석...')
        print(f'   전체 행 수: {len(merged_data)}')
        print(f'   area별 데이터 수:')
        area_counts = merged_data['area'].value_counts().sort_index()  # type: ignore
        for area, count in area_counts.items():
            print(f'     area {area}: {count}행')
        
        # 구조물 종류별 분석
        print(f'\n   구조물 종류별 데이터 수:')
        struct_counts = merged_data['struct_name'].value_counts()  # type: ignore
        for struct, count in struct_counts.items():
            print(f'     {struct}: {count}개')
        
        # 반달곰 커피 위치 확인
        bandalgom_data = merged_data[merged_data['struct_name'] == 'BandalgomCoffee']
        print(f'\n   반달곰 커피 위치:')
        for _, row in bandalgom_data.iterrows():  # type: ignore
            print(f'     ({row["x"]}, {row["y"]}) - area {row["area"]}')
        
        # ============================================
        # 5. area 1에 대한 데이터만 필터링
        # ============================================
        print('\n🎯 area 1 데이터 필터링...')
        
        area1_data = merged_data[merged_data['area'] == 1].copy()
        print(f'   area 1 데이터: {len(area1_data)}행')
        
        # area 1의 구조물 종류별 분석
        print(f'   area 1 구조물 종류별 데이터 수:')
        area1_struct_counts = area1_data['struct_name'].value_counts()  # type: ignore
        for struct, count in area1_struct_counts.items():
            print(f'     {struct}: {count}개')
        
        # area 1의 반달곰 커피 위치
        area1_bandalgom = area1_data[area1_data['struct_name'] == 'BandalgomCoffee']
        print(f'\n   area 1 반달곰 커피 위치:')
        for _, row in area1_bandalgom.iterrows():  # type: ignore
            print(f'     ({row["x"]}, {row["y"]})')
        
        # area 1의 내 집 위치
        area1_myhome = area1_data[area1_data['struct_name'] == 'MyHome']
        print(f'\n   area 1 내 집 위치:')
        for _, row in area1_myhome.iterrows():  # type: ignore
            print(f'     ({row["x"]}, {row["y"]})')
        
        # ============================================
        # 6. 보너스: 구조물 종류별 요약 통계
        # ============================================
        print('\n📈 구조물 종류별 요약 통계 리포트')
        print('=' * 50)
        
        # 전체 통계
        print('전체 지역 통계:')
        total_stats = merged_data.groupby('struct_name').agg({
            'area': ['count', 'nunique'],
            'x': ['min', 'max'],
            'y': ['min', 'max']
        }).round(2)  # type: ignore
        print(total_stats)
        
        print('\narea 1 지역 통계:')
        area1_stats = area1_data.groupby('struct_name').agg({
            'x': ['min', 'max'],
            'y': ['min', 'max'],
            'ConstructionSite': 'sum'
        }).round(2)  # type: ignore
        print(area1_stats)
        
        return area1_data  # type: ignore
        
    except FileNotFoundError as e:
        print(f'❌ 파일을 찾을 수 없습니다: {e}')
        return None
    except Exception as e:
        print(f'❌ 오류가 발생했습니다: {e}')
        return None


def main() -> None:
    """
    메인 함수
    """
    print('🚀 1단계: 데이터 수집 및 분석 시작\n')
    
    # 데이터 분석 실행
    area1_data = load_and_analyze_data()
    
    if area1_data is not None:
        print('\n✅ 데이터 분석 완료!')
        print(f'   최종 결과: area 1 데이터 {len(area1_data)}행')
        print('\n📋 최종 데이터 샘플:')
        print(area1_data.head(10))
        
        # 결과를 CSV로 저장 (선택사항)
        area1_data.to_csv('area1_analyzed_data.csv', index=False)
        print('\n💾 분석 결과가 area1_analyzed_data.csv로 저장되었습니다.')
    else:
        print('\n❌ 데이터 분석에 실패했습니다.')


if __name__ == '__main__':
    main() 