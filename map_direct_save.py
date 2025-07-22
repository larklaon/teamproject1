#!/usr/bin/env python3
"""map_direct_save.py
반달곰 커피 프로젝트 – 3단계 최단 경로 탐색 스크립트.

기능
----
1. `/dataFile` 내 CSV 3종을 병합해 전체 지도 DataFrame 생성.
2. MyHome(시작) → 반달곰 커피(도착) **최단 경로**를 BFS 로 탐색.
   * 공사장(ConstructionSite == 1) 칸은 통행 불가.
   * 이동은 상·하·좌·우 4방향, 가중치 1.
3. 경로를 `home_to_cafe.csv` 로 저장.
4. 기존 지도(2단계 규칙)를 다시 그린 뒤, 경로를 **빨간 선**으로 표시 → `map_final.png` 저장.

제약 준수 사항
--------------
* 외부 패키지 : **pandas, matplotlib** 만 사용.
* PEP 8 / 문자열·들여쓰기 규칙 준수, 경고 메시지 없이 실행.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# 설정 상수
# ---------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / Path("dataFile")  # CSV 파일 위치
OUTPUT_DIR = Path(__file__).resolve().parent

CSV_PATH = OUTPUT_DIR / "home_to_cafe.csv"
MAP_IMG = OUTPUT_DIR / "map_final.png"

# ---------------------------------------------------------------------------
# 공통 유틸 – 폰트, 데이터 로드, 구조물 분류
# ---------------------------------------------------------------------------


def set_korean_font() -> None:
    for name in ["AppleGothic", "NanumGothic", "Malgun Gothic"]:
        if any(name == f.name for f in fm.fontManager.ttflist):
            plt.rcParams["font.family"] = name
            return


def read_csv(name: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / name)
    df.columns = df.columns.str.strip()
    return df


def load_map_dataframe() -> pd.DataFrame:
    """area_map.csv, area_struct.csv, area_category.csv 병합 후 반환."""

    map_df = read_csv("area_map.csv")
    struct_df = read_csv("area_struct.csv")
    cat_df = read_csv("area_category.csv")

    merged = struct_df.merge(cat_df, on="category", how="left").merge(
        map_df, on=["x", "y"], how="left"
    )

    merged["struct"] = merged["struct"].fillna("Empty").astype(str).str.strip()
    merged["ConstructionSite"] = merged["ConstructionSite"].fillna(0).astype(int)

    return merged.reset_index(drop=True)


def classify_kind(row: pd.Series) -> str:
    if int(row["ConstructionSite"]) == 1:
        return "construction"
    name = str(row["struct"]).lower()
    if "coffee" in name or "커피" in name:
        return "cafe"
    if any(k in name for k in ["myhome", "home", "house", "집"]):
        return "home"
    if "apartment" in name or "아파트" in name:
        return "apartment"
    if "building" in name or "빌딩" in name:
        return "building"
    return "other"


# ---------------------------------------------------------------------------
# BFS 최단 경로 탐색
# ---------------------------------------------------------------------------


def bfs_shortest_path(
    obstacles: set[Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """장애물 집합·시작·목적 좌표로 구성된 BFS 최단 경로 반환."""

    if start == goal:
        return [start]

    queue: deque[Tuple[int, int]] = deque([start])
    parent: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        cx, cy = queue.popleft()
        for dx, dy in moves:
            nx, ny = cx + dx, cy + dy
            nxt = (nx, ny)
            if nxt in parent or nxt in obstacles:
                continue
            parent[nxt] = (cx, cy)
            if nxt == goal:
                return _reconstruct_path(parent, goal)
            queue.append(nxt)
    raise ValueError("경로를 찾을 수 없습니다.")


def _reconstruct_path(
    parent: Dict[Tuple[int, int], Tuple[int, int] | None],
    goal: Tuple[int, int],
) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    cur: Tuple[int, int] | None = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))


# ---------------------------------------------------------------------------
# 시각화
# ---------------------------------------------------------------------------


def plot_map_with_path(
    df: pd.DataFrame, path: List[Tuple[int, int]], out_path: Path
) -> None:
    set_korean_font()

    df = df.copy()
    df["kind"] = df.apply(classify_kind, axis=1)

    min_x = min(1, df["x"].min())
    min_y = min(1, df["y"].min())
    max_x = df["x"].max()
    max_y = df["y"].max()

    fig, ax = plt.subplots(figsize=(8, 8))

    # 격자
    for x_val in range(min_x, max_x + 1):
        ax.axvline(x_val, color="lightgray", linewidth=0.5, zorder=0)
    for y_val in range(min_y, max_y + 1):
        ax.axhline(y_val, color="lightgray", linewidth=0.5, zorder=0)

    marker_cfg: Dict[str, Tuple[str, str, str]] = {
        "apartment": ("o", "saddlebrown", "아파트/빌딩"),
        "building": ("o", "saddlebrown", "아파트/빌딩"),
        "cafe": ("s", "green", "반달곰 커피"),
        "home": ("^", "green", "내 집"),
        "construction": ("s", "grey", "건설 현장"),
    }

    plotted: List[str] = []

    def scatter(kind: str, rows: pd.DataFrame, z: int) -> None:
        m, c, label = marker_cfg[kind]
        kw = {"label": label} if label not in plotted else {}
        ax.scatter(
            rows["x"],
            rows["y"],
            marker=m,
            c=c,
            s=100,
            edgecolors="black",
            linewidths=0.5,
            zorder=z,
            **kw,
        )
        plotted.append(label)

    # 공사장을 맨 위에
    for k in ["apartment", "building", "cafe", "home"]:
        r = df[df["kind"] == k]
        if not r.empty:
            scatter(k, r, 2)
    constr = df[df["kind"] == "construction"]
    if not constr.empty:
        scatter("construction", constr, 3)

    # 경로 라인
    if len(path) > 1:
        xs, ys = zip(*path)
        ax.plot(xs, ys, c="red", linewidth=2, zorder=4, label="경로")

    # 축 설정
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
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 메인 흐름
# ---------------------------------------------------------------------------


def main() -> None:
    df = load_map_dataframe()

    # 시작·목적 좌표 찾기
    home_row = df[df["struct"].str.contains("myhome", case=False)]
    if home_row.empty:
        raise ValueError("MyHome 구조물을 찾을 수 없습니다.")
    cafe_row = df[
        df["struct"].str.contains("coffee", case=False)
        | df["struct"].str.contains("커피")
    ]
    if cafe_row.empty:
        raise ValueError("반달곰 커피 구조물을 찾을 수 없습니다.")

    start = (int(home_row.iloc[0]["x"]), int(home_row.iloc[0]["y"]))
    goal = (int(cafe_row.iloc[0]["x"]), int(cafe_row.iloc[0]["y"]))

    # 장애물 집합
    obstacles = {
        (int(r["x"]), int(r["y"]))
        for _, r in df.iterrows()
        if int(r["ConstructionSite"]) == 1
    }

    path = bfs_shortest_path(obstacles, start, goal)

    # CSV 저장
    pd.DataFrame(path, columns=["x", "y"]).to_csv(CSV_PATH, index=False)
    print(f"경로 CSV 저장 → {CSV_PATH}")

    # 지도 + 경로 시각화
    plot_map_with_path(df, path, MAP_IMG)
    print(f"경로 시각화 저장 → {MAP_IMG}")


if __name__ == "__main__":
    main()
