import streamlit as st
import numpy as np
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

def run_symmetry_rotation():
    st.header("(2) 두 번의 대칭이동 시뮬레이터")
    st.caption("두 축 대칭 → 결과가 회전과 같음을 관찰하세요.")

    axis_options = ["x축", "y축", "y=ax"]

    col1, col2 = st.columns(2)
    axis1 = col1.selectbox("첫 번째 대칭축", axis_options, key="axis1")
    axis2 = col2.selectbox("두 번째 대칭축", axis_options, key="axis2")

    angle1 = angle2 = 0
    if axis1 == "y=ax":
        angle1 = st.slider("첫 번째 축의 각도 (y=ax)", -90, 90, 45, key="angle_slider1")
    if axis2 == "y=ax":
        angle2 = st.slider("두 번째 축의 각도 (y=ax)", -90, 90, -45, key="angle_slider2")

    def get_reflection_matrix(axis, angle_deg):
        if axis == "x축":
            return np.array([[1, 0], [0, -1]])
        elif axis == "y축":
            return np.array([[-1, 0], [0, 1]])
        elif axis == "y=ax":
            theta = np.deg2rad(angle_deg)
            cos2t = np.cos(2 * theta)
            sin2t = np.sin(2 * theta)
            return np.array([[cos2t, sin2t], [sin2t, -cos2t]])
        else:
            raise ValueError("Unknown axis")

    if "point" not in st.session_state:
        st.session_state.point = [2.0, 2.0]

    click_fig = go.Figure()
    click_fig.update_layout(
        width=600, height=600, margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
        xaxis=dict(range=[-10, 10], zeroline=True, showgrid=True),
        yaxis=dict(range=[-10, 10], zeroline=True, showgrid=True),
    )
    click_fig.add_trace(go.Scatter(
        x=[st.session_state.point[0]],
        y=[st.session_state.point[1]],
        mode="markers",
        marker=dict(color="blue", size=10),
        name="원래 점"
    ))

    event = plotly_events(click_fig, click_event=True, key="click")
    if event:
        st.session_state.point = [event[0]["x"], event[0]["y"]]

    P = np.array(st.session_state.point)
    A = get_reflection_matrix(axis1, angle1)
    B = get_reflection_matrix(axis2, angle2)
    P1 = A @ P
    P2 = B @ P1

    fig = go.Figure()
    fig.update_layout(
        width=800, height=800,
        margin=dict(l=0, r=0, b=0, t=0),
        xaxis=dict(range=[-10, 10], zeroline=True, showgrid=True),
        yaxis=dict(range=[-10, 10], zeroline=True, showgrid=True),
    )
    fig.add_trace(go.Scatter(x=[P[0]], y=[P[1]], mode="markers", marker=dict(color="blue", size=10), name="원래 점"))
    fig.add_trace(go.Scatter(x=[P2[0]], y=[P2[1]], mode="markers", marker=dict(color="red", size=10), name="변환된 점"))

    def plot_axis(axis, angle_deg, name):
        if axis == "x축":
            x = np.array([-10, 10])
            y = np.array([0, 0])
        elif axis == "y축":
            x = np.array([0, 0])
            y = np.array([-10, 10])
        elif axis == "y=ax":
            theta = np.deg2rad(angle_deg)
            slope = np.tan(theta)
            x = np.array([-10, 10])
            y = slope * x
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(dash="dot", color="orange"), name=name))

    plot_axis(axis1, angle1, "첫 번째 축")
    plot_axis(axis2, angle2, "두 번째 축")

    st.plotly_chart(fig, use_container_width=True)
