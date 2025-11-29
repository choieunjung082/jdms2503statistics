import streamlit as st
import pandas as pd

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(
    page_title="통계 x 엑셀 연습실",
    page_icon="📊",
    layout="wide"
)

st.title("📊 통계 x 엑셀 함수 연습실")
st.caption("중학교 3학년용 · 통계 배우고 엑셀 함수로 계산해보기 · by 최은정 선생님")

# -------------------------------
# 유틸 함수들
# -------------------------------
def create_dataframe_from_text(raw_text: str) -> pd.DataFrame:
    if not raw_text:
        return pd.DataFrame(columns=["값"])

    lines = [line.strip() for line in raw_text.splitlines() if line.strip() != ""]
    numbers = []

    for line in lines:
        clean = line.replace(",", "")
        try:
            value = float(clean)
            numbers.append(value)
        except ValueError:
            continue

    if len(numbers) == 0:
        return pd.DataFrame(columns=["값"])

    return pd.DataFrame({"값": numbers})


def get_excel_range(col_letter: str, start_row: int, count: int) -> str:
    if count <= 0:
        return f"{col_letter}{start_row}:{col_letter}{start_row}"
    end_row = start_row + count - 1
    return f"{col_letter}{start_row}:{col_letter}{end_row}"


def calculate_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    s = df["값"].dropna()
    if s.empty:
        return {}

    desc = {}
    desc["개수"] = int(s.count())
    desc["합계"] = float(s.sum())
    desc["평균"] = float(s.mean())
    desc["중앙값"] = float(s.median())
    desc["최솟값"] = float(s.min())
    desc["최댓값"] = float(s.max())
    desc["표준편차"] = float(s.std(ddof=1))

    try:
        value_counts = s.value_counts()
        max_count = value_counts.max()
        modes = list(value_counts[value_counts == max_count].index)
        desc["최빈값"] = modes
    except Exception:
        desc["최빈값"] = []

    return desc


# -------------------------------
# 사이드바 안내
# -------------------------------
with st.sidebar:
    st.header("🧭 사용 안내")
    st.markdown(
        """
### ✔ 수업 흐름
1. **데이터 입력하기**
2. **통계량 직접 계산**
3. **엑셀 함수와 비교**
4. **그래프로 데이터 분석**
5. **엑셀 함수 요약표로 복습**

### ✔ 수업 목표
- 통계 개념(평균·분산·표준편차) 이해하기  
- 엑셀 함수로 실제 계산하는 방법 익히기  
- 데이터 분석의 기본 구조 체험하기  
        """
    )

# 세션 데이터 저장
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=["값"])

# -------------------------------
# 탭 구성
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "1️⃣ 데이터 만들기",
        "2️⃣ 통계 & 엑셀 함수",
        "3️⃣ 그래프 그리기",
        "4️⃣ 미션 & 생각해보기",
        "5️⃣ 엑셀 함수 요약 & 개념 정리 📘"
    ]
)

# -------------------------------
# 1️⃣ 데이터 만들기 탭
# -------------------------------
with tab1:
    st.subheader("1️⃣ 데이터 만들기 📝")

    col1, col2 = st.columns(2)

    with col1:
        sample_btn = st.button("예시 데이터 20개 불러오기 🎁")

    default_text = ""
    if sample_btn:
        default_text = "\n".join(
            ["75", "88", "92", "61", "70", "84", "95", "100", "68", "73",
             "77", "82", "89", "90", "55", "60", "65", "78", "85", "91"]
        )

    raw_text = st.text_area(
        "📥 숫자 데이터 입력 (한 줄에 하나씩 입력하세요)",
        value=default_text,
        height=250
    )

    if st.button("데이터 불러오기 / 업데이트 🔄"):
        st.session_state["data_df"] = create_dataframe_from_text(raw_text)

    with col2:
        st.markdown("#### 🔍 현재 데이터")
        if not st.session_state["data_df"].empty:
            st.dataframe(st.session_state["data_df"])
        else:
            st.info("데이터가 없습니다.")

    st.markdown("---")
    if not st.session_state["data_df"].empty:
        csv_data = st.session_state["data_df"].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 CSV 파일 다운로드",
            data=csv_data,
            file_name="통계데이터.csv",
            mime="text/csv",
        )


# -------------------------------
# 2️⃣ 통계 & 엑셀 함수 탭
# -------------------------------
with tab2:
    st.subheader("2️⃣ 계산된 통계값 + 엑셀 함수 비교 🔢")

    df = st.session_state["data_df"]
    if df.empty:
        st.warning("먼저 데이터를 입력해 주세요!")
    else:
        stats = calculate_stats(df)

        table = pd.DataFrame(
            {
                "통계량": [
                    "데이터 개수",
                    "합계",
                    "평균",
                    "중앙값",
                    "최솟값",
                    "최댓값",
                    "표준편차(STDEV.S)",
                    "최빈값",
                ],
                "값": [
                    stats["개수"],
                    stats["합계"],
                    round(stats["평균"], 2),
                    stats["중앙값"],
                    stats["최솟값"],
                    stats["최댓값"],
                    round(stats["표준편차"], 2),
                    ", ".join(map(str, stats["최빈값"])),
                ],
            }
        )

        st.dataframe(table, use_container_width=True)

        st.markdown("### 🧮 엑셀에서 동일 계산을 할 때 사용하는 함수")

        colA, colB = st.columns(2)

        colA.markdown("#### ✔ 기본 함수")
        colA.code("=SUM(범위)")
        colA.code("=AVERAGE(범위)")
        colA.code("=MEDIAN(범위)")
        colA.code("=MIN(범위)")
        colA.code("=MAX(범위)")

        colB.markdown("#### ✔ 분산 / 표준편차")
        colB.code("=VAR.P(범위)   // 모집단 분산")
        colB.code("=VAR.S(범위)   // 표본 분산")
        colB.code("=STDEV.P(범위) // 모집단 표준편차")
        colB.code("=STDEV.S(범위) // 표본 표준편차")


# -------------------------------
# 3️⃣ 그래프 그리기 탭
# -------------------------------
with tab3:
    st.subheader("3️⃣ 그래프로 데이터 보기 📊")

    df = st.session_state["data_df"]

    if df.empty:
        st.warning("데이터가 없습니다. 1️⃣ 탭에서 입력하세요.")
    else:
        chart_type = st.radio(
            "📌 그래프 선택",
            ["막대그래프(도수분포)", "꺾은선그래프", "정렬된 데이터 보기"]
        )

        if chart_type == "막대그래프(도수분포)":
            counts = df["값"].value_counts().sort_index()
            st.bar_chart(counts)

        elif chart_type == "꺾은선그래프":
            st.line_chart(df["값"])

        else:
            st.dataframe(df.sort_values("값").reset_index(drop=True))


# -------------------------------
# 4️⃣ 미션 & 생각해보기
# -------------------------------
with tab4:
    st.subheader("4️⃣ 미션 & 생각해보기 🎯")

    st.markdown(
        """
### 🧩 미션 1. 우리 반 데이터 분석하기
1. 점수 등 데이터를 모아 1️⃣ 탭에 입력  
2. 2️⃣에서 통계와 엑셀 함수 비교  
3. 3️⃣에서 그래프로 특징 분석하기  
4. “내 데이터의 특징 한 줄 요약” 작성하기  

---

### 💭 생각해보기 질문
- 평균과 중앙값이 크게 다를 때는 어떤 경우일까?  
- 왜 표본 분산 / 모집단 분산이 나뉠까?  
- 표준편차가 작다는 것은 어떤 의미일까?  

---
        """
    )


# -------------------------------
# 5️⃣ 엑셀 함수 요약 & 개념 정리 (요청하신 새 페이지)
# -------------------------------
with tab5:
    st.subheader("5️⃣ 엑셀 함수 요약 & 개념 정리 📘")

    st.markdown(
        """
### 📌 <엑셀 함수 도구 설명>

---

#### 🟦 **합계**
