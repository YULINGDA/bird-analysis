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
# 4. 분석 결과 텍스트 (사용자 데이터 완벽 반영)
# =========================================================
def get_analysis_text(bird_code, month):
    # 1. 괭이갈매기
    if bird_code == "bird1":
        if month in ["12", "01"]:
            return "**[동계]** 대체로 SPEI가 높은(습윤) 12월과 1월에서 가장 많은 개체수 분포를 보입니다."
        elif month == "10":
            return "**[추계]** 2022년과 2024년의 10월에 특히 많은 분포를 보였습니다."
        elif month == "03":
            return "**[특이점]** 23년 3월 이상 급증. SPEI와의 선형적 상관관계는 낮다고 판단됩니다."
        return "특이 사항 없음"

    # 2. 흰뺨검둥오리
    elif bird_code == "bird2":
        if month in ["01", "02"]:
            return "**[동계]** SPEI와 상관없이 전국적으로 많은 수가 분포하며, 연도가 지나도 큰 변화가 없습니다."
        elif month == "03":
            return "**[춘계]** 1, 2월에 비해 개체수가 적으며, 건조할수록 분포가 많아지는 경향이 일부 관측됩니다."
        elif month == "10":
            return "**[추계]** 대체적으로 SPEI 수치와 상관없이 고르게 분포합니다."
        elif month in ["11", "12"]:
            return "**[추세]** 가장 많은 개체수를 보이며, 연도가 지남에 따라 SPEI와 관계없이 증가하는 추세입니다."
        return "특이 사항 없음"

    # 3. 쇠백로
    elif bird_code == "bird3":
        if month == "01":
            return "**[핵심]** 22년 제외 SPEI가 높을수록(습윤) 개체수가 많음. 4종 중 변화가 가장 선명합니다."
        elif month == "02":
            return "**[특이점]** 21년부터 건조해졌으나 오히려 개체수 분포가 더 많이 측정되는 패턴을 보입니다."
        elif month in ["03", "10"]:
            return "**[이동기]** SPEI 패턴을 따르지 않고 분포가 불규칙하게 변화합니다."
        elif month in ["11", "12"]:
            return "**[동계 진입]** SPEI가 높을 때(습윤) 분포가 더 많은 경향을 보입니다."
        return "특이 사항 없음"

    # 4. 쇠물닭
    elif bird_code == "bird4":
        if month == "01":
            return "**[핵심]** SPEI와 양의 상관관계. 2021년을 기점으로 개체수가 뚜렷하게 증가했습니다."
        elif month in ["02", "03"]:
            return "**[초봄]** SPEI 변화와 관계없이 개체수 및 분포 변화가 거의 없습니다."
        elif month in ["10", "11", "12"]:
            return "**[한계]** 여름 철새 특성상 해당 시기에는 개체수가 거의 측정되지 않았습니다."
        return "특이 사항 없음"
    
    return "분석 데이터 없음"

# =========================================================
# 5. [핵심] 동시 재생을 위한 HTML 코드 생성기
# =========================================================
def render_dual_video(file1, file2, title1, title2):
    """
    두 영상을 하나의 HTML 블록으로 만들어 동시에 재생시킴
    """
    try:
        # 파일 읽어서 base64 변환
        with open(file1, "rb") as f1:
            b64_1 = base64.b64encode(f1.read()).decode()
        with open(file2, "rb") as f2:
            b64_2 = base64.b64encode(f2.read()).decode()
            
        # HTML 코드 (Flexbox 사용)
        html = f"""
        <div style="display: flex; justify-content: space-between; gap: 20px;">
            <div style="width: 48%;">
                <h4 style="text-align: center; margin: 0px;">🅰️ {title1}</h4>
                <video width="100%" autoplay loop muted playsinline style="border: 2px solid #ddd; border-radius: 5px;">
                    <source src="data:video/mp4;base64,{b64_1}" type="video/mp4">
                </video>
            </div>
            <div style="width: 48%;">
                <h4 style="text-align: center; margin: 0px;">🅱️ {title2}</h4>
                <video width="100%" autoplay loop muted playsinline style="border: 2px solid #ddd; border-radius: 5px;">
                    <source src="data:video/mp4;base64,{b64_2}" type="video/mp4">
                </video>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        return True
    except Exception as e:
        return False

# =========================================================
# 6. 개별 보기 함수
# =========================================================
def show_bird_analysis(bird_code, bird_name):
    st.markdown(f"### 📅 {bird_name} - 월별 변화")
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
            st.video(video_file) # 개별 보기는 일반 플레이어
        else:
            st.info("⚠️ 영상 파일이 없습니다.")
    with col2:
        st.success(f"📊 {selected_month}월 상세 분석")
        st.info(get_analysis_text(bird_code, selected_month))

# =========================================================
# 7. 비교 분석 화면 (동시 재생 버튼 포함)
# =========================================================
def show_comparison():
    st.markdown("### ⚔️ 종별 교차 비교 (Cross-Analysis)")
    st.caption("두 종을 선택하고 **[▶️ 동시 재생]** 버튼을 누르면 영상이 함께 시작됩니다.")
    
    bird_map = {
        "괭이갈매기": "bird1",
        "흰뺨검둥오리": "bird2",
        "쇠백로": "bird3",
        "쇠물닭": "bird4"
    }
    
    c1, c2, c3, c4 = st.columns([1, 1, 1.5, 1])
    with c1:
        left_name = st.selectbox("비교군 A (좌측)", list(bird_map.keys()), index=2)
    with c2:
        right_name = st.selectbox("비교군 B (우측)", list(bird_map.keys()), index=1)
    with c3:
        comp_month = st.select_slider("비교할 월(Month)", options=["01", "02", "03", "10", "11", "12"])
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
            # 1. 동시 영상 재생 (HTML 방식)
            success = render_dual_video(file_left, file_right, left_name, right_name)
            
            if success:
                st.write("") # 여백
                # 2. 하단 설명 텍스트
                t1, t2 = st.columns(2)
                with t1:
                    st.caption(get_analysis_text(left_code, comp_month))
                with t2:
                    st.caption(get_analysis_text(right_code, comp_month))
            else:
                st.error("영상 로딩 중 오류가 발생했습니다.")
        else:
            st.error("❌ 선택한 월의 영상 파일이 서버에 없습니다.")
    else:
        st.info("👆 위 옵션을 선택하고 버튼을 눌러주세요.")

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
