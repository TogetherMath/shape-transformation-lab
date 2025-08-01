import streamlit as st

# 웹앱 제목
st.set_page_config(page_title="도형 변환 실험실", layout="wide")
st.title("🔄 도형 변환 실험실")

# 사이드바 메뉴
menu = st.sidebar.radio(
    "📂 메뉴를 선택하세요",
    ["행렬을 통한 일차변환", "두 번의 대칭이동", "복소평면에서의 변환", "복소평면에서 평행이동과 회전이동의 결합"]
)

# 메뉴에 따라 다른 내용 표시
if menu == "행렬을 통한 일차변환":
    st.subheader("🏠 행렬을 통한 일차변환")
    st.write("여러 도형을 여러 행렬로 일차변환을 실행해 보세요.")

elif menu == "두 번의 대칭이동":
    st.subheader("🔺 두 번의 대칭이동")
    st.write("두 번의 대칭이동은 반드시 회전이동이 될까요?")

elif menu == "복소평면에서의 변환":
    st.subheader("⬛ 복소평면에서의 변환")
    st.write("복소평면에서 여러 도형을 여러 변환 공식으로 변환시켜 보세요.")

elif menu == "복소평면에서 평행이동과 회전이동의 결합":
    st.subheader("📏 복소평면에서 평행이동과 회전이동의 결합")
    st.write("복소평면에서 회전이동 사이에 평행이동이 들어가도 회전이동이 될까요?")
