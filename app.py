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

# 3. 사이드바 (범례 및 설명)
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
# 4. 분석 결과 텍스트 반환 함수 (단순화)
# =========================================================

def get_analysis_text(bird_code, month):
    # 1. 괭이갈매기
    if bird_code == "bird1":
        if month in ["12", "01"]:
            return "**[동계]** SPEI가 높을수록(습윤) 분포가 증가하는 경향."
        elif month == "10":
            return "**[추계]** 22년, 24년에 특히 높은 밀도 기록."
        elif month == "03":
            return "**[특이점]** 23년 3월 이상 급증. 기후 외적 요인 영향 큼."
        return "특이 사항 없음."

    # 2. 흰뺨검둥오리
    elif bird_code == "bird2":
        if month in ["01", "02"]:
            return "**[동계]** SPEI와 무관하게 전국적으로 고밀도 유지 (강한 내성)."
        elif month == "03":
            return "**[춘계]** 건조할수록 오히려 분포가 느는 역상관 경향 일부 관측."
        elif month in ["11", "12"]:
            return "**[추세]** 기후보다는 연도별 개체수 자체 증가 추세가 뚜렷함."
        return "특이 사항 없음."

    # 3. 쇠백로
    elif bird_code == "bird3":
        if month == "01":
            return "**[핵심]** SPEI와 가장 뚜렷한 양의 상관관계 (가
