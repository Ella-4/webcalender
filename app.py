import streamlit as st
import sqlite3
from datetime import datetime, date
import calendar

# 페이지 설정
st.set_page_config(
    page_title="의료 학회 캘린더",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세련된 모던 파란색 UI/UX CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 전체 스타일 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
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
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%);
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
    
    /* 월 네비게이션 */
    .month-navigation {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.08);
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
        background: linear-gradient(90deg, #3b82f6, #1d4ed8, #6366f1);
        border-radius: 0 0 8px 8px;
    }
    
    .month-title {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
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
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    /* 사이드바 이벤트 카드 */
    .sidebar-section {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.08);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-title {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.1);
        position: relative;
    }
    
    .sidebar-title::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        border-radius: 2px;
    }
    
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 20px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.08);
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #6366f1 100%);
        transition: width 0.4s ease;
        border-radius: 0 8px 8px 0;
    }
    
    .event-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(59, 130, 246, 0.2);
        border-left-color: #1d4ed8;
        border-radius: 24px;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
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
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #6366f1 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .deadline-section {
        margin-top: 1.2rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    .deadline-item {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #64748b;
        padding: 0.7rem 1rem;
        border-radius: 16px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        border-left: 3px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.05);
    }
    
    .deadline-item.urgent {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #dc2626;
        border-left-color: #dc2626;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.15);
    }
    
    /* 빈 상태 */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #64748b;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        border: 2px dashed rgba(59, 130, 246, 0.2);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.05);
    }
    
    .empty-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Streamlit 커스터마이징 */
    .stSelectbox > div > div {
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.05);
    }
    
    .stMultiSelect > div > div {
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.05);
    }
    
    /* 사이드바 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* 반응형 */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        
        .month-title {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 데이터베이스 초기화
@st.cache_resource
def init_database():
    conn = sqlite3.connect('conferences.db', check_same_thread=False)
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conferences (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            abstract_deadline TEXT,
            registration_deadline TEXT,
            location TEXT,
            department TEXT,
            description TEXT
        )
    ''')
    
    # 기존 데이터 삭제 후 새로 추가
    conn.execute('DELETE FROM conferences')
    
    # 정확한 데이터 추가
    sample_data = [
        ("대한연골 및 골관절염학회", "2025-10-23", "2025-10-24", "2025-08-24", "2025-10-12", 
         "엠배서더 서울 풀만, 2층 그랜드볼룸", "정형외과", "연골 및 골관절염 관련 최신 연구 발표 및 토론"),
        ("대한수부외과학회 추계학술대회", "2025-11-01", "2025-11-01", "2025-08-31", "", 
         "연세대학교 세브란스병원 6층 은명대강당 및 종합관 331호, 337호 강의실", "정형외과", "수부외과 분야의 최신 기술과 치료법 공유"),
        ("대한정형외과 스포츠의학회 ISSS 2026", "2026-03-08", "2026-03-13", "2025-09-01", "", 
         "MONA 용평리조트, 평창, 대한민국", "정형외과", "국제 스포츠의학 심포지엄 - 스포츠 손상 예방과 치료")
    ]
    
    conn.executemany('''
        INSERT INTO conferences 
        (title, start_date, end_date, abstract_deadline, registration_deadline, 
         location, department, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)
    conn.commit()
    
    return conn

# 데이터 로드
def load_conferences(year, month):
    conn = init_database()
    
    # 해당 월의 컨퍼런스 조회
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    
    query = '''
        SELECT * FROM conferences 
        WHERE start_date < ? AND end_date >= ?
        ORDER BY start_date
    '''
    
    cursor = conn.execute(query, (end_date, start_date))
    conferences = []
    
    for row in cursor.fetchall():
        conferences.append({
            'id': row[0],
            'title': row[1],
            'start_date': row[2],
            'end_date': row[3],
            'abstract_deadline': row[4],
            'registration_deadline': row[5],
            'location': row[6],
            'department': row[7],
            'description': row[8]
        })
    
    return conferences

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
            color = "#ef4444" if i == 6 else "#3b82f6" if i == 5 else "#374151"
            st.markdown(f'<div style="background: #f8fafc; padding: 1rem; text-align: center; font-weight: 600; color: {color}; border-bottom: 1px solid #e2e8f0;">{day}</div>', unsafe_allow_html=True)
    
    # 날짜별 표시
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown('<div style="background: #fafbfc; min-height: 100px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0;"></div>', unsafe_allow_html=True)
                else:
                    # 오늘 날짜 확인
                    current_date = date(year, month, day)
                    is_today = current_date == today
                    is_weekend = i >= 5
                    
                    # 배경색 설정
                    bg_color = "#dbeafe" if is_today else "white"
                    text_color = "#1e40af" if is_today else "#3b82f6" if is_weekend else "#374151"
                    if i == 6:  # 일요일
                        text_color = "#ef4444"
                    
                    # 해당 날짜의 학회 찾기
                    day_date = f"{year}-{month:02d}-{day:02d}"
                    day_conferences = [conf for conf in conferences 
                                     if conf['start_date'] <= day_date <= conf['end_date']]
                    
                    # 이벤트 표시
                    events_html = ""
                    colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"]
                    for idx, conf in enumerate(day_conferences[:4]):
                        title = conf['title'][:12] + "..." if len(conf['title']) > 12 else conf['title']
                        color = colors[idx % 4]
                        events_html += f'<div style="background: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; margin: 1px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{conf["title"]}">{title}</div>'
                    
                    if len(day_conferences) > 4:
                        remaining = len(day_conferences) - 4
                        events_html += f'<div style="color: #6b7280; font-size: 0.65rem; text-align: center; padding: 1px;">+{remaining}개 더</div>'
                    
                    cell_html = f'''
                    <div style="background: {bg_color}; min-height: 100px; padding: 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; transition: all 0.2s ease;">
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
            <div class="header-subtitle">Medical Society Calendar</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">기간 선택</div>', unsafe_allow_html=True)
        
        # 연도/월 선택
        year_options = list(range(2025, 2027))
        selected_year = st.selectbox("연도", year_options, index=0)
        
        if selected_year == 2025:
            month_options = list(range(8, 13))  # 8월부터 12월
            month_names = ['8월', '9월', '10월', '11월', '12월']
            default_idx = 2 if datetime.now().month >= 10 else 0
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
    conferences = load_conferences(selected_year, selected_month)
    
    # 부서 필터 - 항상 표시
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">부서 필터</div>', unsafe_allow_html=True)
        
        all_departments = ["정형외과", "신경외과"]  # 모든 가능한 부서
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
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title">이번 달 학회</div>', unsafe_allow_html=True)
            
            for conf in filtered_conferences:
                deadlines_html = ""
                
                if conf['abstract_deadline']:
                    try:
                        deadline_date = datetime.strptime(conf['abstract_deadline'], "%Y-%m-%d").date()
                        days_left = (deadline_date - datetime.now().date()).days
                        is_urgent = days_left <= 30 and days_left >= 0
                        deadline_class = "deadline-item urgent" if is_urgent else "deadline-item"
                        deadlines_html += f'<div class="{deadline_class}">📝 초록마감: {format_date_short(conf["abstract_deadline"])}</div>'
                    except:
                        pass
                
                if conf['registration_deadline']:
                    try:
                        deadline_date = datetime.strptime(conf['registration_deadline'], "%Y-%m-%d").date()
                        days_left = (deadline_date - datetime.now().date()).days
                        is_urgent = days_left <= 30 and days_left >= 0
                        deadline_class = "deadline-item urgent" if is_urgent else "deadline-item"
                        deadlines_html += f'<div class="{deadline_class}">✅ 등록마감: {format_date_short(conf["registration_deadline"])}</div>'
                    except:
                        pass
                
                if deadlines_html:
                    deadlines_section = f'<div class="deadline-section">{deadlines_html}</div>'
                else:
                    deadlines_section = ""
                
                # 날짜 범위 표시
                date_range = format_date(conf['start_date'])
                if conf['start_date'] != conf['end_date']:
                    date_range += ' ~ ' + format_date(conf['end_date'])
                
                st.markdown(f'''
                <div class="event-card">
                    <div class="event-card-title">{conf['title']}</div>
                    <div class="event-card-date">
                        <span>{date_range}</span>
                    </div>
                    <div class="event-card-location">
                        <span>{conf['location'] or '장소 미정'}</span>
                    </div>
                    <div class="event-card-department">{conf['department']}</div>
                    {deadlines_section}
                </div>
                ''', unsafe_allow_html=True)
                
                # 상세 정보
                with st.expander("상세 정보", expanded=False):
                    st.write(f"**설명:** {conf['description']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # 학회가 없을 때는 아무것도 표시하지 않음
            pass

if __name__ == "__main__":
    main()