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
st.caption("중학교 3학년용 · 통계 배우고 엑셀 함수로 다시 정리해보기")


# -------------------------------
# 유틸 함수들
# -------------------------------
def create_dataframe_from_text(raw_text: str) -> pd.DataFrame:
    """
    한 줄에 하나의 숫자가 적힌 텍스트(예: 점수 목록)를 DataFrame으로 바꿔주는 함수
    """
    if not raw_text:
        return pd.DataFrame(columns=["값"])

    lines = [line.strip() for line in raw_text.splitlines() if line.strip() != ""]
    numbers = []

    for line in lines:
        # 쉼표(,)가 들어간 숫자도 처리 (예: 1,234)
        clean = line.replace(",", "")
        try:
            value = float(clean)
            numbers.append(value)
        except ValueError:
            # 숫자로 바꿀 수 없는 값은 무시
            continue

    if len(numbers) == 0:
        return pd.DataFrame(columns=["값"])

    df = pd.DataFrame({"값": numbers})
    return df


def get_excel_range(col_letter: str, start_row: int, count: int) -> str:
    """
    엑셀 함수에 넣을 범위 문자열(예: B2:B33)을 만들어주는 함수
    """
    if count <= 0:
        return f"{col_letter}{start_row}:{col_letter}{start_row}"
    end_row = start_row + count - 1
    return f"{col_letter}{start_row}:{col_letter}{end_row}"


def calculate_stats(df: pd.DataFrame) -> dict:
    """
    기본 통계량 계산
    """
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
    desc["표준편차"] = float(s.std(ddof=1))  # 표본 표준편차 (STDEV.S에 대응)

    # 최빈값 (여러 개일 수 있음)
    try:
        value_counts = s.value_counts()
        max_count = value_counts.max()
        modes = list(value_counts[value_counts == max_count].index)
        desc["최빈값"] = modes
    except Exception:
        desc["최빈값"] = []

    return desc


# -------------------------------
# 사이드바
# -------------------------------
with st.sidebar:
    st.header("🧭 사용 방법")
    st.markdown(
        """
1. **데이터 만들기** 탭에서 점수나 키 같은 숫자 데이터를 입력해요.  
2. **통계 & 엑셀 함수** 탭에서 평균, 중앙값 등을 확인하고  
   엑셀에서 쓸 수 있는 **함수 수식**을 같이 봐요.  
3. **그래프 그리기** 탭에서는 막대그래프 등으로 데이터 모양을 살펴봐요.  

💡 *입력한 데이터는 모두 브라우저 안에서만 사용돼요.*
        """
    )


# -------------------------------
# 메인 레이아웃 - 탭 구성
# -------------------------------
tab_make, tab_stats, tab_chart, tab_quiz = st.tabs(
    ["1️⃣ 데이터 만들기", "2️⃣ 통계 & 엑셀 함수", "3️⃣ 그래프 그리기", "4️⃣ 미션 & 생각해보기"]
)

# 세션 상태에 데이터 저장하기
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=["값"])

# ---------------------------------
# 1️⃣ 데이터 만들기 탭
# ---------------------------------
with tab_make:
    st.subheader("1️⃣ 데이터 만들기 📝")

    st.markdown(
        """
- 한 줄에 **하나의 숫자**씩 입력해보세요.  
- 예시: 시험 점수, 키, 달리기 기록 시간 등  
- 나중에 이 데이터를 엑셀로 내려받아서 함수 연습에 쓸 거예요. 😊
        """
    )

    col_left, col_right = st.columns(2)

    with col_left:
        sample_btn = st.button("예시 데이터 불러오기 (시험 점수 20명) 🎁")

    default_text = ""
    if sample_btn:
        default_text = "\n".join(
            ["75", "88", "92", "61", "70", "84", "95", "100", "68", "73",
             "77", "82", "89", "90", "55", "60", "65", "78", "85", "91"]
        )

    raw_text = st.text_area(
        "📥 숫자 데이터 입력 (한 줄에 하나씩)",
        value=default_text,
        height=260,
        placeholder="예) \n78\n82\n90\n67\n...",
    )

    if st.button("데이터 불러오기 / 업데이트 🔄"):
        df = create_dataframe_from_text(raw_text)
        st.session_state["data_df"] = df

    with col_right:
        st.markdown("#### 🔍 현재 데이터 미리보기")
        if not st.session_state["data_df"].empty:
            st.dataframe(st.session_state["data_df"], use_container_width=True)
            st.success(f"데이터 개수: {len(st.session_state['data_df'])}개")
        else:
            st.info("아직 저장된 데이터가 없습니다. 왼쪽에 값을 입력하고 버튼을 눌러보세요.")

    st.markdown("---")
    st.markdown("#### 💾 엑셀에서 열 수 있는 파일로 저장하기 (CSV)")

    if not st.session_state["data_df"].empty:
        csv_data = st.session_state["data_df"].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 CSV 파일 다운로드 (엑셀로 열기 가능)",
            data=csv_data,
            file_name="통계연습_데이터.csv",
            mime="text/csv",
            help="다운로드 후 엑셀에서 파일을 열면 됩니다.",
        )
        st.caption("💡 CSV 파일은 엑셀에서 바로 열 수 있는 텍스트 형식의 표 파일이에요.")
    else:
        st.caption("데이터를 입력하면 다운로드 버튼이 활성화됩니다.")


# ---------------------------------
# 2️⃣ 통계 & 엑셀 함수 탭
# ---------------------------------
with tab_stats:
    st.subheader("2️⃣ 통계 요약 & 엑셀 함수 연습 🔢")

    df = st.session_state["data_df"]
    if df.empty:
        st.warning("먼저 1️⃣ 탭에서 데이터를 만들어 주세요!")
    else:
        st.markdown("#### ✅ 기본 통계량")
        stats = calculate_stats(df)

        if not stats:
            st.warning("계산할 수 있는 데이터가 없습니다. 숫자 데이터를 다시 확인해 주세요.")
        else:
            # 표 형태로 보여주기
            stats_table = pd.DataFrame(
                {
                    "통계량": [
                        "데이터 개수 (COUNT)",
                        "합계 (SUM)",
                        "평균 (AVERAGE)",
                        "중앙값 (MEDIAN)",
                        "최솟값 (MIN)",
                        "최댓값 (MAX)",
                        "표준편차 (STDEV.S)",
                        "최빈값 (MODE.SNGL)",
                    ],
                    "값": [
                        stats["개수"],
                        stats["합계"],
                        round(stats["평균"], 2),
                        round(stats["중앙값"], 2),
                        stats["최솟값"],
                        stats["최댓값"],
                        round(stats["표준편차"], 2),
                        ", ".join(map(str, stats["최빈값"])) if stats["최빈값"] else "없음",
                    ],
                }
            )

            st.dataframe(stats_table, use_container_width=True)

            st.markdown("---")
            st.markdown("#### 🧮 엑셀에서 이렇게 쓸 수 있어요!")

            st.markdown(
                """
아래는 엑셀에서 **같은 값을 구할 때 사용할 수 있는 함수 수식** 예시입니다.  
데이터가 `B2`부터 아래로 쭉 입력되어 있다고 가정해볼게요. (예: B2:B21)
                """
            )

            # 엑셀 범위 설정 (기본: B열, 2행부터)
            col_letter = st.text_input("엑셀에서 데이터가 있는 열 문자 입력 (예: B)", value="B")
            start_row = st.number_input("데이터가 시작되는 행 번호 (예: 2)", min_value=1, value=2, step=1)

            rng = get_excel_range(col_letter=col_letter.upper(), start_row=start_row, count=stats["개수"])

            formula_col1, formula_col2 = st.columns(2)

            with formula_col1:
                st.markdown("##### 📌 기본 함수")
                st.code(f"=COUNT({rng})   // 개수", language="text")
                st.code(f"=SUM({rng})     // 합계", language="text")
                st.code(f"=AVERAGE({rng}) // 평균", language="text")
                st.code(f"=MEDIAN({rng})  // 중앙값", language="text")

            with formula_col2:
                st.markdown("##### 📌 최솟값 / 최댓값 / 표준편차 / 최빈값")
                st.code(f"=MIN({rng})        // 최솟값", language="text")
                st.code(f"=MAX({rng})        // 최댓값", language="text")
                st.code(f"=STDEV.S({rng})    // 표본 표준편차", language="text")
                st.code(f"=MODE.SNGL({rng})  // 최빈값(1개)", language="text")

            st.info(
                "💡 실제 엑셀에서 데이터가 어느 열, 어느 행에 있는지에 따라 "
                "범위(B2:B21 부분)만 바꾸면 돼요!"
            )


# ---------------------------------
# 3️⃣ 그래프 그리기 탭
# ---------------------------------
with tab_chart:
    st.subheader("3️⃣ 데이터 모양 살펴보기 📊")

    df = st.session_state["data_df"]
    if df.empty:
        st.warning("먼저 1️⃣ 탭에서 데이터를 만들어 주세요!")
    else:
        st.markdown(
            """
데이터의 **분포**를 그래프로 보면 특징을 더 잘 알 수 있어요.  
예를 들어, 점수가 한쪽으로 몰려 있는지, 골고루 퍼져 있는지 등을 볼 수 있어요.
            """
        )

        chart_type = st.radio(
            "원하는 그래프 종류를 선택해보세요 👇",
            ["막대그래프 (값별 도수)", "꺾은선그래프 (값 순서대로)", "상자수염그림 느낌 보기(설명용)"],
        )

        if chart_type == "막대그래프 (값별 도수)":
            st.markdown("#### 🔢 값별 도수(빈도) 막대그래프")
            counts = df["값"].value_counts().sort_index()
            chart_df = counts.reset_index()
            chart_df.columns = ["값", "도수"]
            st.bar_chart(chart_df.set_index("값"))
            st.caption("같은 값이 몇 번 나왔는지 보여주는 그래프예요.")

        elif chart_type == "꺾은선그래프 (값 순서대로)":
            st.markdown("#### 📈 값이 입력된 순서대로 꺾은선그래프")
            st.line_chart(df["값"])
            st.caption("시험을 본 순서, 측정한 순서 등 **시간/순서에 따라 어떻게 변하는지** 볼 수 있어요.")

        else:
            st.markdown("#### 📦 상자수염그림(Boxplot) 개념 설명")
            st.markdown(
                """
Streamlit 기본 기능만 사용해서 **진짜 상자수염그림을 그리기는 조금 어려워요.  
하지만 개념은 이렇게 생각해볼 수 있어요.**

- 데이터를 작은 것부터 큰 것까지 **정렬**한다.
- 가운데 있는 값이 **중앙값**이다.
- 아래쪽 25% 지점, 위쪽 25% 지점을 찾으면 **사분위수(Q1, Q3)** 를 알 수 있다.
- 이 네 개의 값(최솟값, Q1, 중앙값, Q3, 최댓값)을 축 위에 표시하면  
  상자수염그림의 의미를 이해하는 데 도움이 돼요. 😊
                """
            )
            st.markdown("#### 🔍 정렬된 데이터 미리보기")
            st.dataframe(df.sort_values("값").reset_index(drop=True), use_container_width=True)


# ---------------------------------
# 4️⃣ 미션 & 생각해보기 탭
# ---------------------------------
with tab_quiz:
    st.subheader("4️⃣ 미션 & 생각해보기 🎯")

    st.markdown(
        """
아래 미션 중 마음에 드는 것을 골라서 **엑셀 + 이 웹앱**을 함께 활용해보세요.

---

### 🧩 미션 1. 우리 반 모의고사 점수 분석하기
1. 각자 또는 모둠별로 모의고사 점수를 모은다.  
2. 이 웹앱 1️⃣ 탭에 점수를 입력하고 통계를 구한다.  
3. 엑셀에 데이터를 붙여넣고,  
   - `=AVERAGE(...)`  
   - `=MEDIAN(...)`  
   - `=STDEV.S(...)`  
   - `=MODE.SNGL(...)`  
   을 직접 사용해 본다.  
4. 웹앱 결과와 엑셀 결과가 같은지 비교해 본다.

---

### 📊 미션 2. 나의 생활 데이터 분석하기
예시:
- 하루 걸음 수
- 하루 공부 시간
- 일주일 동안 잠잔 시간

1. 7일 또는 14일 정도의 데이터를 모은다.  
2. 이 웹앱에 넣어 평균, 중앙값, 최솟값, 최댓값을 구한다.  
3. 엑셀로 옮겨 그래프(세로 막대그래프, 꺾은선그래프)를 직접 만들어 본다.  
4. **“내 생활 패턴”** 을 한 문장으로 정리해 본다.

---

### 💭 생각해보기 질문
- 평균과 중앙값이 **많이 차이** 나는 경우는 어떤 상황일까?  
- 최빈값이 의미 있는 경우(예: 신발 사이즈, 옷 사이즈)는 어떤 데이터일까?  
- 같은 데이터를 평균으로 설명할 때와 중앙값으로 설명할 때,  
  **느낌이 달라지는 사례**를 찾아볼 수 있을까?

---
선생님이 원하는 미션을 골라 수행한 뒤,  
**엑셀 파일 + 한 줄 소감**을 함께 제출해도 좋아요. 😄
        """
    )
