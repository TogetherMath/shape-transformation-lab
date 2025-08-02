import streamlit as st
from section1_transformation_by_matrix import run_transformation_by_matrix
from section2_symmetry_rotation import run_symmetry_rotation
from section3_complex_plane import run_complex_plane
from section4_rotation_translation import run_rotation_translation

# ✅ 페이지 설정
st.set_page_config(
    page_title="도형 변환 실험실",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 페이지 제목
st.title("🔄 도형 변환 실험실")

# ✅ 사이드바 메뉴
menu = st.sidebar.radio("📂 실험을 선택하세요", [
    "1. 행렬을 통한 일차변환",
    "2. 대칭과 회전변환",
    "3. 복소평면에서 이동",
    "4. 회전과 평행이동"
])

# ✅ 선택에 따라 해당 시뮬레이터 실행
if menu == "1. 행렬을 통한 일차변환":
    run_transformation_by_matrix()
elif menu == "2. 대칭과 회전변환":
    run_symmetry_rotation()
elif menu == "3. 복소평면에서 이동":
    run_complex_plane()
elif menu == "4. 회전과 평행이동":
    run_rotation_translation()
