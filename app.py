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
            return "**[핵심]** SPEI와 가장 뚜렷한 양의 상관관계 (가뭄 시 급감)."
        elif month == "02":
            return "**[특이점]** 21년부터 건조해졌으나 분포는 증가하는 역설적 패턴."
        elif month in ["11", "12"]:
            return "**[동계]** 습윤할수록 분포 증가 경향 뚜렷함."
        return "특이 사항 없음."

    # 4. 쇠물닭
    elif bird_code == "bird4":
        if month == "01":
            return "**[핵심]** SPEI와 양의 상관관계. 21년 기점 개체수 증가."
        elif month in ["10", "11", "12"]:
            return "**[한계]** 여름 철새 특성상 동계 데이터 희소함."
        return "개체수 변화 미미함."
    
    return "데이터 없음"

# =========================================================
# 5. 개별 종 분석 화면 함수
# =========================================================

def show_bird_analysis(bird_code, bird_name):
    st.markdown(f"### 📅 {bird_name} - 월별 변화")
    
    # 월 선택
    selected_month = st.radio(
        f"{bird_name} 월 선택:", 
        ["01", "02", "03", "10", "11", "12"], 
        key=bird_code, 
        horizontal=True
    )
    
    col1, col2 = st.columns([1.8, 1])
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    with col1:
        if os.path.exists(video_file):
            st.video(video_file)
            st.caption(f"🎥 재생 중: {video_file}")
        else:
            st.info("⚠️ 해당 월의 영상 파일이 없습니다.")
            st.code(video_file)

    with col2:
        st.subheader("📊 상세 분석")
        info_text = get_analysis_text(bird_code, selected_month)
        st.info(info_text)

# =========================================================
# 6. 비교 분석 화면 함수 (여기가 핵심!)
# =========================================================

def show_comparison():
    st.markdown("### ⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.markdown("두 종의 분포 변화를 나란히 비교하여 **기후 민감도 차이**를 확인합니다.")
    
    # 새 이름과 코드 매핑
    bird_map = {
        "괭이갈매기": "bird1",
        "흰뺨검둥오리": "bird2",
        "쇠백로": "bird3",
        "쇠물닭": "bird4"
    }
    
    # 컨트롤 패널
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        # 쇠백로를 기본값으로
        left_name = st.selectbox("비교군 A (좌측)", list(bird_map.keys()), index=2)
    with c2:
        # 흰뺨검둥오리를 기본값으로
        right_name = st.selectbox("비교군 B (우측)", list(bird_map.keys()), index=1)
    with c3:
        comp_month = st.select_slider("비교할 월(Month)", options=["01", "02", "03", "10", "11", "12"])

    # 비디오 파일명 생성
    left_code = bird_map[left_name]
    right_code = bird_map[right_name]
    
    file_left = f"{left_code}_{comp_month}.mp4"
    file_right = f"{right_code}_{comp_month}.mp4"

    # 화면 분할 표시
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.success(f"🅰️ {left_name}")
        if os.path.exists(file_left):
            st.video(file_left)
            st.caption(get_analysis_text(left_code, comp_month))
        else:
            st.warning("영상 없음")

    with col_r:
        st.warning(f"🅱️ {right_name}")
        if os.path.exists(file_right):
            st.video(file_right)
            st.caption(get_analysis_text(right_code, comp_month))
        else:
            st.warning("영상 없음")

# =========================================================
# 7. 메인 탭 실행
# =========================================================

# 탭 5개 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 괭이갈매기", "2. 흰뺨검둥오리", "3. 쇠백로", "4. 쇠물닭", "⚔️ 비교 분석"
])

with tab1:
    show_bird_analysis("bird1", "괭이갈매기")
with tab2:
    show_bird_analysis("bird2", "흰뺨검둥오리")
with tab3:
    show_bird_analysis("bird3", "쇠백로")
with tab4:
    show_bird_analysis("bird4", "쇠물닭")
with tab5:
    show_comparison()
