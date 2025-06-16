import streamlit as st
import pyrebase
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# ---------------------
# Firebase 설정
# ---------------------
firebase_config = {
    "apiKey": "AIzaSyCswFmrOGU3FyLYxwbNPTp7hvQxLfTPIZw",
    "authDomain": "sw-projects-49798.firebaseapp.com",
    "databaseURL": "https://sw-projects-49798-default-rtdb.firebaseio.com",
    "projectId": "sw-projects-49798",
    "storageBucket": "sw-projects-49798.appspot.com",
    "messagingSenderId": "812186368395",
    "appId": "1:812186368395:web:be2f7291ce54396209d78e"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# ---------------------
# 세션 상태 초기화
# ---------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.id_token = ""

# ---------------------
# 로그인 함수
# ---------------------
def login_page():
    st.header("🔐 로그인")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.id_token = user['idToken']
            st.success("로그인 성공!")
            st.experimental_rerun()
        except:
            st.error("로그인 실패. 이메일과 비밀번호를 확인하세요.")

# ---------------------
# 로그아웃 함수
# ---------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.id_token = ""
    st.success("로그아웃 되었습니다.")
    time.sleep(1)
    st.experimental_rerun()

# ---------------------
# EDA 기능 함수
# ---------------------
def eda_page():
    st.title("📊 Bike Sharing Demand EDA")
    uploaded = st.file_uploader("train.csv 파일 업로드", type="csv")
    if uploaded is None:
        st.info("CSV 파일을 업로드하세요.")
        return

    df = pd.read_csv(uploaded, parse_dates=['datetime'])
    st.subheader("기초 정보")
    st.write(df.head())

    st.subheader("시간대별 평균 대여량")
    df['hour'] = df['datetime'].dt.hour
    fig, ax = plt.subplots()
    sns.pointplot(x='hour', y='count', data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("상관관계 분석")
    corr = df[['temp', 'atemp', 'humidity', 'windspeed', 'count']].corr()
    fig2, ax2 = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
    st.pyplot(fig2)

# ---------------------
# 메인 앱 실행
# ---------------------
st.title("🚲 자전거 대여 분석 웹앱")

if st.session_state.logged_in:
    st.sidebar.write(f"**로그인됨:** {st.session_state.user_email}")
    if st.sidebar.button("로그아웃"):
        logout()
    page = st.sidebar.radio("페이지 선택", ["EDA 분석"])
    if page == "EDA 분석":
        eda_page()
else:
    login_page()
