import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("📊 지역별 인구 분석 대시보드")

# 데이터 업로드
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.replace("-", 0, inplace=True)
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

uploaded_file = st.file_uploader("📎 CSV 파일을 업로드하세요", type="csv")
if uploaded_file:
    df = load_data(uploaded_file)
    
    # 컬럼명 확인용 출력
    st.write("🔍 데이터 컬럼명:", df.columns.tolist())
    
    st.subheader("🔍 데이터 미리보기")
    st.dataframe(df.head())

    # '연령대' 컬럼 있는지 확인
    if "연령대" not in df.columns or "지역" not in df.columns:
        st.error("CSV 파일에 '연령대' 또는 '지역' 컬럼이 없습니다. 파일을 확인해주세요.")
    else:
        tabs = st.tabs(["연도별 추이", "지역별 분석", "변화량 분석", "누적 시각화"])

        # 연도별 추이
        with tabs[0]:
            st.header("📆 연도별 인구 추이")
            region = st.selectbox("지역 선택", df["지역"].unique())
            age = st.selectbox("연령대 선택", df["연령대"].unique())
            filtered_rows = df[(df["지역"] == region) & (df["연령대"] == age)]
            if not filtered_rows.empty:
                row = filtered_rows.iloc[0]
                years = df.columns[2:]
                values = row[2:].values

                fig, ax = plt.subplots()
                ax.plot(years, values, marker='o')
                ax.set_title(f"{region} - {age} 인구 추이")
                ax.set_ylabel("인구 수")
                ax.set_xlabel("연도")
                st.pyplot(fig=fig)
            else:
                st.warning("선택한 조건에 맞는 데이터가 없습니다.")

        # 지역별 분석
        with tabs[1]:
            st.header("📍 지역별 인구 비교")
            year = st.selectbox("연도 선택", df.columns[2:], key="연도선택")
            age_group = st.selectbox("연령대 선택", df["연령대"].unique(), key="연령선택")
            filtered = df[df["연령대"] == age_group][["지역", year]]
            sorted_df = filtered.sort_values(by=year, ascending=False)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=sorted_df, x=year, y="지역", ax=ax)
            st.pyplot(fig=fig)

        # 변화량 분석
        with tabs[2]:
            st.header("📊 2015 → 2022 변화량")
            if "변화량" not in df.columns:
                df["변화량"] = df["2022"] - df["2015"]
            change_df = df[df["연령대"] == "전체"][["지역", "변화량"]].sort_values(by="변화량", ascending=False)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=change_df, x="변화량", y="지역", ax=ax)
            st.pyplot(fig=fig)

        # 누적 시각화
        with tabs[3]:
            st.header("🎨 연령대별 누적 막대그래프")
            year = st.selectbox("연도 선택", df.columns[2:], key="누적연도")
            pivot = df.pivot(index="지역", columns="연령대", values=year).fillna(0)

            fig, ax = plt.subplots(figsize=(12, 6))
            pivot.plot(kind="bar", stacked=True, ax=ax)
            st.pyplot(fig=fig)
