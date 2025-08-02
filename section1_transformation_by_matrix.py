import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import plotly.graph_objects as go


def run_transformation_by_matrix():
    st.header("🟩 (1) 행렬을 통한 일차변환 시뮬레이터")
    st.markdown("여러 도형을 여러 행렬로 일차변환하는 실험을 해 보세요.")



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

    # ✅ Plotly 버전 시각화 함수
    def plot_shape(shape_type, shape, transformed, matrix, font_family, a=1, b=1, c=0):
        fig = go.Figure()

        # 원래 도형
        fig.add_trace(go.Scatter(
            x=shape[:, 0], y=shape[:, 1],
            mode='lines+markers',
            name='변환전 도형',
            line=dict(color='blue'),
            marker=dict(color='blue')
        ))

        # 변환된 도형
        fig.add_trace(go.Scatter(
            x=transformed[:, 0], y=transformed[:, 1],
            mode='lines+markers',
            name='변환후 도형',
            line=dict(color='red', dash='dash'),
            marker=dict(color='red')
        ))

        # 직선일 경우 변환된 점 하나 강조
        if shape_type == "직선":
            if b != 0:
                base_point = np.array([0, c / b])
            else:
                base_point = np.array([c / a, 0])
            new_point = np.dot(base_point, matrix.T)
            fig.add_trace(go.Scatter(
                x=[new_point[0]], y=[new_point[1]],
                mode='markers',
                name='변환된 점',
                marker=dict(color='red', size=10, symbol='circle')
            ))

        # 축 범위 조절
        all_x = np.concatenate([shape[:, 0], transformed[:, 0]])
        all_y = np.concatenate([shape[:, 1], transformed[:, 1]])
        if shape_type == "직선":
            all_x = np.append(all_x, new_point[0])
            all_y = np.append(all_y, new_point[1])
        x_center = np.mean(all_x)
        y_center = np.mean(all_y)
        x_range = np.ptp(all_x)
        y_range = np.ptp(all_y)
        half_range = max(x_range, y_range) * 0.75
        half_range = min(half_range, 20)  # 최대 20으로 제한
        if half_range < 1:
            half_range = 2
        fig.update_layout(
            width=600,
            height=600,
            xaxis=dict(
                range=[x_center - half_range, x_center + half_range],
                zeroline=True,
                zerolinecolor='gray',
                showgrid=True,  # ✅ 보조선 추가
                gridcolor='lightgray',  # ✅ 선 색상 설정 (선택)
            ),
            yaxis=dict(
                range=[y_center - half_range, y_center + half_range],
                zeroline=True,
                zerolinecolor='gray',
                scaleanchor='x'   # ✅ 이 위치가 맞습니다!
            ),
            font=dict(family=font_family),
            legend=dict(x=0.01, y=0.99),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        return fig



    ##################### (1) ########################
    # ✅ 메뉴별 콘텐츠


    col1, spacer, col2 = st.columns([1.4, 0.3, 2])  # 좌:입력 / 우:출력

    with col1:
        st.subheader("# 도형 입력 ___________________")
        shape_type = st.selectbox("도형 종류를 선택하세요", ["삼각형", "사각형", "원", "직선"])

        if shape_type == "삼각형":
            A = np.array(st.text_input("점 A 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
            B = np.array(st.text_input("점 B 좌표 (예: 1,2)", "1,2").split(','), dtype=float)
            C = np.array(st.text_input("점 C 좌표 (예: 2,1)", "2,1").split(','), dtype=float)
            shape = np.array([A, B, C, A])
        elif shape_type == "사각형":
            A = np.array(st.text_input("점 A 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
            B = np.array(st.text_input("점 B 좌표 (예: 1,2)", "1,2").split(','), dtype=float)
            C = np.array(st.text_input("점 C 좌표 (예: 2,2)", "2,2").split(','), dtype=float)
            D = np.array(st.text_input("점 D 좌표 (예: 2,1)", "2,1").split(','), dtype=float)
            shape = np.array([A, B, C, D, A])
        elif shape_type == "원":
            center = np.array(st.text_input("원 중심 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
            radius = st.number_input("반지름", value=2.0, step=0.1, format="%.1f")
            theta = np.linspace(0, 2*np.pi, 200)
            shape = np.stack([center[0] + radius * np.cos(theta),
                                center[1] + radius * np.sin(theta)], axis=1)
        elif shape_type == "직선":
            st.markdown("직선의 형태: $ax + by = c$")
            a = st.number_input("계수 a", value=1.0, step=0.1, format="%.1f")
            b = st.number_input("계수 b", value=1.0, step=0.1, format="%.1f")
            c = st.number_input("상수 c", value=2.0, step=0.1, format="%.1f")
            x_vals = np.linspace(-20, 20, 400)
            if b != 0:
                y_vals = (c - a * x_vals) / b
            else:
                x_vals = np.full(400, c / a)
                y_vals = np.linspace(-5, 5, 400)
            shape = np.stack([x_vals, y_vals], axis=1)

        st.subheader("# 2×2 변환 행렬 입력 ___________________")
        a11 = st.number_input("a11", value=1.0, step=0.1, format="%.1f")
        a12 = st.number_input("a12", value=-1.0, step=0.1, format="%.1f")
        a21 = st.number_input("a21", value=1.0, step=0.1, format="%.1f")
        a22 = st.number_input("a22", value=2.0, step=0.1, format="%.1f")
        matrix = np.array([[a11, a12], [a21, a22]])

    with col2:
        # 직선 관련 계수 기본값 선언 (에러 방지용)
        if shape_type == "직선":
            a, b, c = a, b, c
        else:
            a, b, c = 1, 1, 1

        #변환적용
        transformed = np.dot(shape, matrix.T)

        st.subheader("시각화 결과")
        st.subheader("수식 표시")
        st.latex(
            fr"""\text{{입력된 행렬}} =
    \begin{{bmatrix}}
    {a11} & {a12} \\
    {a21} & {a22}
    \end{{bmatrix}}"""
        )

        if shape_type == "원":
            st.latex(rf"(x - {format_number(center[0])})^2 + (y - {format_number(center[1])})^2 = {format_number(radius)}^2")
        elif shape_type == "직선":
            st.latex(rf"\text{{입력된 직선:}} \quad {format_number(a)}x + {format_number(b)}y = {format_number(c)}")

        fig = plot_shape(shape_type, shape, transformed, matrix, 'NanumGothic', a, b, c)
        st.plotly_chart(fig, use_container_width=True)



