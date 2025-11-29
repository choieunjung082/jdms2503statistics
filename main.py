import streamlit as st
import pandas as pd
import statistics as stats

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
# 예시 데이터 (33명 수학 점수)
# -------------------------------
DEFAULT_DATA = [
    {"번호": 1, "수학": 95},
    {"번호": 2, "수학": 37},
    {"번호": 3, "수학": 92},
    {"번호": 4, "수학": 62},
    {"번호": 5, "수학": 87},
    {"번호": 6, "수학": 43},
    {"번호": 7, "수학": 94},
    {"번호": 8, "수학": 79},
    {"번호": 9, "수학": 81},
    {"번호": 10, "수학": 71},
    {"번호": 11, "수학": 91},
    {"번호": 12, "수학": 91},
    {"번호": 13, "수학": 97},
    {"번호": 14, "수학": 61},
    {"번호": 15, "수학": 96},
    {"번호": 16, "수학": 37},
    {"번호": 17, "수학": 93},
    {"번호": 18, "수학": 84},
    {"번호": 19, "수학": 87},
    {"번호": 20, "수학": 87},
    {"번호": 21, "수학": 78},
    {"번호": 22, "수학": 94},
    {"번호": 23, "수학": 87},
    {"번호": 24, "수학": 68},
    {"번호": 25, "수학": 85},
    {"번호": 26, "수학": 80},
    {"번호": 27, "수학": 7},
    {"번호": 28, "수학": 75},
    {"번호": 29, "수학": 82},
    {"번호": 30, "수학": 97},
    {"번호": 31, "수학": 90},
    {"번호": 32, "수학": 93},
    {"번호": 33, "수학": 96},
]

DEFAULT_DF = pd.DataFrame(DEFAULT_DATA)


# -------------------------------
# 유틸: 텍스트 → DataFrame
# -------------------------------
def text_to_df(raw_text: str) -> pd.DataFrame:
    """
    한 줄에 하나의 숫자를 입력한 텍스트를 DataFrame으로 변환
    (예: 구글폼 점수 복붙)
    """
    if not raw_text.strip():
        return DEFAULT_DF.copy()

    lines = [line.strip() for line in raw_text.splitlines() if line.strip() != ""]
    numbers = []

    for line in lines:
        clean = line.replace(",", "")
        try:
            value = float(clean)
            numbers.append(value)
        except ValueError:
            # 숫자로 인식 안 되는 줄은 무시
            continue

    if len(numbers) == 0:
        return DEFAULT_DF.copy()

    df = pd.DataFrame(
        {"번호": range(1, len(numbers) + 1), "수학": numbers}
    )
    return df


# -------------------------------
# 사이드바: 사용 방법 안내
# -------------------------------
with st.sidebar:
    st.header("🧭 사용 방법")
    st.markdown(
        """
1. **예시 점수**를 먼저 보고 통계값을 확인해 보세요.  
2. 아래 텍스트 박스에 **직접 점수 목록을 붙여넣기** 하면  
   통계값이 자동으로 다시 계산됩니다.  
3. 우측 카드에서 **엑셀 함수** 예시를 보고  
   집이나 학교에서 엑셀로 똑같이 연습해 보세요. ✏️
        """
    )
    st.markdown("---")
    st.markdown("교사용 팁: 이 페이지 링크를 학생들에게 공유하면, 학생 개별 점수로 통계·엑셀 활동이 가능합니다.")


# -------------------------------
# 1. 데이터 입력 영역
# -------------------------------
st.subheader("1️⃣ 점수 데이터 입력하기")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("#### ✍️ 점수 붙여넣기 (선택)")
    st.write("한 줄에 **한 명의 점수**만 입력하세요. (예: 구글폼 응답을 복사해서 붙여넣기)")
    example_text = "\n".join(str(row["수학"]) for row in DEFAULT_DATA)
    user_text = st.text_area(
        "여기에 점수 목록을 입력하세요. 비워두면 기본 예시 데이터가 사용됩니다.",
        value="",
        height=200,
        placeholder=example_text,
    )

with col_right:
    st.markdown("#### 📋 현재 사용 중인 데이터")
    df = text_to_df(user_text)
    st.dataframe(df, use_container_width=True)

    st.info(f"현재 **{len(df)}명**의 수학 점수가 있습니다.")


# -------------------------------
# 2. 통계량 계산하기
# -------------------------------
st.subheader("2️⃣ 대표값 · 산포도 살펴보기")

scores = df["수학"].astype(float)
n = len(scores)
mean = scores.mean()
median = scores.median()
mode_list = scores.mode().tolist()
score_min = scores.min()
score_max = scores.max()
score_range = score_max - score_min
q1 = scores.quantile(0.25)
q3 = scores.quantile(0.75)
var = scores.var(ddof=1) if n > 1 else 0
std = scores.std(ddof=1) if n > 1 else 0

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("##### ⭐ 대표값")
    st.metric("평균 (Mean)", f"{mean:.2f}")
    st.metric("중앙값 (Median)", f"{median:.2f}")
    if len(mode_list) == 1:
        st.metric("최빈값 (Mode)", f"{mode_list[0]:.0f}")
    else:
        st.metric("최빈값 (Mode)", ", ".join(map(lambda x: str(int(x)), mode_list)))

with c2:
    st.markdown("##### 📏 범위 & 사분위수")
    st.metric("최댓값", f"{score_max:.0f}")
    st.metric("최솟값", f"{score_min:.0f}")
    st.metric("범위 (Range)", f"{score_range:.0f}")
    st.caption(f"1사분위수(Q1): {q1:.2f} / 3사분위수(Q3): {q3:.2f}")

with c3:
    st.markdown("##### 🎯 분산 · 표준편차")
    st.metric("분산 (Variance)", f"{var:.2f}")
    st.metric("표준편차 (Std Dev)", f"{std:.2f}")
    st.caption("점수들이 평균에서 얼마나 퍼져 있는지 보여주는 값이에요.")


# -------------------------------
# 3. 분포 시각화 (간단 히스토그램)
# -------------------------------
st.subheader("3️⃣ 점수 분포 살펴보기 (막대그래프)")

# 점수를 구간별로 나누기 (예: 0~9, 10~19, ..., 90~100)
bins = list(range(0, 101, 10))
labels = [f"{b}~{b+9}" for b in bins[:-1]]
categories = pd.cut(scores, bins=bins, labels=labels, include_lowest=True, right=True)
freq_table = categories.value_counts().sort_index()
freq_df = pd.DataFrame({"구간": freq_table.index.astype(str), "학생 수": freq_table.values}).set_index("구간")

st.bar_chart(freq_df)

st.caption("👉 어떤 점수대에 학생들이 많이 모여 있는지 한눈에 보이나요?")


# -------------------------------
# 4. 엑셀 함수로 똑같이 해보기 👩‍💻👨‍💻
# -------------------------------
st.subheader("4️⃣ 엑셀에서 똑같이 계산해 보기")

st.markdown(
    """
예를 들어, 엑셀의 **A열에는 번호**, **B열에는 수학 점수**가 있다고 해볼게요.  
(즉, `A2:A34`, `B2:B34`에 데이터가 있다고 가정합니다.)

아래 표의 수식을 엑셀 셀에 직접 입력해 보세요. 💡
"""
)

excel_table = pd.DataFrame(
    {
        "개념": [
            "평균",
            "중앙값",
            "최빈값",
            "최댓값",
            "최솟값",
            "범위",
            "분산",
            "표준편차",
            "80점 이상 인원 수",
        ],
        "엑셀 함수": [
            "AVERAGE",
            "MEDIAN",
            "MODE.SNGL",
            "MAX",
            "MIN",
            "MAX - MIN",
            "VAR.S",
            "STDEV.S",
            "COUNTIF",
        ],
        "예시 수식": [
            "=AVERAGE(B2:B34)",
            "=MEDIAN(B2:B34)",
            "=MODE.SNGL(B2:B34)",
            "=MAX(B2:B34)",
            "=MIN(B2:B34)",
            "=MAX(B2:B34)-MIN(B2:B34)",
            "=VAR.S(B2:B34)",
            "=STDEV.S(B2:B34)",
            '=COUNTIF(B2:B34,">=80")',
        ],
        "설명": [
            "전체 점수의 평균(산술평균)을 구함",
            "작은 순서로 정렬했을 때 가운데 값",
            "가장 많이 나온 점수",
            "가장 큰 점수",
            "가장 작은 점수",
            "최댓값 - 최솟값",
            "표본 분산 (n-1로 나눔)",
            "표본 표준편차",
            "80점 이상인 학생 수를 셈",
        ],
    }
)

st.dataframe(excel_table, use_container_width=True)


# -------------------------------
# 5. 엑셀 함수 미니 퀴즈 🎮
# -------------------------------
st.subheader("5️⃣ 엑셀 함수 미니 퀴즈 🎮")

st.markdown(
    """
엑셀 시트에  
- **A열** : 번호  
- **B열** : 수학 점수  
- **C열** : 편차  
- **D열** : 편차의 제곱  
- **E열** : 등수  

가 입력되어 있다고 가정해 볼게요. (데이터 범위는 `2행 ~ 34행`)

오른쪽 문제 칸(노란 셀)에 들어갈 **엑셀 함수 이름** 또는 **대표 수식**을 적어 보세요.  
"""
)

# Q1 전체 평균
st.markdown("### Q1. 전체 평균은?")
st.write("👉 ‘수학’ 점수의 전체 평균을 구할 때, 어떤 **함수 이름**을 써야 할까요?")
q1 = st.text_input("예: AVERAGE, MEDIAN, ...", key="q1")
if q1:
    if q1.strip().upper() == "AVERAGE":
        st.success("정답! 전체 평균은 **AVERAGE** 함수로 구합니다. 예: `=AVERAGE(B2:B34)` ✅")
    else:
        st.error("조금 아쉬워요 😢 전체 평균은 **AVERAGE** 함수로 구합니다. (예: `=AVERAGE(B2:B34)`)")

st.markdown("---")

# Q2 중간값
st.markdown("### Q2. 중간값은?")
st.write("👉 점수를 작은 순서대로 정렬했을 때 ‘가운데 값’을 구하는 **함수 이름**은 무엇일까요?")
q2 = st.text_input("예: MEDIAN, MODE.SNGL, ...", key="q2")
if q2:
    if q2.strip().upper() == "MEDIAN":
        st.success("정답! 중간값은 **MEDIAN** 함수로 구합니다. 예: `=MEDIAN(B2:B34)` ✅")
    else:
        st.error("중간값은 **MEDIAN** 함수로 구해요. 다시 한 번 떠올려 볼까요?")

st.markdown("---")

# Q3 등수 – RANK
st.markdown("### Q3. 등수는 RANK 함수로 확인하기")
st.write(
    """
👉 각 학생의 **등수**를 구하려면 어떤 함수가 필요할까요?  
샘플에서 14등이 4명이라면, **RANK 함수가 동점자에게 같은 등수를 주는 방식**이라는 것도 함께 떠올려 보세요.
"""
)
q3 = st.text_input("예: RANK, RANK.EQ, RANK.AVG 중에서 선택", key="q3")
if q3:
    if q3.strip().upper() in ["RANK", "RANK.EQ"]:
        st.success("좋아요! 등수는 보통 **RANK** 또는 **RANK.EQ** 함수로 구합니다. 🎯")
        st.info("예: `=RANK.EQ(B2,$B$2:$B$34,0)`  (0은 높은 점수가 1등이 되도록 내림차순 정렬)")
    else:
        st.error("등수를 구할 때는 **RANK** (또는 **RANK.EQ**) 함수를 사용합니다.")

st.markdown("---")

# Q4 최빈값
st.markdown("### Q4. 최빈값은?")
st.write("👉 가장 **많이 나온 점수(최빈값)** 를 구하는 함수 이름은 무엇일까요?")
q4 = st.text_input("예: MODE.SNGL, AVERAGE, ...", key="q4")
if q4:
    if q4.strip().upper() in ["MODE.SNGL", "MODE"]:
        st.success("정답! 최빈값은 **MODE.SNGL** (또는 예전 버전의 MODE) 함수로 구합니다. ✅")
        st.info("예: `=MODE.SNGL(B2:B34)`")
    else:
        st.error("최빈값은 **MODE.SNGL** 함수를 사용해요. (예: `=MODE.SNGL(B2:B34)`)")

st.markdown("---")

# Q5 COUNTIF로 특정 점수 개수 세기
st.markdown("### Q5. COUNTIF로 특정 점수 개수 확인하기")
st.write(
    """
👉 예를 들어 **87점인 학생 수**가 몇 명인지 알고 싶다면,  
어떤 **함수 이름**과 **조건식**을 사용해야 할까요?
"""
)
q5_func = st.text_input("사용할 함수 이름은? (예: COUNTIF)", key="q5_func")
q5_formula = st.text_input("예시 수식을 한 번 써 볼까요? (예: =COUNTIF(B2:B34,87))", key="q5_formula")

if q5_func:
    if q5_func.strip().upper() == "COUNTIF":
        st.success("함수 이름은 **COUNTIF**가 맞습니다! 👍")
    else:
        st.error("조건을 만족하는 개수를 셀 때는 **COUNTIF** 함수를 씁니다.")

if q5_formula:
    expected = "=COUNTIF(B2:B34,87)"
    if q5_formula.replace(" ", "").upper() == expected.upper():
        st.success("수식까지 완벽해요! `=COUNTIF(B2:B34,87)` 🎉")
    else:
        st.info("대표 예시는 `=COUNTIF(B2:B34,87)` 처럼 쓸 수 있어요.")

st.markdown("---")

# Q6 A 성적 / 59점 이하 인원수
st.markdown("### Q6. A 성적(90점 이상)과 59점 이하 인원 수")
st.write(
    """
👉 **90점 이상(A 성적)** 학생 수와,  
👉 **59점 이하** 학생 수를 세려면 어떤 함수를 쓸까요?  
조건이 있으니 어떤 함수일지 떠올려 보세요.
"""
)
q6_func = st.text_input("이때 사용할 함수 이름은? (예: COUNT, COUNTIF, ...)", key="q6_func")
if q6_func:
    if q6_func.strip().upper() == "COUNTIF":
        st.success("맞아요! 둘 다 **COUNTIF** 함수로 조건을 바꿔가며 셀 수 있어요. ✅")
        st.info(
            """
예시 수식  
- 90점 이상 인원 수: `=COUNTIF(B2:B34,">=90")`  
- 59점 이하 인원 수: `=COUNTIF(B2:B34,"<=59")`
            """
        )
    else:
        st.error("조건이 있을 때는 **COUNTIF** 함수를 사용합니다!")

st.markdown("---")

# Q7 분산
st.markdown("### Q7. 분산 구하기")
st.write(
    """
👉 각각의 점수가 평균에서 얼마나 퍼져 있는지 나타내는 **분산**을  
엑셀에서 구할 때는 어떤 함수 이름을 사용할까요?
(표본 분산 기준, `n-1`로 나누는 방식)
"""
)
q7 = st.text_input("예: VAR.S, STDEV.S, ...", key="q7")
if q7:
    if q7.strip().upper() in ["VAR.S", "VAR"]:
        st.success("정답! 분산은 보통 **VAR.S** 함수를 사용합니다. 예: `=VAR.S(B2:B34)` 📊")
    else:
        st.error("분산을 구할 때는 **VAR.S** 함수를 주로 사용합니다. (예: `=VAR.S(B2:B34)`)")

st.markdown("---")
st.caption("위 문제들을 실제 엑셀 시트에서 직접 함수로 계산해 보며 손에 익혀 봅시다! 💻✨")

# -------------------------------
# 푸터
# -------------------------------
st.markdown("---")
st.caption("© 통계 x 엑셀 연습실 · 중학교 3학년 수학 수업용 실습용 예시 앱")
