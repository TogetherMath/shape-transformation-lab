import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import plotly.graph_objects as go


def run_rotation_translation():
    st.header("🟥 (4) 회전과 평행이동 조합 시뮬레이터")
    st.write("이곳에 (4)번 시뮬레이터 내용을 구현할 예정입니다.")





# ✅ 페이지 설정
#st.set_page_config(page_title="도형 변환 실험실", layout="wide")
#st.title("🔄 도형 변환 실험실")

# ✅ 한글 폰트 설정
font_path = './fonts/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
font_prop = None
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

# ✅ 숫자 포맷 함수
def format_number(n):
    return f"{n:.1f}".rstrip('0').rstrip('.') if n % 1 != 0 else str(int(n))


