import streamlit as st
import os

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

# 3. 사이드바 (심플한 범례)
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
    
    # 복잡한 숫자 범위 삭제 -> 직관적인 색상 설명
    st.info("🟦 **습윤 (Wet Conditions)**")
    st.caption("색이 진할수록 수분 과잉 상태가 강함")
    
    st.error("🟥 **가뭄 (Drought Conditions)**")
    st.caption("색이 진할수록 건조/가뭄 강도가 심함")
    
    st.markdown("---")
    st.write("※ **0 (흰색/회색)** : 정상 기후 범위")

# =========================================================
# 4. 핵심 기능: 월별 영상 재생 및 분석 로직
# =========================================================

def show_bird_analysis(bird_code, bird_name):
    """
    bird_code: 파일명 앞부분 (예: bird1)
    bird_name: 화면에 표시할 한글 이름
    """
    st.markdown(f"### 📅 {bird_name} - 월별 시계열 변화 (2014~2024)")
    
    # 1. 월 선택 버튼 (1, 2, 3, 10, 11, 12월)
    selected_month = st.radio(
        "분석할 월(Month)을 선택하세요:",
        options=["01", "02", "03", "10", "11", "12"],
        format_func=lambda x: f"{x}월",
        horizontal=True,
        key=bird_code  # 탭별 충돌 방지용 키
    )
    
    col1, col2 = st.columns([1.8, 1])
    
    # 파일명 조합 (예: bird1_01.mp4)
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    # --- 왼쪽: 영상 재생 ---
    with col1:
        if os.path.exists(video_file):
            st.video(video_file)
            st.caption(f"🎥 재생 중: {bird_name} {selected_month}월 분포 변화")
        else:
            st.warning(f"⚠️ 영상 파일을 찾을 수 없습니다.")
            st.code(f"필요한 파일명: {video_file}")

    # --- 오른쪽: 분석 멘트 (계절별 공통 분석) ---
    with col2:
        st.subheader(f"📊 {selected_month}월 분석 포인트")
        
        if selected_month in ["01", "02", "12"]:
            st.markdown("""
            **❄️ 동계 (Winter Season)**
            * **기후 특징:** 저온 건조하며, SPEI 지수의 변동성이 크게 나타나는 시기.
            * **관전 포인트:**
                * 내륙 습지 결빙 여부와 해안가 분포의 관계.
                * 가뭄(붉은색) 심화 연도에 개체군 밀집 지역이 어떻게 변화하는지 비교.
            """)
            
        elif selected_month in ["03"]:
            st.markdown("""
            **🌱 춘계 (Spring Transition)**
            * **기후 특징:** 기온이 상승하고 강수 패턴이 변화하는 계절적 전환기.
            * **관전 포인트:**
                * 월동 개체군의 이동 또는 번식 준비에 따른 분포 확산 여부.
                * 습윤(푸른색) 지역과 조류 분포의 매칭도 확인.
            """)
            
        else: # 10, 11월
            st.markdown("""
            **🍂 추계 (Autumn Season)**
            * **기후 특징:** 건기가 시작되는 시점으로, 서식지 수위 변화에 민감.
            * **관전 포인트:**
                * 기온 하강에 따라 개체군이 남하하거나 특정 수계로 모이는 경향.
                * 서식지 환경(가뭄 등) 변화에 따른 초기 분포 밀도 차이 관측.
            """)

# =========================================================
# 5. 메인 탭 구성 (4종 조류)
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "1. 괭이갈매기", 
    "2. 흰뺨검둥오리", 
    "3. 쇠백로", 
    "4. 쇠물닭"
])

with tab1:
    show_bird_analysis("bird1", "괭이갈매기")

with tab2:
    show_bird_analysis("bird2", "흰뺨검둥오리")

with tab3:
    show_bird_analysis("bird3", "쇠백로")

with tab4:
    show_bird_analysis("bird4", "쇠물닭")