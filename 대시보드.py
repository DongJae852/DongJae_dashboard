# # app.py

# import os
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import numpy as np
# import requests
# import tempfile

# # ── 한글 폰트(나눔고딕) 웹에서 동적 로드 ──
# font_url = (
#     "https://github.com/google/fonts/raw/main/ofl/nanumgothic/"
#     "NanumGothic-Regular.ttf"
# )
# resp = requests.get(font_url)
# resp.raise_for_status()
# with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as tmp:
#     tmp.write(resp.content)
#     tmp_path = tmp.name

# fm.fontManager.addfont(tmp_path)
# plt.rc("font", family="Nanum Gothic")
# plt.rcParams["axes.unicode_minus"] = False

# # — 페이지 설정
# st.set_page_config(
#     page_title="시그니처팟 월별 판매량 대시보드",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# @st.cache_data
# def load_data(path, mtime):
#     _ = mtime
#     return pd.read_excel(path, sheet_name=["판매점", "직영점"])

# # — 데이터 파일 경로 (레포 루트 기준)
# EXCEL_PATH = "시그니처팟_월별_판매량_4월.xlsx"
# if not os.path.exists(EXCEL_PATH):
#     st.error(f"데이터 파일이 없습니다: '{EXCEL_PATH}'")
#     st.stop()

# mtime = os.path.getmtime(EXCEL_PATH)
# sheets = load_data(EXCEL_PATH, mtime)

# # — 사이드바: 시트 선택
# st.sidebar.title("⚙️ 설정")
# sheet_name = st.sidebar.selectbox("▶ 시트 선택", list(sheets.keys()))
# df = sheets[sheet_name]

# # — 월별 컬럼 목록 (A,B 제외)
# month_cols = df.columns[2:]

# # — 대시보드 타이틀
# st.title(f"📊 {sheet_name} 월별 판매량 대시보드")

# # — 원본 데이터 보기
# with st.expander("🔍 원본 데이터 보기"):
#     st.dataframe(df, use_container_width=True)

# # — 1) 월별 전체 판매수량 추이
# st.subheader("1) 월별 전체 판매수량 추이")
# monthly_total = df[month_cols].sum()

# fig, ax = plt.subplots(figsize=(10, 5))
# ax.bar(monthly_total.index, monthly_total.values)
# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title("월별 전체 판매수량")
# plt.xticks(rotation=45)

# bar_offset = max(monthly_total.values) * 0.01
# for x, y in zip(monthly_total.index, monthly_total.values):
#     ax.text(x, y + bar_offset, f"{int(y):,}", ha='center', va='bottom', fontsize=9)

# plt.tight_layout()
# st.pyplot(fig)

# # — 2) 품목별 판매 추이
# st.subheader("2) 품목별 판매 추이")
# item = st.selectbox("▶ 품목 선택", options=df["품명"].unique())
# series = df[df["품명"] == item][month_cols].iloc[0]

# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(series.index, series.values, marker='o', linewidth=2)
# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title(f"{item} 판매 추이")
# plt.xticks(rotation=45)

# offset = max(series.values[~np.isnan(series.values)]) * 0.003
# for x, y in zip(series.index, series.values):
#     if not np.isnan(y):
#         ax.text(x, y + offset, f"{int(y):,}", ha='center', va='bottom', fontsize=9)

# plt.tight_layout()
# st.pyplot(fig)

# # — 3) 상위 N개 품목 비교
# st.subheader("3) 상위 N개 품목 판매 추이")
# top_n = st.slider("▶ 상위 몇 개 품목?", min_value=1, max_value=10, value=5)
# last_month = month_cols[-1]
# top_items = df.nlargest(top_n, columns=last_month)["품명"].tolist()
# df_top = df[df["품명"].isin(top_items)].set_index("품명")[month_cols].T

# fig, ax = plt.subplots(figsize=(16, 10))
# for it in top_items:
#     ax.plot(df_top.index, df_top[it], marker='o', linewidth=1, label=it)

# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title(f"상위 {top_n}개 품목 판매 추이")
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=6, fontsize=8)
# plt.xticks(rotation=45)

# y_offset_base = df_top.max().max() * 0.01
# for it in top_items:
#     ys = df_top[it].values
#     for x, y in zip(df_top.index, ys):
#         if not np.isnan(y):
#             ax.text(x, y + y_offset_base, f"{int(y):,}", ha='center', va='bottom', fontsize=8)

# plt.tight_layout()
# st.pyplot(fig)




# # app.py

# import os
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import numpy as np
# import requests
# import tempfile

# # ── 1) 페이지 설정 ──
# st.set_page_config(
#     page_title="시그니처팟 월별 판매량 대시보드",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ── 2) Streamlit UI용 한글 폰트 적용 via Google Fonts ──
# st.markdown(
#     """
#     <style>
#       @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');
#       html, body, [class*="css"] {
#         font-family: 'Noto Sans KR', sans-serif;
#       }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ── 3) Matplotlib 차트용 한글 폰트 동적 로드 ──
# font_url = (
#     "https://github.com/google/fonts/raw/main/ofl/nanumgothic/"
#     "NanumGothic-Regular.ttf"
# )
# resp = requests.get(font_url)
# resp.raise_for_status()
# with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as tmp:
#     tmp.write(resp.content)
#     tmp_path = tmp.name

# fm.fontManager.addfont(tmp_path)
# plt.rc("font", family="Nanum Gothic")
# plt.rcParams["axes.unicode_minus"] = False  # 마이너스 깨짐 방지

# # ── 4) 캐시된 데이터 로드 함수 ──
# @st.cache_data
# def load_data(path, mtime):
#     _ = mtime  # 캐시 무효화용 인자
#     return pd.read_excel(path, sheet_name=["판매점", "직영점"])

# # ── 5) Excel 파일 경로 및 로드 ──
# EXCEL_PATH = "시그니처팟_월별_판매량.xlsx"
# if not os.path.exists(EXCEL_PATH):
#     st.error(f"데이터 파일이 없습니다: '{EXCEL_PATH}'")
#     st.stop()

# mtime = os.path.getmtime(EXCEL_PATH)
# sheets = load_data(EXCEL_PATH, mtime)

# # ── 6) 사이드바: 시트 선택 ──
# st.sidebar.title("⚙️ 설정")
# sheet_name = st.sidebar.selectbox("▶ 시트 선택", list(sheets.keys()))
# df = sheets[sheet_name]

# # ── 7) 월별 컬럼 추출 ──
# month_cols = df.columns[2:]

# # ── 8) 대시보드 타이틀 ──
# st.title(f"📊 {sheet_name} 월별 판매량 대시보드")

# # ── 9) 원본 데이터 보기 ──
# with st.expander("🔍 원본 데이터 보기"):
#     st.dataframe(df, use_container_width=True)

# # ── 10) 월별 전체 판매수량 추이 ──
# st.subheader("1) 월별 전체 판매수량 추이")
# monthly_total = df[month_cols].sum()
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.bar(monthly_total.index, monthly_total.values)
# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title("월별 전체 판매수량")
# plt.xticks(rotation=45)
# bar_offset = max(monthly_total.values) * 0.01
# for x, y in zip(monthly_total.index, monthly_total.values):
#     ax.text(x, y + bar_offset, f"{int(y):,}", ha='center', va='bottom', fontsize=9)
# plt.tight_layout()
# st.pyplot(fig)

# # ── 11) 품목별 판매 추이 ──
# st.subheader("2) 품목별 판매 추이")
# item = st.selectbox("▶ 품목 선택", options=df["품명"].unique())
# series = df[df["품명"] == item][month_cols].iloc[0]
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(series.index, series.values, marker='o', linewidth=2)
# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title(f"{item} 판매 추이")
# plt.xticks(rotation=45)
# offset = max(series.values[~np.isnan(series.values)]) * 0.003
# for x, y in zip(series.index, series.values):
#     if not np.isnan(y):
#         ax.text(x, y + offset, f"{int(y):,}", ha='center', va='bottom', fontsize=9)
# plt.tight_layout()
# st.pyplot(fig)

# # ── 12) 상위 N개 품목 판매 추이 ──
# st.subheader("3) 상위 N개 품목 판매 추이")
# top_n = st.slider("▶ 상위 몇 개 품목?", min_value=1, max_value=10, value=5)
# last_month = month_cols[-1]
# top_items = df.nlargest(top_n, columns=last_month)["품명"].tolist()
# df_top = df[df["품명"].isin(top_items)].set_index("품명")[month_cols].T
# fig, ax = plt.subplots(figsize=(16, 10))
# for it in top_items:
#     ax.plot(df_top.index, df_top[it], marker='o', linewidth=1, label=it)
# ax.set_xlabel("월별")
# ax.set_ylabel("판매수량")
# ax.set_title(f"상위 {top_n}개 품목 판매 추이")
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=6, fontsize=8)
# plt.xticks(rotation=45)
# y_offset_base = df_top.max().max() * 0.01
# for it in top_items:
#     for x, y in zip(df_top.index, df_top[it].values):
#         if not np.isnan(y):
#             ax.text(x, y + y_offset_base, f"{int(y):,}", ha='center', va='bottom', fontsize=8)
# plt.tight_layout()
# st.pyplot(fig)





# app.py

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import requests
import tempfile

# ──────────────────────────────────────────────────────────
# 1) 페이지 설정 (반드시 최상단에)
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="시그니처팟 월별 판매량 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────
# 2) Streamlit UI 전체에 구글 Noto Sans KR 적용
#    (사이드바, 위젯, 텍스트 등)
# ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');
      html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────
# 3) Matplotlib 차트용 한글 폰트 나눔고딕 동적 로드
# ──────────────────────────────────────────────────────────
font_url = (
    "https://github.com/google/fonts/raw/main/ofl/nanumgothic/"
    "NanumGothic-Regular.ttf"
)
resp = requests.get(font_url)
resp.raise_for_status()
with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as tmp:
    tmp.write(resp.content)
    tmp_path = tmp.name

fm.fontManager.addfont(tmp_path)
plt.rc("font", family="Nanum Gothic")
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

# ──────────────────────────────────────────────────────────
# 4) 데이터 로드 캐시 함수
# ──────────────────────────────────────────────────────────
@st.cache_data
def load_data(path, mtime):
    _ = mtime  # 캐시 무효화용
    return pd.read_excel(path, sheet_name=["판매점", "직영점"])


# ──────────────────────────────────────────────────────────
# 5) 엑셀 파일 경로 체크 & 로드
# ──────────────────────────────────────────────────────────
EXCEL_PATH = "시그니처팟_월별_판매량_4월.xlsx"
if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ 데이터 파일이 없습니다: '{EXCEL_PATH}'")
    st.stop()

mtime = os.path.getmtime(EXCEL_PATH)
sheets = load_data(EXCEL_PATH, mtime)


# ──────────────────────────────────────────────────────────
# 6) 사이드바에서 시트 선택
# ──────────────────────────────────────────────────────────
st.sidebar.title("⚙️ 설정")
sheet_name = st.sidebar.selectbox("▶ 시트 선택", list(sheets.keys()))
df = sheets[sheet_name]


# ──────────────────────────────────────────────────────────
# 7) 월별 컬럼 목록 생성 (A,B 제외)
# ──────────────────────────────────────────────────────────
month_cols = df.columns[2:]


# ──────────────────────────────────────────────────────────
# 8) 대시보드 제목
# ──────────────────────────────────────────────────────────
st.title(f"📊 {sheet_name} 월별 판매량 대시보드")


# ──────────────────────────────────────────────────────────
# 9) 원본 데이터 펼쳐보기
# ──────────────────────────────────────────────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)


# ──────────────────────────────────────────────────────────
# 10) 월별 전체 판매수량 추이 (막대 그래프)
# ──────────────────────────────────────────────────────────
st.subheader("1) 월별 전체 판매수량 추이")
monthly_total = df[month_cols].sum()
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(monthly_total.index, monthly_total.values)
ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title("월별 전체 판매수량")
plt.xticks(rotation=45)

bar_offset = max(monthly_total.values) * 0.01
for x, y in zip(monthly_total.index, monthly_total.values):
    ax.text(x, y + bar_offset, f"{int(y):,}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
st.pyplot(fig)


# ──────────────────────────────────────────────────────────
# 11) 품목별 판매 추이 (라인 그래프)
# ──────────────────────────────────────────────────────────
st.subheader("2) 품목별 판매 추이")
item = st.selectbox("▶ 품목 선택", options=df["품명"].unique())
series = df[df["품명"] == item][month_cols].iloc[0]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(series.index, series.values, marker="o", linewidth=2)
ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title(f"{item} 판매 추이")
plt.xticks(rotation=45)

offset = max(series.values[~np.isnan(series.values)]) * 0.003
for x, y in zip(series.index, series.values):
    if not np.isnan(y):
        ax.text(x, y + offset, f"{int(y):,}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
st.pyplot(fig)


# ──────────────────────────────────────────────────────────
# 12) 상위 N개 품목 판매 추이 (라인 그래프)
# ──────────────────────────────────────────────────────────
st.subheader("3) 상위 N개 품목 판매 추이")
top_n = st.slider("▶ 상위 몇 개 품목?", 1, 10, 5)
last_month = month_cols[-1]
top_items = df.nlargest(top_n, columns=last_month)["품명"].tolist()
df_top = df[df["품명"].isin(top_items)].set_index("품명")[month_cols].T

fig, ax = plt.subplots(figsize=(16, 10))
for it in top_items:
    ax.plot(df_top.index, df_top[it], marker="o", linewidth=1, label=it)

ax.set_xlabel("월별")
ax.set_ylabel("판매수량")
ax.set_title(f"상위 {top_n}개 품목 판매 추이")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=6, fontsize=8)
plt.xticks(rotation=45)

y_offset_base = df_top.max().max() * 0.01
for it in top_items:
    for x, y in zip(df_top.index, df_top[it].values):
        if not np.isnan(y):
            ax.text(x, y + y_offset_base, f"{int(y):,}", ha="center", va="bottom", fontsize=8)

plt.tight_layout()
st.pyplot(fig)







