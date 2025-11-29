import streamlit as st
import os
import base64

# -----------------------------------------------------------------------------
# 1. 페이지 설정 (무조건 맨 윗줄)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="조류 분포 & SPEI 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. 제목 및 사이드바
# -----------------------------------------------------------------------------
st.title("🦅 기후 변화(SPEI)와 조류 서식지 분포 상관관계 분석")
st.markdown("이 대시보드는 **2014~2024년** 데이터를 기반으로 **기후 가뭄 지수(SPEI)**와 **철새 서식지 분포**의 시공간적 상관성을 분석합니다.")
st.divider()

with st.sidebar:
    st.header("📝 지표 정의")
    with st.expander("📌 SPEI란?", expanded=True):
        st.markdown("**Standardized Precipitation–Evapotranspiration Index**")
        st.caption("강수량(P)과 증발산량(PET)을 통합하여 '실질적 건조도'를 나타내는 지수")
    
    st.divider()
    st.subheader("🎨 지도 범례")
    st.info("🟦 **습윤 (Wet)** : 수분 과잉")
    st.error("🟥 **가뭄 (Dry)** : 수분 부족")

# -----------------------------------------------------------------------------
# 3. 분석 데이터 (DB) - 사용자 분석 내용 탑재
# -----------------------------------------------------------------------------
def get_bird_report(bird_code, month):
    # 기본값
    report = {
        "sensitivity": "분석 중",
        "correlation": "판단 보류",
        "summary": "해당 시기의 특이 사항이 관측되지 않았습니다."
    }

    # 1. 괭이갈매기
    if bird_code == "bird1":
        if month in ["12", "01"]:
            report = {"sensitivity": "낮음", "correlation": "약한 양의 상관", 
                      "summary": "대체로 SPEI가 높은(습윤) 시기에 분포가 많으나, 경향성이 뚜렷하지 않음."}
        elif month == "03":
            report = {"sensitivity": "매우 낮음", "correlation": "무상관", 
                      "summary": "2023년 3월의 비이상적 급증 등 기후 외적 요인(먹이원 등)이 지배적임."}
        elif month == "10":
            report = {"sensitivity": "중간", "correlation": "특이 패턴", 
                      "summary": "2022, 2024년 10월에 높은 밀도를 보임."}

    # 2. 흰뺨검둥오리
    elif bird_code == "bird2":
        if month in ["01", "02"]:
            report = {"sensitivity": "낮음 (내성종)", "correlation": "무상관", 
                      "summary": "SPEI 변동과 무관하게 전국적으로 고밀도를 유지함 (강한 환경 내성)."}
        elif month == "03":
            report = {"sensitivity": "중간", "correlation": "음의 상관", 
                      "summary": "건조할수록(SPEI 하락) 분포가 늘어나는 역상관 경향이 일부 관측됨."}
        elif month in ["11", "12"]:
            report = {"sensitivity": "낮음", "correlation": "추세 의존", 
                      "summary": "기후보다는 연도별 개체수 자체의 자연 증가 추세가 뚜렷함."}

    # 3. 쇠백로
    elif bird_code == "bird3":
        if month == "01":
            report = {"sensitivity": "매우 높음", "correlation": "강한 양의 상관", 
                      "summary": "가뭄 시(SPEI 하락) 개체수가 급감하고 습윤 시 증가함. 가장 뚜렷한 기후 지표종."}
        elif month == "02":
            report = {"sensitivity": "높음", "correlation": "음의 상관 (밀집)", 
                      "summary": "건조해짐에도 분포가 증가하는 역설적 패턴. 수자원 고갈에 따른 '밀집 효과'로 추정."}
        elif month in ["11", "12"]:
            report = {"sensitivity": "높음", "correlation": "양의 상관", 
                      "summary": "동계 진입 시 습윤한 환경을 선호하는 경향이 뚜렷함."}

    # 4. 쇠물닭
    elif bird_code == "bird4":
        if month == "01":
            report = {"sensitivity": "중간", "correlation": "양의 상관", 
                      "summary": "SPEI와 양의 상관성을 보이나, 2021년 기점의 개체수 증가폭이 더 큼."}
        elif month in ["10", "11", "12"]:
            report = {"sensitivity": "판단 불가", "correlation": "데이터 희소", 
                      "summary": "여름 철새 특성상 동계 데이터가 부족하여 상관성 판단 불가."}

    return report

# -----------------------------------------------------------------------------
# 4. 동시 재생 HTML 생성 함수 (에러 방지)
# -----------------------------------------------------------------------------
def get_dual_video_html(path1, path2):
    try:
        # 파일1 읽기
        with open(path1, "rb") as f:
            b64_1 = base64.b64encode(f.read()).decode()
        # 파일2 읽기
        with open(path2, "rb") as f:
            b64_2 = base64.b64encode(f.read()).decode()
            
        # HTML 생성 (Flexbox 레이아웃)
        return f"""
        <div style="display: flex; justify-content: space-between; gap: 20px;">
            <div style="width: 48%;">
                <video width="100%" autoplay loop muted playsinline style="border: 2px solid #eee; border-radius: 8px;">
                    <source src="data:video/mp4;base64,{b64_1}" type="video/mp4">
                </video>
            </div>
            <div style="width: 48%;">
                <video width="100%" autoplay loop muted playsinline style="border: 2px solid #eee; border-radius: 8px;">
                    <source src="data:video/mp4;base64,{b64_2}" type="video/mp4">
                </video>
            </div>
        </div>
        """
    except Exception:
        return None

# -----------------------------------------------------------------------------
# 5. 화면 렌더링 함수
# -----------------------------------------------------------------------------
def show_individual_tab(bird_code, bird_name):
    st.subheader(f"📅 {bird_name} - 월별 분석")
    sel_month = st.radio(f"{bird_name} 월 선택", ["01", "02", "03", "10", "11", "12"], key=bird_code, horizontal=True)
    
    col1, col2 = st.columns([1.5, 1])
    file_path = f"{bird_code}_{sel_month}.mp4"
    
    with col1:
        if os.path.exists(file_path):
            st.video(file_path)
        else:
            st.warning("⚠️ 영상 파일이 없습니다.")
            
    with col2:
        rep = get_bird_report(bird_code, sel_month)
        st.info(f"**민감도:** {rep['sensitivity']}")
        st.write(f"**유형:** {rep['correlation']}")
        st.success(f"💡 {rep['summary']}")

def show_comparison_tab():
    st.subheader("⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.caption("비교할 두 종을 선택하고 **[▶️ 동시 재생]** 버튼을 누르세요.")
    
    b_map = {"괭이갈매기": "bird1", "흰뺨검둥오리": "bird2", "쇠백로": "bird3", "쇠물닭": "bird4"}
    
    c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1])
    with c1: l_name = st.selectbox("좌측 (A)", list(b_map.keys()), index=2)
    with c2: r_name = st.selectbox("우측 (B)", list(b_map.keys()), index=1)
    with c3: month = st.select_slider("비교 월", options=["01", "02", "03", "10", "11", "12"])
    with c4: 
        st.write("")
        btn = st.button("▶️ 동시 재생", type="primary")
    
    st.divider()
    
    if btn:
        f1 = f"{b_map[l_name]}_{month}.mp4"
        f2 = f"{b_map[r_name]}_{month}.mp4"
        
        if os.path.exists(f1) and os.path.exists(f2):
            html = get_dual_video_html(f1, f2)
            if html:
                st.markdown(html, unsafe_allow_html=True)
                
                # 하단 분석 텍스트
                r1 = get_bird_report(b_map[l_name], month)
                r2 = get_bird_report(b_map[r_name], month)
                
                t1, t2 = st.columns(2)
                with t1: st.info(f"**🅰️ {l_name}:** {r1['sensitivity']}")
                with t2: st.info(f"**🅱️ {r_name}:** {r2['sensitivity']}")
            else:
                st.error("영상 변환 중 오류 발생")
        else:
            st.error("❌ 선택한 월의 영상 파일이 서버에 없습니다.")

# -----------------------------------------------------------------------------
# 6. 메인 실행 (탭 구성)
# -----------------------------------------------------------------------------
tabs = st.tabs(["1. 괭이갈매기", "2. 흰뺨검둥오리", "3. 쇠백로", "4. 쇠물닭", "⚔️ 비교 분석"])

with tabs[0]: show_individual_tab("bird1", "괭이갈매기")
with tabs[1]: show_individual_tab("bird2", "흰뺨검둥오리")
with tabs[2]: show_individual_tab("bird3", "쇠백로")
with tabs[3]: show_individual_tab("bird4", "쇠물닭")
with tabs[4]: show_comparison_tab()
