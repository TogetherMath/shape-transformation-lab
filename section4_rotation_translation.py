import streamlit as st
import numpy as np
import plotly.graph_objs as go


def run_rotation_translation():
    st.header("🟥 (4) 회전과 평행이동 시뮬레이터")
    st.latex(r"w = (\cos\theta + i\sin\theta)(z + \alpha) + \beta")
    st.markdown("평행이동&회전이동&평행이동은 회전이동일까요? 회전의 기준점은?")

    # 윗줄: alpha, theta, beta 입력
    st.subheader("🔧 α, θ, β 값을 정해 보세요.")
    upper_col1, upper_col2, upper_col3 = st.columns(3)

    with upper_col1:
        st.markdown("**α (회전 이전 평행이동)**")
        alpha_re = st.number_input("Re(α)", value=1.0, step=0.5, format="%.2f", key="alpha_re")
        alpha_im = st.number_input("Im(α)", value=0.0, step=0.5, format="%.2f", key="alpha_im")

    with upper_col2:
        st.markdown("**θ (회전각, 도)**")
        theta_deg = st.number_input("회전각 θ", value=45.0, step=1.0, format="%.1f")
        theta_rad = np.radians(theta_deg)
        cos_theta = np.cos(theta_rad)
        sin_theta = np.sin(theta_rad)

    with upper_col3:
        st.markdown("**β (회전 이후 평행이동)**")
        beta_re = st.number_input("Re(β)", value=0.0, step=0.5, format="%.2f", key="beta_re")
        beta_im = st.number_input("Im(β)", value=0.0, step=0.5, format="%.2f", key="beta_im")

    st.divider()

    # 아랫줄: z 입력 + 시각화
    st.subheader("🖱 입력 복소수 z 와 변환 결과 w 시각화")
    lower_col1, lower_col2 = st.columns([1, 1.5])

    with lower_col1:
        st.markdown("**z = x + iy**")
        x = st.number_input("x (실수 부분)", value=2.0, step=0.5, format="%.2f", key="z_x")
        y = st.number_input("y (허수 부분)", value=1.0, step=0.5, format="%.2f", key="z_y")

     

    with lower_col2:
        # ✅ 복소수 정의 및 변환
        z = complex(x, y)
        alpha = complex(alpha_re, alpha_im)
        beta = complex(beta_re, beta_im)
        rotator = complex(cos_theta, sin_theta)
        w = rotator * (z + alpha) + beta

        # ✅ 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[z.real], y=[z.imag], mode='markers',
                                 marker=dict(size=12, color='blue'), name='입력 z'))
        fig.add_trace(go.Scatter(x=[w.real], y=[w.imag], mode='markers',
                                 marker=dict(size=12, color='red'), name='변환 결과 w'))
        fig.add_trace(go.Scatter(x=[alpha.real], y=[alpha.imag], mode='markers',
                                 marker=dict(size=10, color='purple', symbol='x'), name='이동 전 수치 α'))
        fig.add_trace(go.Scatter(x=[beta.real], y=[beta.imag], mode='markers',
                                 marker=dict(size=10, color='orange', symbol='x'), name='이동 후 수치 β'))

        fig.update_layout(
            title="복소평면에서의 회전+평행이동 변환 시각화",
            xaxis_title="Re", yaxis_title="Im",
            xaxis=dict(scaleanchor='y', scaleratio=1, showgrid=True, zeroline=True, range=[-10, 10]),
            yaxis=dict(scaleanchor='x', scaleratio=1, showgrid=True, zeroline=True, range=[-10, 10]),
            width=600, height=600, showlegend=True
        )
        st.plotly_chart(fig)
