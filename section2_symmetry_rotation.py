import streamlit as st
import numpy as np
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

# ✅ 대칭 행렬 생성 함수 (축의 종류와 각도 입력 → 행렬)
def reflection_matrix(axis_type, angle_deg=None):
    
    if axis_type == 'x축':
        return np.array([[1, 0], [0, -1]])
    elif axis_type == 'y축':
        return np.array([[-1, 0], [0, 1]])
    elif axis_type == '직선y=ax':
        # 각도 → 라디안 → 기울기
        theta_rad = np.radians(angle_deg)
        a = np.tan(theta_rad)
        norm = 1 + a**2
        return (1 / norm) * np.array([[1 - a**2, 2*a], [2*a, a**2 - 1]])

# ✅ 시뮬레이터 실행 함수
def run_symmetry_rotation():
    st.header("(2) 두 번의 대칭이동 시뮬레이터")
    st.caption("두 축 대칭의 결과가 회전과 같음을 시각적으로 관찰해 보세요.")



    # 초기 점
    if 'selected_point' not in st.session_state:
        st.session_state.selected_point = np.array([2.0, 1.0])
    x0, y0 = st.session_state.selected_point

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("🖱 입력 설정")
        st.markdown("⬇️ **초기점과 2개의 대칭축을 입력하여 변환된 점을 관찰해 보세요.**")

        # ✅ 초기 점 좌표 입력 (← 이 부분이 새로 추가될 영역입니다)
        st.markdown("🔵 **초기점 좌표를 입력하세요.(-5와 5사이)**")
        x0 = st.number_input("x 좌표", value=2.0, step=0.3, format="%.2f", key="input_x")
        y0 = st.number_input("y 좌표", value=1.0, step=0.3, format="%.2f", key="input_y")
        st.session_state.selected_point = np.array([x0, y0])

        axis1 = st.selectbox("1️⃣ 첫 번째 대칭축", ["x축", "y축", "직선y=ax"], key="axis1")
        if axis1 == "직선y=ax":
            angle1 = st.number_input("x축과 이루는 각도 θ₁ (도)", value=45.0,
                                     step=0.1, format="%.1f", key="angle1")
        else:
            angle1 = 45.0

        axis2 = st.selectbox("2️⃣ 두 번째 대칭축", ["x축", "y축", "직선y=ax"], key="axis2")
        if axis2 == "직선y=ax":
            angle2 = st.number_input("x축과 이루는 각도 θ₂ (도)", value=-45.0,
                                     step=0.1, format="%.1f", key="angle2")
        else:
            angle2 = -45.0

        st.markdown("🔵 입력점 | 🟢 1차 대칭 | 🔴 최종 대칭 결과")
        st.markdown("🟣 축1 (보라색 선), 🟠 축2 (주황색 선)")

    with col2:
        # 행렬
        R1 = reflection_matrix(axis1, angle1 if angle1 is not None else 1.0)
        R2 = reflection_matrix(axis2, angle2 if angle2 is not None else 1.0)

        # 대칭 계산
        P0 = np.array([x0, y0])
        P1 = R1 @ P0
        P2 = R2 @ P1

        # 그래프 생성
        fig = go.Figure()
        fig.update_layout(title="좌표 평면", xaxis=dict(range=[-5, 5]), yaxis=dict(range=[-5, 5]),
                          width=600, height=600)

        # 🎯 대칭축 시각화 함수
        def draw_axis(axis, angle, name, color):
            # ── 1) 공백 제거로 문자열 통일 ──
            
            # ── 2) 통일된 axis_norm으로 분기 ──
            if axis == "x축":
                fig.add_trace(go.Scatter(
                    x=[-5, 5], y=[0, 0], mode='lines',
                    line=dict(color=color, width=2), name=name
                ))
            elif axis == "y축":
                fig.add_trace(go.Scatter(
                    x=[0, 0], y=[-5, 5], mode='lines',
                    line=dict(color=color, width=2), name=name
                ))
            else:
                if angle is None or not np.isfinite(angle):   # 🔧 추가된 보호 조건
                    angle = 45.0
 
                theta = np.radians(angle)
                a = np.tan(theta)

                # ── 기울기에 따라 화면 안에 들어오도록 축 범위 조정 ──
                if abs(a) <= 1:
                    x_vals = np.array([-5, 5])
                    y_vals = a * x_vals
                else:
                    y_vals = np.array([-5, 5])
                    x_vals = y_vals / a

                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals, mode='lines',
                    line=dict(color=color, width=5), name=name
                ))


        # 점 시각화
        fig.add_trace(go.Scatter(x=[P0[0]], y=[P0[1]], mode='markers',
                                 marker=dict(color='blue', size=10), name='입력점'))
        fig.add_trace(go.Scatter(x=[P1[0]], y=[P1[1]], mode='markers',
                                 marker=dict(color='green', size=10), name='1차 대칭'))
        fig.add_trace(go.Scatter(x=[P2[0]], y=[P2[1]], mode='markers',
                                 marker=dict(color='red', size=10), name='최종 결과'))

        draw_axis(axis1, angle1, "🟣 축1", "purple")
            
        draw_axis(axis2, angle2, "🟠 축2", "orange")


        result = plotly_events(fig, click_event=True, override_height=600)
        if result:
            new_x = result[0]['x']
            new_y = result[0]['y']
            st.session_state.selected_point = np.array([new_x, new_y])
            st.rerun()
