"""
AI Timetable Generator - Main Streamlit Application
A comprehensive productivity app with AI-powered timetable generation
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Import custom modules
from auth import AuthManager, render_login_page, check_authentication, get_current_user, logout
from database import DatabaseManager
from ai_generator import AITimetableGenerator
from pdf_generator import PDFGenerator
from productivity import ProductivityTechniques

# Page configuration
st.set_page_config(
    page_title="AI Timetable Generator",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .schedule-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #28a745;
    }
    
    .schedule-item.work {
        border-left-color: #dc3545;
    }
    
    .schedule-item.break {
        border-left-color: #28a745;
    }
    
    .schedule-item.meal {
        border-left-color: #ffc107;
    }
    
    .schedule-item.exercise {
        border-left-color: #007bff;
    }
    
    .schedule-item.sleep {
        border-left-color: #6f42c1;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    .chat-message.user {
        background: #e3f2fd;
        margin-left: 20%;
    }
    
    .chat-message.assistant {
        background: #f3e5f5;
        margin-right: 20%;
    }
    
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .task-input-table {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .importance-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .importance-high {
        background: #ff6b6b;
        color: white;
    }
    
    .importance-medium {
        background: #ffd93d;
        color: #333;
    }
    
    .importance-low {
        background: #6bcb77;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize managers
@st.cache_resource
def init_managers():
    """Initialize all managers"""
    return {
        'auth': AuthManager(),
        'db': DatabaseManager(),
        'ai': AITimetableGenerator(),
        'pdf': PDFGenerator(),
        'productivity': ProductivityTechniques()
    }

def render_sidebar():
    """Render sidebar with navigation and user info"""
    with st.sidebar:
        st.markdown("### 📅 AI Timetable Generator")
        st.markdown("---")
        
        if check_authentication():
            username = get_current_user()
            st.markdown(f"**Welcome, {username}!**")
            
            # Navigation
            st.markdown("### 🧭 Navigation")
            page = st.radio(
                "Go to",
                ["🏠 Dashboard", "📋 Create Timetable", "💬 AI Chat", "📊 History", "⚙️ Settings"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # Quick stats
            managers = init_managers()
            stats = managers['db'].get_user_stats(username)
            
            st.markdown("### 📈 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Timetables", stats['total_timetables'])
            with col2:
                st.metric("Tasks", stats['total_tasks'])
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                logout()
            
            return page
        
        return None

def render_dashboard():
    """Render main dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>📅 AI Timetable Generator</h1>
        <p>Your intelligent productivity companion powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    username = get_current_user()
    managers = init_managers()
    
    # Get user stats
    stats = managers['db'].get_user_stats(username)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>{}</h3>
            <p>Timetables</p>
        </div>
        """.format(stats['total_timetables']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>{}</h3>
            <p>Tasks</p>
        </div>
        """.format(stats['total_tasks']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>{}</h3>
            <p>Chat Messages</p>
        </div>
        """.format(stats['total_chat_messages']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯</h3>
            <p>Focus Mode</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Create New Timetable", use_container_width=True, type="primary"):
            st.session_state.page = "📋 Create Timetable"
            st.rerun()
    
    with col2:
        if st.button("💬 Chat with AI", use_container_width=True):
            st.session_state.page = "💬 AI Chat"
            st.rerun()
    
    with col3:
        if st.button("📊 View History", use_container_width=True):
            st.session_state.page = "📊 History"
            st.rerun()
    
    st.markdown("---")
    
    # Productivity techniques
    st.markdown("### 🛠️ Productivity Tools")
    managers['productivity'].render_all_techniques()
    
    st.markdown("---")
    
    # Recent timetables
    st.markdown("### 📋 Recent Timetables")
    timetables = managers['db'].get_user_timetables(username)
    
    if timetables:
        for tt in timetables[-3:]:
            with st.expander(f"📅 {tt.get('date', 'Unknown')} - {tt.get('day', 'Unknown')}"):
                st.write(f"**Created:** {tt.get('created_at', 'Unknown')[:10]}")
                
                if 'schedule' in tt:
                    for item in tt['schedule'][:5]:
                        st.write(f"• {item.get('time', '')}: {item.get('activity', '')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Download PDF", key=f"pdf_{tt.get('id')}"):
                        filepath = managers['pdf'].generate_timetable_pdf(tt, username)
                        if filepath:
                            with open(filepath, "rb") as f:
                                st.download_button(
                                    "Download PDF",
                                    f,
                                    file_name=os.path.basename(filepath),
                                    mime="application/pdf"
                                )
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{tt.get('id')}"):
                        managers['db'].delete_timetable(username, tt.get('id'))
                        st.rerun()
    else:
        st.info("No timetables yet. Create your first one!")

def render_create_timetable():
    """Render timetable creation page with enhanced task input"""
    st.markdown("### 📋 Create New Timetable")
    
    username = get_current_user()
    managers = init_managers()
    
    # Enhanced task input with task | time | columns format
    st.markdown("#### 📝 Add Your Tasks (Task | Time | Importance)")
    st.markdown("""
    <div class="task-input-table">
        <p>Enter tasks in the format: <strong>Task Name | Duration (minutes) | Importance (high/medium/low)</strong></p>
        <p>Example: <em>Complete project report | 120 | high</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    
    # Bulk task input
    with st.expander("📝 Bulk Task Input (Recommended)", expanded=True):
        task_input = st.text_area(
            "Enter tasks (one per line)",
            placeholder="Complete project report | 120 | high\nReview code changes | 60 | medium\nTeam meeting | 30 | high\nRead documentation | 45 | low",
            height=150
        )
        
        if st.button("➕ Add All Tasks", type="primary"):
            if task_input:
                lines = task_input.strip().split('\n')
                added_count = 0
                for line in lines:
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            task_name = parts[0].strip()
                            try:
                                duration = int(parts[1].strip())
                            except:
                                duration = 60
                            importance = parts[2].strip().lower()
                            if importance not in ['high', 'medium', 'low']:
                                importance = 'medium'
                            
                            st.session_state.tasks.append({
                                'name': task_name,
                                'duration': duration,
                                'priority': importance,
                                'importance': importance,
                                'description': ''
                            })
                            added_count += 1
                
                if added_count > 0:
                    st.success(f"✅ Added {added_count} tasks successfully!")
                else:
                    st.warning("No valid tasks found. Please use the format: Task | Duration | Importance")
    
    # Individual task input
    with st.expander("➕ Add Individual Task"):
        with st.form("individual_task_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                task_name = st.text_input("Task Name")
            
            with col2:
                task_duration = st.number_input("Duration (minutes)", min_value=15, max_value=480, value=60, step=15)
            
            with col3:
                task_importance = st.selectbox("Importance", ["high", "medium", "low"])
            
            task_description = st.text_area("Description (optional)")
            
            if st.form_submit_button("➕ Add Task"):
                if task_name:
                    st.session_state.tasks.append({
                        'name': task_name,
                        'duration': task_duration,
                        'priority': task_importance,
                        'importance': task_importance,
                        'description': task_description
                    })
                    st.success(f"Added: {task_name}")
    
    # Display tasks with importance badges
    if st.session_state.tasks:
        st.markdown("#### 📋 Your Tasks")
        
        # Sort tasks by importance
        importance_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: importance_order.get(x.get('importance', 'medium'), 1))
        
        for i, task in enumerate(sorted_tasks):
            importance = task.get('importance', 'medium')
            importance_class = f"importance-{importance}"
            
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{task['name']}**")
            
            with col2:
                st.write(f"{task['duration']} min")
            
            with col3:
                st.markdown(f'<span class="importance-badge {importance_class}">{importance.upper()}</span>', unsafe_allow_html=True)
            
            with col4:
                st.write(f"#{i+1}")
            
            with col5:
                if st.button("🗑️", key=f"remove_task_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()
        
        # Task summary
        total_time = sum(task['duration'] for task in st.session_state.tasks)
        high_tasks = sum(1 for task in st.session_state.tasks if task.get('importance') == 'high')
        medium_tasks = sum(1 for task in st.session_state.tasks if task.get('importance') == 'medium')
        low_tasks = sum(1 for task in st.session_state.tasks if task.get('importance') == 'low')
        
        st.markdown("---")
        st.markdown("#### 📊 Task Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(st.session_state.tasks))
        with col2:
            st.metric("Total Time", f"{total_time // 60}h {total_time % 60}m")
        with col3:
            st.metric("High Priority", high_tasks)
        with col4:
            st.metric("Medium/Low", f"{medium_tasks}/{low_tasks}")
    
    st.markdown("---")
    
    # Sleep cycle integration
    st.markdown("#### 😴 Sleep Cycle Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wake_time = st.time_input("Wake Up Time", value=datetime.strptime("06:00", "%H:%M").time())
    
    with col2:
        sleep_time = st.time_input("Sleep Time", value=datetime.strptime("22:00", "%H:%M").time())
    
    # Calculate optimal bedtime
    if st.button("🌙 Calculate Optimal Bedtime"):
        bedtimes = managers['productivity'].sleep_optimizer.calculate_optimal_bedtime(wake_time.strftime('%H:%M'))
        if bedtimes:
            st.success("🌙 Optimal Bedtimes Based on Sleep Cycles:")
            for bt in bedtimes:
                quality_emoji = "⭐" if bt['quality'] == 'Optimal' else "✅" if bt['quality'] == 'Good' else "⚠️"
                st.write(f"{quality_emoji} **{bt['time']}** - {bt['cycles']} cycles ({bt['hours']:.1f} hours) - {bt['quality']}")
    
    st.markdown("---")
    
    # Goals input
    st.markdown("#### 🎯 Set Your Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        short_term_goals = st.text_area(
            "Short-term Goals (this week)",
            placeholder="e.g., Complete project proposal, Exercise 3 times"
        )
        
        daily_goals = st.text_area(
            "Daily Goals",
            placeholder="e.g., Finish report, Call mom, Read 30 pages"
        )
    
    with col2:
        long_term_goals = st.text_area(
            "Long-term Goals (this month/year)",
            placeholder="e.g., Learn new skill, Save money, Improve health"
        )
        
        timetable_description = st.text_area(
            "Timetable Description (optional)",
            placeholder="Any specific requirements or preferences for your timetable"
        )
    
    st.markdown("---")
    
    # Preferences
    st.markdown("#### ⚙️ Preferences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        work_start = st.time_input("Work Start Time", value=datetime.strptime("09:00", "%H:%M").time())
    
    with col2:
        work_end = st.time_input("Work End Time", value=datetime.strptime("17:00", "%H:%M").time())
    
    with col3:
        break_preference = st.selectbox(
            "Break Preference",
            ["Pomodoro (25/5)", "50/10", "90/20", "Custom"]
        )
    
    focus_areas = st.multiselect(
        "Focus Areas",
        ["Work", "Study", "Exercise", "Creative", "Learning", "Personal", "Social"]
    )
    
    # Energy level tracking
    st.markdown("#### ⚡ Energy Level Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peak_energy_start = st.time_input("Peak Energy Start", value=datetime.strptime("09:00", "%H:%M").time())
    
    with col2:
        peak_energy_end = st.time_input("Peak Energy End", value=datetime.strptime("12:00", "%H:%M").time())
    
    st.markdown("---")
    
    # Generate timetable
    if st.button("🚀 Generate Timetable", type="primary", use_container_width=True):
        if not st.session_state.tasks:
            st.warning("Please add at least one task")
        else:
            with st.spinner("Generating your personalized timetable with AI..."):
                # Prepare data
                goals = {
                    'short_term': short_term_goals,
                    'long_term': long_term_goals,
                    'daily': daily_goals
                }
                
                preferences = {
                    'wake_up_time': wake_time.strftime('%H:%M'),
                    'sleep_time': sleep_time.strftime('%H:%M'),
                    'work_hours': f"{work_start.strftime('%H:%M')} - {work_end.strftime('%H:%M')}",
                    'break_preferences': break_preference,
                    'focus_areas': ', '.join(focus_areas) if focus_areas else 'General',
                    'peak_energy_start': peak_energy_start.strftime('%H:%M'),
                    'peak_energy_end': peak_energy_end.strftime('%H:%M')
                }
                
                # Generate timetable with importance-based scheduling
                timetable = managers['ai'].generate_timetable(
                    st.session_state.tasks,
                    goals,
                    preferences,
                    timetable_description
                )
                
                if timetable:
                    # Save to database
                    timetable_id = managers['db'].save_timetable(username, timetable)
                    
                    # Save tasks
                    for task in st.session_state.tasks:
                        managers['db'].save_task(username, task)
                    
                    # Save to history
                    managers['auth'].update_user_history(username, {
                        'type': 'timetable_created',
                        'timetable_id': timetable_id,
                        'tasks_count': len(st.session_state.tasks)
                    })
                    
                    st.success("✅ Timetable generated successfully!")
                    
                    # Display timetable
                    st.markdown("### 📅 Your Personalized Timetable")
                    
                    if 'motivation' in timetable:
                        st.info(f"💪 {timetable['motivation']}")
                    
                    # Display schedule with importance indicators
                    for item in timetable.get('schedule', []):
                        item_type = item.get('type', 'work')
                        priority = item.get('priority', 'medium')
                        
                        # Add priority indicator
                        priority_emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                        
                        st.markdown(f"""
                        <div class="schedule-item {item_type}">
                            <strong>{priority_emoji} {item.get('time', '')}</strong> - {item.get('activity', '')}
                            <br>
                            <small>{item.get('description', '')}</small>
                            {f"<br><em>💡 {item.get('tips', '')}</em>" if item.get('tips') else ""}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Summary with sleep cycle info
                    if 'summary' in timetable:
                        st.markdown("### 📊 Daily Summary")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Work Hours", f"{timetable['summary'].get('total_work_hours', 0)}h")
                        
                        with col2:
                            st.metric("Break Time", f"{timetable['summary'].get('total_break_time', 0)}h")
                        
                        with col3:
                            st.metric("Focus Sessions", timetable['summary'].get('focus_sessions', 0))
                        
                        with col4:
                            st.metric("Sleep Hours", f"{timetable['summary'].get('sleep_hours', 7.5)}h")
                    
                    # Sleep cycle recommendations
                    if 'sleep_recommendations' in timetable:
                        st.markdown("### 😴 Sleep Cycle Recommendations")
                        for rec in timetable['sleep_recommendations']:
                            st.write(f"• {rec}")
                    
                    # Download PDF
                    st.markdown("---")
                    st.markdown("### 📥 Download Your Timetable")
                    
                    filepath = managers['pdf'].generate_timetable_pdf(
                        timetable,
                        username,
                        timetable_description
                    )
                    
                    if filepath:
                        with open(filepath, "rb") as f:
                            st.download_button(
                                "📥 Download PDF",
                                f,
                                file_name=os.path.basename(filepath),
                                mime="application/pdf",
                                use_container_width=True
                            )
                    
                    # Clear tasks
                    st.session_state.tasks = []
                else:
                    st.error("Failed to generate timetable. Please try again.")

def render_ai_chat():
    """Render AI chat page"""
    st.markdown("### 💬 Chat with AI Assistant")
    
    username = get_current_user()
    managers = init_managers()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        
        st.markdown(f"""
        <div class="chat-message {role}">
            <strong>{'You' if role == 'user' else 'AI'}:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    user_message = st.text_input("Ask me anything about productivity, timetables, or time management:", key="chat_input")
    
    if st.button("Send", type="primary"):
        if user_message:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Get user context
            user_context = {
                'tasks': st.session_state.get('tasks', []),
                'goals': {
                    'short_term': '',
                    'long_term': '',
                    'daily': ''
                }
            }
            
            # Get AI response
            response = managers['ai'].chat_with_ai(
                user_message,
                st.session_state.chat_history,
                user_context
            )
            
            # Add AI response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

def render_history():
    """Render history page"""
    st.markdown("### 📊 Timetable History")
    
    username = get_current_user()
    managers = init_managers()
    
    timetables = managers['db'].get_user_timetables(username)
    
    if timetables:
        for tt in reversed(timetables):
            with st.expander(f"📅 {tt.get('date', 'Unknown')} - {tt.get('day', 'Unknown')}"):
                st.write(f"**Created:** {tt.get('created_at', 'Unknown')[:10]}")
                
                if 'schedule' in tt:
                    st.markdown("#### Schedule")
                    for item in tt['schedule']:
                        priority = item.get('priority', 'medium')
                        priority_emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                        st.write(f"{priority_emoji} **{item.get('time', '')}**: {item.get('activity', '')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Download PDF", key=f"history_pdf_{tt.get('id')}"):
                        filepath = managers['pdf'].generate_timetable_pdf(tt, username)
                        if filepath:
                            with open(filepath, "rb") as f:
                                st.download_button(
                                    "Download PDF",
                                    f,
                                    file_name=os.path.basename(filepath),
                                    mime="application/pdf"
                                )
                
                with col2:
                    if st.button("🗑️ Delete", key=f"history_del_{tt.get('id')}"):
                        managers['db'].delete_timetable(username, tt.get('id'))
                        st.rerun()
    else:
        st.info("No timetables in history yet.")

def render_settings():
    """Render settings page"""
    st.markdown("### ⚙️ Settings")
    
    username = get_current_user()
    managers = init_managers()
    
    st.markdown("#### 👤 User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {username}")
    
    with col2:
        if st.button("🚪 Logout", type="primary"):
            logout()
    
    st.markdown("---")
    
    st.markdown("#### 🎨 Preferences")
    
    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    # Notification preferences
    notifications = st.checkbox("Enable notifications", value=True)
    
    # Default wake time
    default_wake = st.time_input("Default Wake Time", value=datetime.strptime("06:00", "%H:%M").time())
    
    # Default sleep time
    default_sleep = st.time_input("Default Sleep Time", value=datetime.strptime("22:00", "%H:%M").time())
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

def main():
    """Main application function"""
    # Check authentication
    if not check_authentication():
        render_login_page()
        return
    
    # Render sidebar and get current page
    page = render_sidebar()
    
    # Render current page
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "📋 Create Timetable":
        render_create_timetable()
    elif page == "💬 AI Chat":
        render_ai_chat()
    elif page == "📊 History":
        render_history()
    elif page == "⚙️ Settings":
        render_settings()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
