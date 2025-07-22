#!/usr/bin/env python3
"""map_draw.py
반달곰 커피 프로젝트 – 2단계 지도 시각화 (전 지역 시각화).

수정 내역
=========
* **area 1 전용 필터 제거** : 업로드된 전 지역 데이터를 모두 표시.
* 좌측 상단 (1, 1) 원점 규칙 유지.
* 나머지 마커·범례·경고 제거 로직은 동일.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / Path("dataFile")  # CSV 파일 위치

# ----------------------------------------------------------------------------
# 한글 폰트 설정
# ----------------------------------------------------------------------------


def set_korean_font() -> None:
    for font_name in ["AppleGothic", "NanumGothic", "Malgun Gothic"]:
        if any(font_name == f.name for f in fm.fontManager.ttflist):
            plt.rcParams["font.family"] = font_name
            return


# ----------------------------------------------------------------------------
# 데이터 로드 및 전처리
# ----------------------------------------------------------------------------


def read_csv(name: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / name)
    df.columns = df.columns.str.strip()
    return df


def load_and_prepare_data() -> pd.DataFrame:
    """세 CSV 병합 후 모든 지역 데이터를 반환한다."""

    map_df = read_csv("area_map.csv")
    struct_df = read_csv("area_struct.csv")
    cat_df = read_csv("area_category.csv")

    merged = struct_df.merge(cat_df, on="category", how="left").merge(
        map_df, on=["x", "y"], how="left"
    )

    merged["struct"] = merged["struct"].fillna("Empty").astype(str).str.strip()
    merged["ConstructionSite"] = merged["ConstructionSite"].fillna(0)

    return merged.reset_index(drop=True)


# ----------------------------------------------------------------------------
# 구조물 분류
# ----------------------------------------------------------------------------


def classify_kind(row: pd.Series) -> str:
    if int(row.get("ConstructionSite", 0)) == 1:
        return "construction"
    name = str(row["struct"]).lower()
    if "coffee" in name or "커피" in name:
        return "cafe"
    if any(key in name for key in ["myhome", "home", "house", "집"]):
        return "home"
    if "apartment" in name or "아파트" in name:
        return "apartment"
    if "building" in name or "빌딩" in name:
        return "building"
    return "other"


# ----------------------------------------------------------------------------
# 시각화
# ----------------------------------------------------------------------------


def plot_map(df: pd.DataFrame, output_path: Path) -> None:
    set_korean_font()

    df = df.copy()
    df["kind"] = df.apply(classify_kind, axis=1)

    # 좌표 범위 – 최소값 1 보장
    min_x = min(1, df["x"].min())
    min_y = min(1, df["y"].min())
    max_x = df["x"].max()
    max_y = df["y"].max()

    fig, ax = plt.subplots(figsize=(8, 8))

    for x_val in range(min_x, max_x + 1):
        ax.axvline(x_val, color="lightgray", linewidth=0.5, zorder=0)
    for y_val in range(min_y, max_y + 1):
        ax.axhline(y_val, color="lightgray", linewidth=0.5, zorder=0)

    marker_cfg: Dict[str, Tuple[str, str, str]] = {
        "apartment": ("o", "saddlebrown", "아파트/빌딩"),
        "building": ("o", "saddlebrown", "아파트/빌딩"),
        "cafe": ("s", "green", "반달곰 커피"),
        "home": ("^", "green", "내 집"),
        "construction": ("s", "grey", "공사장"),
    }

    plotted: List[str] = []

    def scatter(kind: str, rows: pd.DataFrame, z: int) -> None:
        marker, color, label = marker_cfg[kind]
        kw = {"label": label} if label not in plotted else {}
        ax.scatter(
            rows["x"],
            rows["y"],
            marker=marker,
            c=color,
            s=100,
            edgecolors="black",
            linewidths=0.5,
            zorder=z,
            **kw,
        )
        plotted.append(label)

    # 공사장 덮어쓰기
    for kind in ["apartment", "building", "cafe", "home"]:
        subset = df[df["kind"] == kind]
        if not subset.empty:
            scatter(kind, subset, 2)
    constr = df[df["kind"] == "construction"]
    if not constr.empty:
        scatter("construction", constr, 3)

    # 축 및 원점 (1,1)
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.legend(loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------------
# 메인
# ----------------------------------------------------------------------------


def main() -> None:
    df = load_and_prepare_data()
    out_path = Path(__file__).resolve().parent / "map.png"
    plot_map(df, out_path)
    print(f"Map saved → {out_path}")


if __name__ == "__main__":
    main()
