# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import matplotlib.font_manager as fm

# ── 한글 폰트 로드 ──
font_path = "fonts/NanumGothic.ttf"            # 상대경로로 지정
fm.fontManager.addfont(font_path)               # 폰트 매니저에 등록
plt.rc("font", family="Nanum Gothic")           # Matplotlib 기본폰트 설정
plt.rcParams["axes.unicode_minus"] = False      # 마이너스 깨짐 방지

# — 페이지 설정
st.set_page_config(
    page_title="시그니처팟 월별 판매량 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(path, mtime):
    _ = mtime   # 이렇게라도 참조해 주면 “안 쓰이는 변수” 경고가 없어집니다
    return pd.read_excel(path, sheet_name=["판매점","직영점"])


# — 데이터 파일 경로 (필요 시 수정)
EXCEL_PATH = "시그니처팟_월별_판매량.xlsx"

# 파일 최종 수정 시간을 구해서 mtime 인자로 넘기면
# Excel 파일이 변경될 때마다 캐시가 무효화됩니다.
mtime = os.path.getmtime(EXCEL_PATH)
sheets = load_data(EXCEL_PATH, mtime)

# — 사이드바: 시트 선택
st.sidebar.title("⚙️ 설정")
sheet_name = st.sidebar.selectbox("▶ 시트 선택", list(sheets.keys()))
df = sheets[sheet_name]

# — 월별 컬럼 목록 (A,B 제외)
month_cols = df.columns[2:]

# — 대시보드 타이틀
st.title(f"📊 {sheet_name} 월별 판매량 대시보드")

# — 원본 데이터 보기
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)

# — 1) 월별 전체 판매수량 추이
st.subheader("1) 월별 전체 판매수량 추이")
monthly_total = df[month_cols].sum()

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(monthly_total.index, monthly_total.values)
ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title("월별 전체 판매수량")
plt.xticks(rotation=45)

# — 막대 위에 라벨 붙이기
for x, y in zip(monthly_total.index, monthly_total.values):
    ax.text(
        x, 
        y + max(monthly_total.values) * 0.01, 
        f"{int(y):,}", 
        ha='center', 
        va='bottom', 
        fontsize=9
    )

plt.tight_layout()
st.pyplot(fig)

# — 2) 품목별 판매 추이
st.subheader("2) 품목별 판매 추이")
item = st.selectbox("▶ 품목 선택", options=df["품명"].unique())
series = df[df["품명"] == item][month_cols].iloc[0]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(series.index, series.values, marker='o', linewidth=2)
ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title(f"{item} 판매 추이")
plt.xticks(rotation=45)

# — 각 점에 라벨 붙이기
for x, y in zip(series.index, series.values):
    # NaN은 건너뛰기
    if np.isnan(y):
        continue
    ax.text(
        x, 
        y + max(series.values[~np.isnan(series.values)]) * 0.003, 
        f"{int(y):,}", 
        ha='center', 
        va='bottom', 
        fontsize=9
    )

plt.tight_layout()
st.pyplot(fig)

# — 3) 상위 N개 품목 비교
st.subheader("3) 모든 품목 판매 추이 비교")
top_n = st.slider("▶ 상위 몇 개 품목?", min_value=1, max_value=10, value=5)
last_month = month_cols[-1]
top_items = df.nlargest(top_n, columns=last_month)["품명"].tolist()
df_top = df[df["품명"].isin(top_items)].set_index("품명")[month_cols].T

fig, ax = plt.subplots(figsize=(16, 10))
for it in top_items:
    ax.plot(df_top.index, df_top[it], marker='o', linewidth=1, label=it)

ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title(f"상위 {top_n}개 품목 판매 추이")
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)

# — 각 점에 라벨 붙이기
for it in top_items:
    xs = df_top.index
    ys = df_top[it].values
    y_offset = max(ys) * 0.01
    for x, y in zip(xs, ys):
        if not pd.isna(y):
            ax.text(
                x,
                y + y_offset,
                f"{int(y):,}",
                ha='center',
                va='bottom',
                fontsize=8
            )

plt.tight_layout()
st.pyplot(fig)

