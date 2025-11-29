import streamlit as st
import os
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="조류 분포 & SPEI 상관관계 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 헤더
st.title("🦅 기후 변화(SPEI)와 조류 서식지 분포 상관관계 분석")
st.markdown("이 대시보드는 **2014~2024년** 데이터를 기반으로 **기후 가뭄 지수(SPEI)**와 **철새 서식지 분포**의 시공간적 상관성을 분석합니다.")
st.divider()

# 3. 사이드바
with st.sidebar:
    st.header("📝 지표 정의")
    with st.expander("📌 SPEI란?", expanded=True):
        st.markdown("**Standardized Precipitation–Evapotranspiration Index**")
        st.caption("강수량(P)과 증발산량(PET)을 통합하여 '실질적 건조도'를 나타내는 지수")
    
    st.divider()
    st.subheader("🎨 지도 범례")
    st.info("🟦 **습윤 (Wet)** : 수분 과잉")
    st.error("🟥 **가뭄 (Dry)** : 수분 부족 (건조)")

# =========================================================
# 4. [핵심] 구조화된 분석 데이터베이스 (DB)
# =========================================================
# 단순 텍스트가 아니라 '민감도', '유형', '상세내용'으로 구조화함

def get_bird_report(bird_code, month):
    """
    종과 월을 입력받아 구조화된 분석 리포트(Dictionary)를 반환
    """
    report = {
        "sensitivity": "판단 보류",  # 민감도 (매우 높음, 높음, 낮음, 불명)
        "correlation": "분석 중",    # 상관성 (양의 상관, 음의 상관, 무상관)
        "summary": "데이터가 충분하지 않거나 분석 대상 기간이 아닙니다."
    }

    # 1. 괭이갈매기
    if bird_code == "bird1":
        if month in ["12", "01"]:
            report = {
                "sensitivity": "낮음 (Low)",
                "correlation": "약한 양의 상관",
                "summary": "대체로 SPEI가 높은(습윤) 시기에 분포가 많으나, 경향성이 뚜렷하지 않음."
            }
        elif month == "03":
            report = {
                "sensitivity": "매우 낮음 (Irregular)",
                "correlation": "무상관 (None)",
                "summary": "2023년 3월의 비이상적 급증 등 기후 외적 요인(먹이원 등)이 지배적임."
            }
        elif month == "10":
            report = {
                "sensitivity": "중간 (Medium)",
                "correlation": "특이 패턴",
                "summary": "2022, 2024년 10월에 높은 밀도를 보임."
            }

    # 2. 흰뺨검둥오리
    elif bird_code == "bird2":
        if month in ["01", "02"]:
            report = {
                "sensitivity": "낮음 (Resilient)",
                "correlation": "무상관 (None)",
                "summary": "SPEI 변동과 무관하게 전국적으로 고밀도를 유지함 (강한 환경 내성)."
            }
        elif month == "03":
            report = {
                "sensitivity": "중간 (Medium)",
                "correlation": "음의 상관 (Negative)",
                "summary": "건조할수록(SPEI 하락) 분포가 늘어나는 역상관 경향이 일부 관측됨."
            }
        elif month in ["11", "12"]:
            report = {
                "sensitivity": "낮음 (Low)",
                "correlation": "추세 의존 (Trend)",
                "summary": "기후보다는 연도별 개체수 자체의 자연 증가 추세가 뚜렷함."
            }

    # 3. 쇠백로 (핵심 지표종)
    elif bird_code == "bird3":
        if month == "01":
            report = {
                "sensitivity": "매우 높음 (Critical)",
                "correlation": "강한 양의 상관 (Positive)",
                "summary": "가뭄 시(SPEI 하락) 개체수가 급감하고 습윤 시 증가함. 가장 뚜렷한 기후 지표종."
            }
        elif month == "02":
            report = {
                "sensitivity": "높음 (High)",
                "correlation": "음의 상관 (Crowding)",
                "summary": "건조해짐에도 분포가 증가하는 역설적 패턴. 수자원 고갈에 따른 '밀집 효과'로 추정."
            }
        elif month in ["11", "12"]:
            report = {
                "sensitivity": "높음 (High)",
                "correlation": "양의 상관 (Positive)",
                "summary": "동계 진입 시 습윤한 환경을 선호하는 경향이 뚜렷함."
            }

    # 4. 쇠물닭
    elif bird_code == "bird4":
        if month == "01":
            report = {
                "sensitivity": "중간 (Medium)",
                "correlation": "양의 상관 (Positive)",
                "summary": "SPEI와 양의 상관성을 보이나, 2021년 기점의 개체수 증가폭이 더 큼."
            }
        elif month in ["10", "11", "12"]:
            report = {
                "sensitivity": "판단 불가 (N/A)",
                "correlation": "데이터 희소",
                "summary": "여름 철새 특성상 동계 데이터가 부족하여 상관성 판단 불가."
            }

    return report

# =========================================================
# 5. 영상 HTML 생성기 (동시 재생용)
# =========================================================
def get_video_html(file_path):
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{b64}" type="video/mp4"></video>'
    except: return None

# =========================================================
# 6. 개별 분석 화면 (리포트 UI 적용)
# =========================================================
def show_bird_analysis(bird_code, bird_name):
    st.markdown(f"### 📅 {bird_name} - 월별 정밀 분석")
    
    selected_month = st.radio(
        f"{bird_name} 월 선택:", ["01", "02", "03", "10", "11", "12"], 
        key=bird_code, horizontal=True
    )
    
    col1, col2 = st.columns([1.5, 1])
    video_file = f"{bird_code}_{selected_month}.mp4"
    
    with col1:
        if os.path.exists(video_file):
            st.video(video_file)
        else:
            st.info("⚠️ 영상 데이터 없음")

    with col2:
        # DB에서 리포트 가져오기
        report = get_bird_report(bird_code, selected_month)
        
        # 1. 메트릭 표시 (점수판처럼)
        m1, m2 = st.columns(2)
        m1.metric("기후 민감도", report['sensitivity'])
        m2.metric("상관 유형", report['correlation'])
        
        # 2. 상세 설명 박스
        st.success("📝 **분석 요약**")
        st.write(report['summary'])
        
        st.caption(f"Based on 2014-2024 {bird_name} Spatial Data")

# =========================================================
# 7. 비교 분석 화면
# =========================================================
def show_comparison():
    st.markdown("### ⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.caption("비교할 두 종을 선택하고 **[▶️ 동시 재생]** 버튼을 누르세요.")
    
    bird_map = {"괭이갈매기": "bird1", "흰뺨검둥오리": "bird2", "쇠백로": "bird3", "쇠물닭": "bird4"}
    
    c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1])
    with c1: left_name = st.selectbox("비교군 A (좌)", list(bird_map.keys()), index=2)
    with c2: right_name = st.selectbox("비교군 B (우)", list(bird_map.keys()), index=1)
    with c3: comp_month = st.select_slider("비교할 월(Month)", options=["01", "02", "03", "10", "11", "12"])
    with c4: 
        st.write("") 
        play_btn = st.button("▶️ 동시 재생 Start", type="primary")

    st.divider()

    left_code = bird_map[left_name]
    right_code = bird_map[right_name]
    file_left = f"{left_code}_{comp_month}.mp4"
    file_right = f"{right_code}_{comp_month}.mp4"

    if play_btn:
        if os.path.exists(file_left) and os.path.exists(file_right):
            html_left = get_video_html(file_left)
            html_right = get_video_html(file_right)
            
            # 리포트 가져오기
            report_l = get_bird_report(left_code, comp_month)
            report_r = get_bird_report(right_code, comp_month)

            col_l, col_r = st.columns(2)
            
            # 좌측 화면 구성
            with col_l:
                st.markdown(f"**🅰️ {left_name}**")
                if html_left: st.markdown(html_left, unsafe_allow_html=True)
                
                # 분석 결과 카드
                st.info(f"**민감도:** {report_l['sensitivity']}")
                st.caption(report_l['summary'])

            # 우측 화면 구성
            with col_r:
                st.markdown(f"**🅱️ {right_name}**")
                if html_right: st.markdown(html_right, unsafe_allow_html=True)
                
                # 분석 결과 카드
                st.info(f"**민감도:** {report_r['sensitivity']}")
                st.caption(report_r['summary'])
        else:
            st.error("❌ 영상 파일이 없습니다.")

# =========================================================
# 8. 실행
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. 괭이갈매기", "2. 흰뺨검둥오리", "3. 쇠백로", "4. 쇠물닭", "⚔️ 비교 분석"])

with tab1: show_bird_analysis("bird1", "괭이갈매기")
with tab2: show_bird_analysis("bird2", "흰뺨검둥오리")
with tab3: show_bird_analysis("bird3", "쇠백로")
with tab4: show_bird_analysis("bird4", "쇠물닭")
with tab5: show_comparison()
