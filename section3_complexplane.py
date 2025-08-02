import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import plotly.graph_objects as go


def run_matrix_transform():
    st.header("🟩 (1) 행렬에 의한 일차변환 시뮬레이터")



# ✅ 페이지 설정
st.set_page_config(page_title="도형 변환 실험실", layout="wide")
st.title("🔄 도형 변환 실험실")

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

################## (3) #####################

st.subheader("🔷 복소평면에서의 변환")
st.write("복소수를 이용한 여러 변환을 실험할 수 있습니다.")

col1, col2 = st.columns([1, 1])

with col1:
    st.title("🔁 복소평면에서의 변환 실험")
    st.markdown("복소수 $z = x + iy$ 로 정의된 도형을 복소함수 $w = f(z)$ 를 통해 변환해 보세요.")

    # ✅ 도형 정의식 입력
    st.subheader("1️⃣ z의 자취 : x, y의 관계식")
    st.caption("!!Warning!! 곱은 *로, 제곱은 **로, 등호는 ==로 표기하세요.(파이썬표기법)")
    definition = st.text_input("예: 2*y == x**2 + 1", value="x**2 + y**2 == 1", key="definition_input")

    # ✅ 복소함수 입력
    st.subheader("2️⃣ 복소함수식 입력 : w = f(z)")
    st.caption("!!Warning!! 허수 i는 1j로 표기하세요.(파이썬 표기법)")
    fz_input = st.text_input("w =", value="(z - 1j)**2", key="function_input")

# ✅ 자동 정의역 추정 및 마스킹
Z_selected = None
final_range = None
max_attempts = 10
# 원본 정의식 보존
original = definition
for attempt in range(max_attempts):
    range_size = 8 + attempt * 2
    N = 800
    x = np.linspace(-range_size, range_size, N)
    y = np.linspace(-range_size, range_size, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    eps = (2 * range_size) / (N - 1)
    eps *= 2  # 허용오차 배율 조정 (라인도 두께 보장)
    try:
        local_vars = {"x": X, "y": Y, "np": np, "i": 1j}
        # 등식 비교일 때 동적 eps 사용
        if "==" in original:
            left, right = original.split("==")
            L = eval(left, local_vars)
            R = eval(right, local_vars)
            mask = np.abs(L - R) < eps
        else:
            mask = eval(original, local_vars)
        mask = np.array(mask, dtype=bool)
        if mask.sum() > 0:
            Z_selected = Z[mask]
            final_range = range_size
            break
    except Exception:
        continue

if Z_selected is None or Z_selected.size == 0:
    st.error("오류 : 식을 다시 확인해 주세요.")
else:
    # ✅ 복소함수 적용
    try:
        W = eval(fz_input, {"z": Z_selected, "np": np})
    except Exception as e:
        st.error(f"복소함수 적용 오류: {e}")
        W = None

    # ✅ 시각화
    with col2:
        if W is not None and getattr(W, 'size', 0) > 0:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=Z_selected.real, y=Z_selected.imag,
                mode='markers', marker=dict(size=4, color='blue'),
                name='변환 전 도형 z'
            ))
            fig.add_trace(go.Scatter(
                x=W.real, y=W.imag,
                mode='markers', marker=dict(size=4, color='red'),
                name='변환 후 도형 w'
            ))

            # 축 및 그리드, 스케일 동기화
            all_re = np.concatenate([Z_selected.real, W.real])
            all_im = np.concatenate([Z_selected.imag, W.imag])
            x_min, x_max = all_re.min(), all_re.max()
            y_min, y_max = all_im.min(), all_im.max()
            margin = max(x_max - x_min, y_max - y_min) * 0.1
            fig.update_xaxes(
                range=[x_min - margin, x_max + margin],
                zeroline=True, zerolinecolor='gray',
                showgrid=True, gridcolor='lightgray',
                scaleanchor='y', scaleratio=1
            )
            fig.update_yaxes(
                range=[y_min - margin, y_max + margin],
                zeroline=True, zerolinecolor='gray',
                showgrid=True, gridcolor='lightgray',
                scaleanchor='x', scaleratio=1
            )
            fig.update_layout(
                title='복소함수를 통한 도형 변환',
                xaxis_title='Re', yaxis_title='Im',
                width=600, height=600, showlegend=True
            )
            st.plotly_chart(fig)
        else:
            st.warning("복소함수 적용 결과가 없습니다.")





