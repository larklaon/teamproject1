#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 전체 프로젝트 테스트 스크립트
===========================================

이 스크립트는 모든 단계를 순서대로 실행하여 프로젝트가 정상적으로 작동하는지 확인합니다.

실행 방법:
python test_all.py

작성자: AI Assistant
날짜: 2024년
"""

import sys
import os
import subprocess
import time

def run_step(step_name: str, script_name: str) -> bool:
    """
    각 단계를 실행하는 함수
    
    Args:
        step_name: str - 단계 이름
        script_name: str - 실행할 스크립트 이름
        
    Returns:
        bool: 성공 여부
    """
    print(f'\n{"="*60}')
    print(f'🚀 {step_name} 실행 중...')
    print(f'{"="*60}')
    
    try:
        # 현재 디렉토리를 상위로 변경
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 스크립트 실행
        result = subprocess.run([
            sys.executable, 
            f'coffee_pathfinding_project/{script_name}'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f'✅ {step_name} 성공!')
            print('출력:')
            print(result.stdout)
            return True
        else:
            print(f'❌ {step_name} 실패!')
            print('오류:')
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f'❌ {step_name} 시간 초과!')
        return False
    except Exception as e:
        print(f'❌ {step_name} 실행 중 오류: {e}')
        return False

def check_files() -> bool:
    """
    필요한 파일들이 생성되었는지 확인하는 함수
    
    Returns:
        bool: 모든 파일이 존재하는지 여부
    """
    print(f'\n{"="*60}')
    print('📁 생성된 파일 확인 중...')
    print(f'{"="*60}')
    
    required_files = [
        'coffee_pathfinding_project/area1_analyzed_data.csv',
        'coffee_pathfinding_project/map.png',
        'coffee_pathfinding_project/map_final.png',
        'coffee_pathfinding_project/home_to_cafe.csv'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f'✅ {file_path} (크기: {file_size} bytes)')
        else:
            print(f'❌ {file_path} (없음)')
            all_exist = False
    
    return all_exist

def main():
    """
    메인 함수 - 전체 테스트 실행
    """
    print('🧪 커피 경로찾기 프로젝트 전체 테스트 시작')
    print('이 스크립트는 모든 단계를 순서대로 실행합니다.')
    
    # 각 단계 실행
    steps = [
        ('1단계: 데이터 분석', 'caffee_map_detailed.py'),
        ('2단계: 지도 시각화', 'map_draw_detailed.py'),
        ('3단계: 경로 탐색', 'map_direct_save_detailed.py')
    ]
    
    success_count = 0
    for step_name, script_name in steps:
        if run_step(step_name, script_name):
            success_count += 1
        else:
            print(f'\n❌ {step_name}에서 실패했습니다. 테스트를 중단합니다.')
            break
    
    # 파일 확인
    files_ok = check_files()
    
    # 최종 결과
    print(f'\n{"="*60}')
    print('📊 최종 테스트 결과')
    print(f'{"="*60}')
    print(f'성공한 단계: {success_count}/{len(steps)}')
    print(f'파일 생성: {"✅ 성공" if files_ok else "❌ 실패"}')
    
    if success_count == len(steps) and files_ok:
        print('\n🎉 모든 테스트가 성공했습니다!')
        print('프로젝트가 정상적으로 작동합니다.')
    else:
        print('\n⚠️ 일부 테스트가 실패했습니다.')
        print('오류 메시지를 확인하고 문제를 해결해주세요.')

if __name__ == '__main__':
    main() 