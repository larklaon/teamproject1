#!/usr/bin/env python3
"""
caffee_map.py
~~~~~~~~~~~~~
반달곰 커피 프로젝트 1단계: 원본 CSV 세 개를 하나의 DataFrame으로
통합·정제하고 area 1 데이터와 구조물별 통계를 생성한다.

사용 방법::
    $ python caffee_map.py

출력:
    - area1_data.csv      : area 1의 상세 좌표·구조물·공사 여부
    - area1_summary.csv   : 구조물별 개수 요약
"""

from pathlib import Path
from typing import Tuple

import pandas as pd

# --------------------------------------------------------------------------- #
# 상수 정의
# --------------------------------------------------------------------------- #
BASE_DIR: Path = Path(__file__).resolve().parent
MAP_FILE: Path = BASE_DIR / "dataFile/area_map.csv"
STRUCT_FILE: Path = BASE_DIR / "dataFile/area_struct.csv"
CATEGORY_FILE: Path = BASE_DIR / "dataFile/area_category.csv"


# --------------------------------------------------------------------------- #
# 함수 정의
# --------------------------------------------------------------------------- #
def load_csv() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """CSV 세 개를 모두 읽어 DataFrame으로 반환한다."""
    area_map = pd.read_csv(MAP_FILE)
    area_struct = pd.read_csv(STRUCT_FILE)
    area_category = pd.read_csv(CATEGORY_FILE)
    return area_map, area_struct, area_category


def integrate_data(
    area_map: pd.DataFrame,
    area_struct: pd.DataFrame,
    area_category: pd.DataFrame,
) -> pd.DataFrame:
    """
    구조물·카테고리·공사 현장 정보를 하나로 통합한다.

    반환 DataFrame 컬럼:
        area, x, y, struct, constructionsite, category
    """
    merged = area_struct.merge(area_category, on="category", how="left").merge(
        area_map, on=["x", "y"], how="left"
    )

    # 컬럼 이름 공백 제거·소문자화
    merged.columns = merged.columns.str.strip().str.lower()

    # 컬럼 순서 재정렬
    ordered_cols = [
        "area",
        "x",
        "y",
        "struct",
        "constructionsite",
        "category",
    ]
    merged = merged[ordered_cols]

    # x, y, area 기준 정렬
    merged.sort_values(["area", "y", "x"], inplace=True, ignore_index=True)
    return merged


def filter_area_one(df: pd.DataFrame) -> pd.DataFrame:
    """area 값이 1인 행만 반환한다."""
    return df[df["area"] == 1].reset_index(drop=True)


def report_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    구조물(struct)별 개수를 집계해 반환한다.

    NaN(빈 칸)은 분석 대상이 아니므로 제외한다.
    """
    summary = (
        df.dropna(subset=["struct"])
        .groupby("struct", as_index=False)["struct"]
        .count()
        .rename(columns={"struct": "count"})
        .sort_values("count", ascending=False, ignore_index=True)
    )
    return summary


def main() -> None:
    """스크립트 실행 진입점."""
    area_map, area_struct, area_category = load_csv()

    combined = integrate_data(area_map, area_struct, area_category)
    area_one = filter_area_one(combined)
    summary = report_summary(area_one)

    # ────────────────────────── 결과 출력 ────────────────────────── #
    print("✅ area 1 데이터 (상위 10행)")
    print(area_one.head(10).to_string(index=False), "\n")

    print("✅ 구조물별 요약 통계")
    print(summary.to_string(index=False), "\n")

    # ────────────────────────── 파일 저장 ───────────────────────── #
    area_one.to_csv("area1_data.csv", index=False)
    summary.to_csv("area1_summary.csv", index=False)


# --------------------------------------------------------------------------- #
# 스크립트 실행
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()
