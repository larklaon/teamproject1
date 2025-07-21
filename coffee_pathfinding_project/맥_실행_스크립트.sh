#!/bin/bash

# 🍎 맥 환경 커피 패스파인딩 프로젝트 자동 실행 스크립트
# 이 스크립트를 실행하면 모든 설정과 실행을 자동으로 해줍니다!

echo "🍎 커피 패스파인딩 프로젝트 자동 실행 스크립트 시작!"
echo "=================================================="

# 1. 현재 위치 확인
echo "📍 현재 위치 확인 중..."
pwd

# 2. Python 설치 확인
echo "🐍 Python 설치 확인 중..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3가 이미 설치되어 있습니다."
    python3 --version
else
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo "Homebrew를 통해 Python을 설치합니다..."
    
    # Homebrew 설치 확인
    if command -v brew &> /dev/null; then
        echo "✅ Homebrew가 이미 설치되어 있습니다."
    else
        echo "📦 Homebrew 설치 중..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "🐍 Python 설치 중..."
    brew install python
fi

# 3. 프로젝트 폴더로 이동
echo "📁 프로젝트 폴더로 이동 중..."
cd ~/Documents/cursor/teamproject1/coffee_pathfinding_project

# 4. 가상환경 확인 및 생성
echo "🔧 가상환경 설정 중..."
if [ -d "coffee_env" ]; then
    echo "✅ 가상환경이 이미 존재합니다."
else
    echo "📦 가상환경 생성 중..."
    python3 -m venv coffee_env
fi

# 5. 가상환경 활성화
echo "🚀 가상환경 활성화 중..."
source coffee_env/bin/activate

# 6. 필요한 라이브러리 설치
echo "📚 필요한 라이브러리 설치 중..."
pip install --upgrade pip
pip install pandas matplotlib numpy

# 7. 데이터 파일 확인
echo "📂 데이터 파일 확인 중..."
if [ -d "../dataFile" ]; then
    echo "✅ dataFile 폴더가 존재합니다."
    ls ../dataFile
else
    echo "❌ dataFile 폴더를 찾을 수 없습니다."
    echo "프로젝트 구조를 확인해주세요."
    exit 1
fi

# 8. 프로젝트 실행
echo "🎯 프로젝트 실행 중..."
echo "=================================================="
python test_all.py

# 9. 결과 확인
echo "=================================================="
echo "📊 실행 결과 확인 중..."
echo "생성된 파일들:"
ls -la *.png *.csv 2>/dev/null || echo "파일이 아직 생성되지 않았습니다."

echo "=================================================="
echo "🎉 스크립트 실행 완료!"
echo ""
echo "💡 다음에 실행할 때는:"
echo "1. 터미널 열기"
echo "2. cd ~/Documents/cursor/teamproject1/coffee_pathfinding_project"
echo "3. source coffee_env/bin/activate"
echo "4. python test_all.py"
echo ""
echo "🔧 가상환경 비활성화: deactivate" 