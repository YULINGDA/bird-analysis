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
# 4. 분석 결과 텍스트 생성 함수
# =========================================================

def get_analysis_text(bird_code, month):
    if bird_code == "bird1": # 괭이갈매기
        if month in ["12", "01"]:
            return "**[동계]** SPEI가 높을수록(습윤) 분포가 증가하는 경향."
        elif month == "10":
            return "**[추계]** 22년, 24년에 특히 높은 밀도 기록."
        elif month == "03":
            return "**[특이점]** 23년 3월 이상 급증. 기후 외 요인 영향 큼."
        else: return "특이 사항 없음."

    elif bird_code == "bird2": # 흰뺨검둥오리
        if month in ["01", "02"]:
            return "**[동계]** SPEI와 무관하게 전국적으로 고밀도 유지 (강한 내성)."
        elif month == "03":
            return "**[춘계]** 건조할수록 오히려 분포가 느는 역상관 경향 일부 관측."
        elif month in ["11", "12"]:
            return "**[추세]** 기후보다는 연도별 개체수 자체 증가 추세가 뚜렷함."
        else: return "특이 사항 없음."

    elif bird_code == "bird3": # 쇠백로
        if month == "01":
            return "**[핵심]** SPEI와 가장 뚜렷한 양의 상관관계 (가뭄 시 급감)."
        elif month == "02":
            return "**[특이점]** 21년부터 건조해졌으나 분포는 증가하는 역설적 패턴."
        elif month in ["11", "12"]:
            return "**[동계]** 습윤할수록 분포 증가 경향 뚜렷함."
        else: return "특이 사항 없음."

    elif bird_code == "bird4": # 쇠물닭
        if month == "01":
            return "**[핵심]** SPEI와 양의 상관관계. 21년 기점 개체수 증가."
        elif month in ["10", "11", "12"]:
            return "**[한계]** 여름 철새 특성상 동계 데이터 희소함."
        else: return "개체수 변화 미미함."
    
    return "분석 결과 없음"

# =========================================================
# 5. 개별 보기 함수
# =========================================================

def show_bird_analysis(bird_code, bird_name):
    st.markdown(f"### 📅 {bird_name} - 월별 변화")
    selected_month = st.radio(
        "월(Month) 선택:", 
        ["01", "02", "03", "10", "11", "12"], 
        key=bird_code, horizontal=True
    )
    col1, col2 = st.columns([1.8, 1])
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    with col1:
        if os.path.exists(video_file):
            st.video(video_file)
        else:
            st.info("⚠️ 해당 월의 영상 데이터가 없습니다.")
    with col2:
        st.info(get_analysis_text(bird_code, selected_month))

# =========================================================
# 6. [NEW] 비교 분석 함수 (여기가 새로 추가된 부분!)
# =========================================================

def show_comparison():
    st.markdown("### ⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.markdown("두 종의 분포 변화를 나란히 비교하여 **기후 민감도 차이**를 확인합니다.")
    
    # 새 이름 매핑
    bird_dict = {
        "1. 괭이갈매기": "bird1",
        "2. 흰뺨검둥오리": "bird2",
        "3. 쇠백로": "bird3",
        "4. 쇠물닭": "bird4"
    }
    
    # 상단 컨트롤 패널
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        left_bird = st.selectbox("비교군 A (좌측)", list(bird_dict.keys()), index=2) # 기본값: 쇠백로
    with c2:
        right_bird = st.selectbox("비교군 B (우측)", list(bird_dict.keys()), index=1) # 기본값: 흰뺨검둥오리
    with c3:
        comp_month = st.select_slider("비교할 월(Month)", options=["01", "02", "03", "10", "11", "12"])

    # 화면 분할
    left_col, right_col = st.columns(2)
    
    # --- 좌측 영상 ---
    with left_col:
        l_code = bird_dict[left_bird]
        l_file = f"{l_code}_{comp_month}.mp4"
        st.success(f"🅰️ {left_bird}")
        if os.path.exists(l_file):
            st.video(l_file)
            st.caption(get_analysis_text(l_code, comp_month))
        else:
            st.warning("영상 없음")

    # --- 우측 영상 ---
    with right_col:
        r_code = bird_dict[right_bird]
        r_file = f"{r_code}_{comp_month}.mp4"
        st.warning(f"🅱️ {right_bird}")
        if os.path.exists(r_file):
            st.video(r_file)
            st.caption(get_analysis_text(r_code, comp_month))
        else:
            st.warning("영상 없음")

# =========================================================
# 7. 메인 탭 구성 (탭 5개로 늘어남)
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 괭이갈매기", "2. 흰뺨검둥오리", "3. 쇠백로", "4. 쇠물닭", "⚔️ 비교 분석"
])

with tab1: show_bird_analysis("bird1", "괭이갈매기")
with tab2: show_bird_analysis("bird2", "흰뺨검둥오리")
with tab3: show_bird_analysis("bird3", "쇠백로")
with tab4: show_bird_analysis("bird4", "쇠물닭")
with tab5: show_comparison() # 새로 추가된 비교 탭
