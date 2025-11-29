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

# 3. 사이드바 (범례)
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
    
    st.info("🟦 **습윤 (Wet Conditions)**")
    st.caption("색이 진할수록 수분 과잉 상태가 강함")
    
    st.error("🟥 **가뭄 (Drought Conditions)**")
    st.caption("색이 진할수록 건조/가뭄 강도가 심함")
    
    st.markdown("---")
    st.write("※ **0 (흰색/회색)** : 정상 기후 범위")

# =========================================================
# 4. 분석 결과 텍스트 생성 함수 (사용자 분석 내용 반영)
# =========================================================

def get_analysis_text(bird_code, month):
    """
    각 새와 월에 맞는 분석 멘트를 반환합니다.
    bird1: 괭이갈매기
    bird2: 흰뺨검둥오리
    bird3: 쇠백로
    bird4: 쇠물닭
    """
    
    # -----------------------------------------------------
    # 1. 괭이갈매기 (Bird 1)
    # -----------------------------------------------------
    if bird_code == "bird1":
        if month in ["12", "01"]:
            return """
            **[동계 분포 특징]**
            * 대체로 SPEI가 높은(습윤한) 시기에 가장 많은 개체수 분포를 보임.
            """
        elif month in ["10"]:
            return """
            **[추계 분포 특징]**
            * 2022년과 2024년 10월에 특히 많은 분포 밀도를 기록함.
            """
        elif month in ["03"]:
            return """
            **[춘계 분포 특징 (특이점)]**
            * 2023년 3월, 다른 연도에 비해 비정상적으로 많은 서식이 관찰됨.
            * **결론:** 전반적으로 SPEI와의 선형적인 상관관계는 높지 않은 것으로 판단됨.
            """
        else:
            return "데이터 관측 및 분석 중입니다."

    # -----------------------------------------------------
    # 2. 흰뺨검둥오리 (Bird 2)
    # -----------------------------------------------------
    elif bird_code == "bird2":
        if month in ["01", "02"]:
            return """
            **[동계 분포 특징]**
            * SPEI 지수와 상관없이 전국적으로 높은 밀도의 분포를 유지함.
            * 연도별 변화폭이 크지 않음 (안정적).
            """
        elif month in ["03"]:
            return """
            **[춘계 분포 특징]**
            * 1, 2월에 비해 상대적으로 개체수가 적음.
            * **특이점:** SPEI가 낮아질수록(건조할수록) 개체 분포가 오히려 많아지는 경향이 일부 관측됨.
            """
        elif month in ["10"]:
            return """
            **[추계 분포 특징]**
            * 대체로 SPEI 수치와 무관하게 고른 분포를 보임.
            """
        elif month in ["11", "12"]:
            return """
            **[초겨울 분포 특징]**
            * 가장 많은 개체수를 보여주며, 연도가 지날수록 SPEI와 관계없이 개체수가 증가하는 추세임.
            """

    # -----------------------------------------------------
    # 3. 쇠백로 (Bird 3)
    # -----------------------------------------------------
    elif bird_code == "bird3":
        if month in ["01"]:
            return """
            **[1월 핵심 분석]**
            * **상관관계 뚜렷함:** 2022년을 제외하고, SPEI가 높을수록(습윤할수록) 더 많은 개체가 분포함.
            * 4종 중 SPEI에 따른 변화가 가장 선명하게 나타남.
            """
        elif month in ["02"]:
            return """
            **[2월 특이 패턴]**
            * 2021년부터 SPEI가 감소(건조)하였으나, 오히려 개체수 분포는 증가하는 역설적 패턴이 관측됨 (24년 제외).
            """
        elif month in ["11", "12"]:
            return """
            **[동계 진입기]**
            * SPEI가 높을 때(습윤) 분포가 더 많은 양의 상관 경향을 보임.
            """
        else: # 3월, 10월
            return """
            **[이동기 특징]**
            * SPEI 지수보다는 다른 환경 요인에 의해 분포가 변화하는 것으로 보임 (상관성 낮음).
            """

    # -----------------------------------------------------
    # 4. 쇠물닭 (Bird 4)
    # -----------------------------------------------------
    elif bird_code == "bird4":
        if month in ["01"]:
            return """
            **[1월 핵심 분석]**
            * 평균적으로 SPEI가 높을수록 분포가 높음 (양의 상관).
            * 2021년을 기점으로 개체수가 뚜렷하게 증가함.
            """
        elif month in ["02", "03"]:
            return """
            **[초봄 분포 특징]**
            * SPEI 변화와 관계없이 개체수 및 분포의 변화가 거의 없이 적은 상태 유지.
            """
        elif month in ["10", "11", "12"]:
            return """
            **[추계/동계 특징]**
            * 여름 철새 특성상 해당 시기에는 개체수가 거의 측정되지 않음 (데이터 희소).
            """
    
    return "분석 데이터 없음"


# =========================================================
# 5. 메인 기능: 월별 영상 재생 및 분석 로직
# =========================================================

def show_bird_analysis(bird_code, bird_name):
    """
    bird_code: 파일명 앞부분 (예: bird1)
    bird_name: 화면에 표시할 한글 이름
    """
    st.markdown(f"### 📅 {bird_name} - 월별 시계열 변화 (2014~2024)")
    
    # 1. 월 선택 버튼
    selected_month = st.radio(
        "분석할 월(Month)을 선택하세요:",
        options=["01", "02", "03", "10", "11", "12"],
        format_func=lambda x: f"{x}월",
        horizontal=True,
        key=bird_code
    )
    
    col1, col2 = st.columns([1.8, 1])
    
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    # --- 왼쪽: 영상 재생 ---
    with col1:
        if os.path.exists(video_file):
            st.video(video_file)
            st.caption(f"🎥 재생 중: {bird_name} {selected_month}월 분포 변화")
        else:
            st.warning(f"⚠️ 영상 파일을 찾을 수 없습니다.")
            st.code(f"필요한 파일명: {video_file}")

    # --- 오른쪽: 분석 멘트 (사용자 데이터 반영) ---
    with col2:
        st.subheader(f"📊 {selected_month}월 상세 분석")
        
        # 위에서 만든 함수를 통해 분석 텍스트를 가져옴
        analysis_text = get_analysis_text(bird_code, selected_month)
        
        st.info(analysis_text)
        
        # 공통 주석
        st.caption("※ 분석 근거: 2014-2024 격자별 SPEI 및 개체수 밀도 데이터")

# =========================================================
# 6. 메인 탭 구성 (4종 조류)
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "1. 괭이갈매기", 
    "2. 흰뺨검둥오리", 
    "3. 쇠백로", 
    "4. 쇠물닭"
])

with tab1:
    # bird1 = 괭이갈매기
    show_bird_analysis("bird1", "괭이갈매기")

with tab2:
    # bird2 = 흰뺨검둥오리 (주의: 사용자 텍스트 순서와 다를 수 있으니 코드 매핑 확인)
    show_bird_analysis("bird2", "흰뺨검둥오리")

with tab3:
    # bird3 = 쇠백로
    show_bird_analysis("bird3", "쇠백로")

with tab4:
    # bird4 = 쇠물닭
    show_bird_analysis("bird4", "쇠물닭")