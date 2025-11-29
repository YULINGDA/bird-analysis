import streamlit as st
import os
import base64

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="조류 분포 & SPEI 상관관계 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 제목 및 헤더
st.title("🦅 기후 변화(SPEI)와 조류 서식지 분포 상관관계 분석")
st.markdown("""
이 대시보드는 **2014년부터 2024년까지** 한반도 내 주요 조류 4종의 분포 변화와 
**기후 가뭄 지수(SPEI)** 간의 시공간적 패턴을 시각화하여 분석합니다.
""")
st.divider()

# 3. 사이드바
with st.sidebar:
    st.header("📝 지표 정의: SPEI")
    st.markdown("**Standardized Precipitation–Evapotranspiration Index**")
    with st.expander("📌 정의 및 원리", expanded=True):
        st.markdown("""
        * **정의:** 강수량(P)과 잠재증발산량(PET)의 차이를 이용한 표준화 지수.
        * **핵심:** 기온 상승에 따른 증발산 효과를 반영하여 실질적인 건조 상태를 파악함.
        """)
    st.divider()
    st.subheader("🎨 지도 색상 해석")
    st.info("🟦 **습윤 (Wet)** : 색이 진할수록 수분 과잉")
    st.error("🟥 **가뭄 (Dry)** : 색이 진할수록 건조 심함")
    st.write("※ **0 (흰색)** : 정상 기후 범위")

# =========================================================
# 4. 분석 결과 텍스트 반환 함수
# =========================================================

def get_analysis_text(bird_code, month):
    if bird_code == "bird1":
        if month in ["12", "01"]: return "**[동계]** SPEI가 높을수록(습윤) 분포 증가 경향."
        elif month == "10": return "**[추계]** 22, 24년 높은 밀도 기록."
        elif month == "03": return "**[특이점]** 23년 3월 이상 급증."
        return "특이 사항 없음."
    elif bird_code == "bird2":
        if month in ["01", "02"]: return "**[동계]** SPEI 무관하게 고밀도 유지 (강한 내성)."
        elif month == "03": return "**[춘계]** 건조할수록 분포 증가 역상관."
        elif month in ["11", "12"]: return "**[추세]** 연도별 개체수 자체 증가 뚜렷."
        return "특이 사항 없음."
    elif bird_code == "bird3":
        if month == "01": return "**[핵심]** SPEI와 가장 뚜렷한 양의 상관관계."
        elif month == "02": return "**[특이점]** 건조해졌으나 분포 증가하는 역설적 패턴."
        elif month in ["11", "12"]: return "**[동계]** 습윤할수록 분포 증가."
        return "특이 사항 없음."
    elif bird_code == "bird4":
        if month == "01": return "**[핵심]** SPEI 양의 상관. 21년 기점 증가."
        elif month in ["10", "11", "12"]: return "**[한계]** 여름 철새라 데이터 희소."
        return "개체수 변화 미미함."
    return "데이터 없음"

# =========================================================
# 5. [핵심기술] 동시 재생을 위한 HTML 생성 함수
# =========================================================
def get_video_html(file_path, width="100%"):
    """
    영상 파일을 HTML 코드로 변환하여 강제 자동 재생(Autoplay) 시키는 함수
    """
    try:
        with open(file_path, "rb") as f:
            video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
        # autoplay: 자동재생, loop: 반복, muted: 음소거 (음소거 안 하면 브라우저가 자동재생 막음)
        return f'''
        <video width="{width}" autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
        </video>
        '''
    except:
        return None

# =========================================================
# 6. 개별 보기 함수
# =========================================================

def show_bird_analysis(bird_code, bird_name):
    st.markdown(f"### 📅 {bird_name} - 월별 변화")
    selected_month = st.radio(
        f"{bird_name} 월 선택:", ["01", "02", "03", "10", "11", "12"], 
        key=bird_code, horizontal=True
    )
    col1, col2 = st.columns([1.8, 1])
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    with col1:
        if os.path.exists(video_file):
            # 개별 보기는 그냥 일반 플레이어 사용
            st.video(video_file)
        else:
            st.info("⚠️ 영상 파일 없음")
    with col2:
        st.info(get_analysis_text(bird_code, selected_month))

# =========================================================
# 7. 비교 분석 화면 (동시 재생 기능 적용)
# =========================================================

def show_comparison():
    st.markdown("### ⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.caption("아래 버튼을 누르면 두 종의 영상이 **동시에 재생**됩니다.")
    
    bird_map = {
        "괭이갈매기": "bird1",
        "흰뺨검둥오리": "bird2",
        "쇠백로": "bird3",
        "쇠물닭": "bird4"
    }
    
    # 컨트롤 패널
    c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1])
    with c1:
        left_name = st.selectbox("비교군 A (좌)", list(bird_map.keys()), index=2)
    with c2:
        right_name = st.selectbox("비교군 B (우)", list(bird_map.keys()), index=1)
    with c3:
        comp_month = st.select_slider("비교할 월(Month)", options=["01", "02", "03", "10", "11", "12"])
    
    with c4:
        st.write("") 
        play_btn = st.button("▶️ 동시 재생 Start", type="primary")

    st.divider()

    # 파일 경로 확인
    left_code = bird_map[left_name]
    right_code = bird_map[right_name]
    file_left = f"{left_code}_{comp_month}.mp4"
    file_right = f"{right_code}_{comp_month}.mp4"

    # 화면 분할
    col_l, col_r = st.columns(2)

    # 버튼 눌렀을 때만 작동
    if play_btn:
        if os.path.exists(file_left) and os.path.exists(file_right):
            # 좌측 영상 HTML 생성
            html_left = get_video_html(file_left)
            # 우측 영상 HTML 생성
            html_right = get_video_html(file_right)

            with col_l:
                st.success(f"🅰️ {left_name}")
                if html_left:
                    st.markdown(html_left, unsafe_allow_html=True) # HTML 강제 실행
                    st.caption(get_analysis_text(left_code, comp_month))
            
            with col_r:
                st.warning(f"🅱️ {right_name}")
                if html_right:
                    st.markdown(html_right, unsafe_allow_html=True) # HTML 강제 실행
                    st.caption(get_analysis_text(right_code, comp_month))
        else:
            st.error("❌ 선택한 월의 영상 파일이 없습니다.")
    else:
        # 대기 화면
        with col_l:
            st.info("👈 비교군 A를 선택하세요.")
        with col_r:
            st.info("👉 비교군 B를 선택하세요.")

# =========================================================
# 8. 메인 탭 실행
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 괭이갈매기", "2. 흰뺨검둥오리", "3. 쇠백로", "4. 쇠물닭", "⚔️ 비교 분석"
])

with tab1: show_bird_analysis("bird1", "괭이갈매기")
with tab2: show_bird_analysis("bird2", "흰뺨검둥오리")
with tab3: show_bird_analysis("bird3", "쇠백로")
with tab4: show_bird_analysis("bird4", "쇠물닭")
with tab5: show_comparison()
