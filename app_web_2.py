import streamlit as st
from supabase import create_client, Client
from datetime import datetime, date
import calendar
import os

# 페이지 설정
st.set_page_config(
    page_title="의료 학회 캘린더",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supabase 설정
@st.cache_resource
def init_supabase():
    try:
        # secrets.toml에서 Supabase 설정 가져오기
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
        
    except KeyError as e:
        st.error(f"🔧 secrets.toml 파일에서 {e} 설정을 찾을 수 없습니다.")
        st.code("""
# .streamlit/secrets.toml 파일에 다음 내용을 추가하세요:
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
        """)
        st.stop()
        
    except Exception as e:
        st.error(f"❌ Supabase 연결 실패: {e}")
        st.stop()

# 세련된 모던 파란색 UI/UX CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 전체 스타일 */
    .stApp {
        background: linear-gradient(135deg, #fafbfc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        padding: 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* 헤더 */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: white;
        text-align: center;
        padding: 3rem 2rem 2rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #5b21b6 100%);
        opacity: 0.9;
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }
    
    /* 연결 상태 표시 */
    .connection-status {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .connection-status.error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    /* 월 네비게이션 */
    .month-navigation {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.06);
        position: relative;
        overflow: hidden;
    }
    
    .month-navigation::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #8b5cf6);
        border-radius: 0 0 8px 8px;
    }
    
    .month-title {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* 캘린더 컨테이너 */
    .calendar-wrapper {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.08);
        margin-bottom: 2rem;
    }
    
    /* 사이드바 이벤트 카드 */
    .sidebar-section {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.06);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-title {
        background: linear-gradient(135deg, #667eea, #764ba2, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.08);
        position: relative;
    }
    
    .sidebar-title::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #8b5cf6);
        border-radius: 2px;
    }
    
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #faf9ff 100%);
        border: 1px solid rgba(102, 126, 234, 0.08);
        border-left: 4px solid #667eea;
        border-radius: 20px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.06);
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8b5cf6 100%);
        transition: width 0.4s ease;
        border-radius: 0 8px 8px 0;
    }
    
    .event-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
        border-left-color: #764ba2;
        border-radius: 24px;
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
    }
    
    .event-card:hover::before {
        width: 8px;
        border-radius: 0 12px 12px 0;
    }
    
    .event-card-title {
        color: #1e293b;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }
    
    .event-card-date {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .event-card-location {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        line-height: 1.4;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .event-card-department {
        background: linear-gradient(135deg, #e2e8f0 0%, #f1f5f9 100%);
        color: #475569;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(102, 126, 234, 0.15);
        backdrop-filter: blur(10px);
    }
    
    .deadline-section {
        margin-top: 1.2rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(102, 126, 234, 0.08);
    }
    
    .deadline-item {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #374151;
        padding: 0.7rem 1rem;
        border-radius: 16px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        border-left: 3px solid rgba(102, 126, 234, 0.15);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.04);
    }
    
    .deadline-item.urgent {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #dc2626;
        border-left-color: #dc2626;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.15);
    }
    
    /* 지난 마감일 스타일 */
    .deadline-item.expired {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        color: #6b7280;
        border-left-color: #9ca3af;
        box-shadow: 0 2px 8px rgba(156, 163, 175, 0.1);
        text-decoration: line-through;
        opacity: 0.7;
    }
    
    .deadline-item.expired::before {
        content: '⏰ ';
        opacity: 0.5;
    }
    
    /* 빈 상태 */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #047857;
        background: linear-gradient(135deg, #ffffff 0%, #f6fdf6 100%);
        border-radius: 24px;
        border: 2px dashed rgba(74, 222, 128, 0.15);
        box-shadow: 0 4px 20px rgba(74, 222, 128, 0.04);
    }
    
    .empty-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
        background: linear-gradient(135deg, #4ade80, #a3e635);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 새로고침 버튼 */
    .refresh-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .refresh-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드 (Supabase에서)
@st.cache_data(ttl=300)  # 5분 캐시
def load_conferences_from_supabase(year, month):
    try:
        supabase = init_supabase()
        
        # 해당 월의 컨퍼런스 조회
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        # Supabase에서 데이터 조회
        response = (supabase.table('conferences')
                   .select("*")
                   .lt('start_date', end_date)
                   .gte('end_date', start_date)
                   .order('start_date')
                   .execute())
        
        conferences = []
        for row in response.data:
            conferences.append({
                'id': row['id'],
                'title': row['title'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'abstract_deadline': row.get('abstract_deadline'),
                'registration_deadline': row.get('registration_deadline'),
                'location': row.get('location'),
                'department': row.get('department'),
                'description': row.get('description')
            })
        
        return conferences, None
        
    except Exception as e:
        return [], str(e)

# 마감일 상태 확인 함수
def get_deadline_status(deadline_str):
    """마감일 상태를 반환 (expired, urgent, normal)"""
    if not deadline_str:
        return "normal"
    
    try:
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_left = (deadline_date - today).days
        
        if days_left < 0:  # 지난 날짜
            return "expired"
        elif days_left <= 30:  # 30일 이내
            return "urgent"
        else:
            return "normal"
    except:
        return "normal"

# 날짜 포맷팅
def format_date(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y년 %m월 %d일")
    except:
        return date_str

def format_date_short(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%m/%d")
    except:
        return date_str

# 간단한 캘린더 렌더링
def render_simple_calendar(year, month, conferences):
    cal = calendar.monthcalendar(year, month)
    today = datetime.now().date()
    
    st.markdown('<div class="calendar-wrapper">', unsafe_allow_html=True)
    
    # 요일 헤더
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    cols = st.columns(7)
    for i, day in enumerate(weekdays):
        with cols[i]:
            color = "#ef4444" if i == 6 else "#667eea" if i == 5 else "#374151"
            st.markdown(f'<div style="background: #f8fafc; padding: 1rem; text-align: center; font-weight: 600; color: {color}; border-bottom: 1px solid rgba(102, 126, 234, 0.08);">{day}</div>', unsafe_allow_html=True)
    
    # 날짜별 표시
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown('<div style="background: #fafbfc; min-height: 100px; border-bottom: 1px solid rgba(102, 126, 234, 0.04); border-right: 1px solid rgba(102, 126, 234, 0.04);"></div>', unsafe_allow_html=True)
                else:
                    # 오늘 날짜 확인
                    current_date = date(year, month, day)
                    is_today = current_date == today
                    is_weekend = i >= 5
                    
                    # 배경색 설정
                    bg_color = "#f3f4f6" if is_today else "white"
                    text_color = "#374151" if is_today else "#667eea" if is_weekend else "#374151"
                    if i == 6:  # 일요일
                        text_color = "#ef4444"
                    
                    # 해당 날짜의 학회 찾기
                    day_date = f"{year}-{month:02d}-{day:02d}"
                    day_conferences = [conf for conf in conferences 
                                     if conf['start_date'] <= day_date <= conf['end_date']]
                    
                    # 이벤트 표시
                    events_html = ""
                    colors = ["#667eea", "#764ba2", "#8b5cf6", "#a855f7"]
                    for idx, conf in enumerate(day_conferences[:4]):
                        title = conf['title'][:12] + "..." if len(conf['title']) > 12 else conf['title']
                        color = colors[idx % 4]
                        events_html += f'<div style="background: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; margin: 1px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{conf["title"]}">{title}</div>'
                    
                    if len(day_conferences) > 4:
                        remaining = len(day_conferences) - 4
                        events_html += f'<div style="color: #6b7280; font-size: 0.65rem; text-align: center; padding: 1px;">+{remaining}개 더</div>'
                    
                    cell_html = f'''
                    <div style="background: {bg_color}; min-height: 100px; padding: 8px; border-bottom: 1px solid rgba(102, 126, 234, 0.08); border-right: 1px solid rgba(102, 126, 234, 0.08); transition: all 0.2s ease;">
                        <div style="font-size: 0.95rem; font-weight: 600; color: {text_color}; margin-bottom: 4px;">{day}</div>
                        {events_html}
                    </div>
                    '''
                    
                    st.markdown(cell_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 앱
def main():
    # 헤더
    st.markdown('''
    <div class="main-header">
        <div class="header-content">
            <div class="header-title">의료 학회 캘린더</div>
            <div class="header-subtitle">Medical Society Calendar - Powered by Supabase</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 연결 상태 확인
    try:
        supabase = init_supabase()
        # 간단한 연결 테스트
        test_response = supabase.table('conferences').select("count", count="exact").execute()
        total_count = test_response.count
        st.markdown(f'<div class="connection-status">✅ Supabase 연결됨 (총 {total_count}개 학회)</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="connection-status error">❌ Supabase 연결 오류: {str(e)}</div>', unsafe_allow_html=True)
        return
    
    # 사이드바
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">기간 선택</div>', unsafe_allow_html=True)
        
        # 새로고침 버튼
        if st.button("🔄 데이터 새로고침", help="Supabase에서 최신 데이터를 불러옵니다"):
            st.cache_data.clear()
            st.rerun()
        
        # 연도/월 선택
        year_options = list(range(2025, 2027))
        selected_year = st.selectbox("연도", year_options, index=0)
        
        if selected_year == 2025:
            month_options = list(range(9, 13))  # 8월부터 12월
            month_names = ['9월', '10월', '11월', '12월']
            default_idx = 1 if datetime.now().month >= 10 else 0
            selected_month_idx = st.selectbox("월", range(len(month_names)), 
                                            format_func=lambda x: month_names[x], index=default_idx)
            selected_month = month_options[selected_month_idx]
        else:
            month_options = list(range(1, 13))
            month_names = [f'{i}월' for i in month_options]
            selected_month_idx = st.selectbox("월", range(len(month_names)), 
                                            format_func=lambda x: month_names[x], index=2)
            selected_month = month_options[selected_month_idx]
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 학회 로드
    conferences, error = load_conferences_from_supabase(selected_year, selected_month)
    
    if error:
        st.error(f"❌ 데이터 로드 실패: {error}")
        return
    
    # 부서 필터
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">부서 필터</div>', unsafe_allow_html=True)
        
        all_departments = list(set([c['department'] for c in conferences if c['department']]))
        if not all_departments:
            all_departments = ["정형외과", "신경외과"]
        
        selected_departments = st.multiselect(
            "부서 선택", all_departments, default=all_departments
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 필터링
    if conferences:
        filtered_conferences = [
            c for c in conferences 
            if c['department'] in selected_departments
        ]
    else:
        filtered_conferences = []
    
    # 메인 레이아웃
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 월 네비게이션
        st.markdown(f'''
        <div class="month-navigation">
            <div class="month-title">{selected_year}년 {selected_month}월</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 간단한 캘린더 렌더링
        render_simple_calendar(selected_year, selected_month, filtered_conferences)
    
    with col2:
        if filtered_conferences:
            # 캐러셀 인덱스 상태값 준비
            if "conf_idx" not in st.session_state:
                st.session_state.conf_idx = 0

            n = len(filtered_conferences)
            # 현재 인덱스 정규화 (필터 바뀌었을 때 범위 밖 방지)
            st.session_state.conf_idx %= max(n, 1)

            # 헤더 + 네비게이션
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title">이번 달 학회</div>', unsafe_allow_html=True)

            nav1, nav2, nav3 = st.columns([1, 4, 1])
            with nav1:
                # 이전
                if st.button("◀", key="prev_conf", help="이전 학회"):
                    st.session_state.conf_idx = (st.session_state.conf_idx - 1) % n
            with nav3:
                # 다음
                if st.button("▶", key="next_conf", help="다음 학회"):
                    st.session_state.conf_idx = (st.session_state.conf_idx + 1) % n
            with nav2:
                st.markdown(
                    f'<div style="text-align:center; color:#64748b; font-weight:600; '
                    f'padding-top:6px;">{st.session_state.conf_idx + 1} / {n}</div>',
                    unsafe_allow_html=True
                )

            # 현재 선택된 학회 1건만 표시
            conf = filtered_conferences[st.session_state.conf_idx]

            # 마감 뱃지 만들기 (개선된 버전)
            deadlines_html = ""
            
            # 초록 마감
            if conf.get('abstract_deadline'):
                status = get_deadline_status(conf['abstract_deadline'])
                deadline_class = f"deadline-item {status}"
                
                if status == "expired":
                    deadlines_html += f'<div class="{deadline_class}">📝 초록접수 마감: {format_date_short(conf["abstract_deadline"])} (마감됨)</div>'
                elif status == "urgent":
                    try:
                        deadline_date = datetime.strptime(conf['abstract_deadline'], "%Y-%m-%d").date()
                        days_left = (deadline_date - datetime.now().date()).days
                        deadlines_html += f'<div class="{deadline_class}">📝 초록접수 마감: {format_date_short(conf["abstract_deadline"])} (D-{days_left})</div>'
                    except:
                        deadlines_html += f'<div class="{deadline_class}">📝 초록접수 마감: {format_date_short(conf["abstract_deadline"])}</div>'
                else:
                    deadlines_html += f'<div class="{deadline_class}">📝 초록접수 마감: {format_date_short(conf["abstract_deadline"])}</div>'
            
            # 등록 마감
            if conf.get('registration_deadline'):
                status = get_deadline_status(conf['registration_deadline'])
                deadline_class = f"deadline-item {status}"
                
                if status == "expired":
                    deadlines_html += f'<div class="{deadline_class}">✅ 사전접수 마감: {format_date_short(conf["registration_deadline"])} (마감됨)</div>'
                elif status == "urgent":
                    try:
                        deadline_date = datetime.strptime(conf['registration_deadline'], "%Y-%m-%d").date()
                        days_left = (deadline_date - datetime.now().date()).days
                        deadlines_html += f'<div class="{deadline_class}">✅ 사전접수 마감: {format_date_short(conf["registration_deadline"])} (D-{days_left})</div>'
                    except:
                        deadlines_html += f'<div class="{deadline_class}">✅ 사전접수 마감: {format_date_short(conf["registration_deadline"])}</div>'
                else:
                    deadlines_html += f'<div class="{deadline_class}">✅ 사전접수 마감: {format_date_short(conf["registration_deadline"])}</div>'

            deadlines_section = f'<div class="deadline-section">{deadlines_html}</div>' if deadlines_html else ""

            # 날짜 범위
            date_range = format_date(conf['start_date'])
            if conf['start_date'] != conf['end_date']:
                date_range += ' ~ ' + format_date(conf['end_date'])

            # 카드 렌더
            st.markdown(f'''
            <div class="event-card">
                <div class="event-card-title">{conf['title']}</div>
                <div class="event-card-date"><span>{date_range}</span></div>
                <div class="event-card-location"><span>{conf.get('location') or '장소 미정'}</span></div>
                <div class="event-card-department">{conf.get('department') or '부서 미정'}</div>
                {deadlines_section}
            </div>
            ''', unsafe_allow_html=True)

            # Description 토글
            with st.expander("Description", expanded=False):
                description = conf.get('description', '') or ''
                st.write(f"**설명:** {description}")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            # 없음 상태
            st.markdown('''
            <div class="empty-state">
                <div class="empty-icon">🗓️</div>
                이번 달 표시할 학회가 없습니다.
            </div>
            ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()