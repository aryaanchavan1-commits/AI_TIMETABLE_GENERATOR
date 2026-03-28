"""
Productivity Techniques Module for AI Timetable Generator
Implements Pomodoro, sleep cycles, and other productivity methods with AI integration
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time

class PomodoroTimer:
    """Pomodoro Technique Timer"""
    
    def __init__(self):
        self.work_duration = 25  # minutes
        self.short_break = 5     # minutes
        self.long_break = 15     # minutes
        self.sessions_before_long = 4
    
    def get_session_info(self, session_count: int) -> Dict[str, Any]:
        """Get current session information"""
        if session_count % self.sessions_before_long == 0 and session_count > 0:
            return {
                'type': 'long_break',
                'duration': self.long_break,
                'message': 'Time for a long break! Stretch, walk, or relax.'
            }
        elif session_count % 2 == 0:
            return {
                'type': 'work',
                'duration': self.work_duration,
                'message': 'Focus time! Work on your task with full concentration.'
            }
        else:
            return {
                'type': 'short_break',
                'duration': self.short_break,
                'message': 'Short break! Rest your eyes and stretch.'
            }
    
    def render_pomodoro_widget(self):
        """Render Pomodoro timer widget in Streamlit"""
        st.markdown("### 🍅 Pomodoro Timer")
        
        if 'pomodoro_session' not in st.session_state:
            st.session_state.pomodoro_session = 0
            st.session_state.pomodoro_running = False
            st.session_state.pomodoro_start_time = None
        
        session_info = self.get_session_info(st.session_state.pomodoro_session)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"**Session {st.session_state.pomodoro_session + 1}**")
            st.write(session_info['message'])
        
        with col2:
            st.metric("Duration", f"{session_info['duration']} min")
        
        with col3:
            if st.button("▶️ Start" if not st.session_state.pomodoro_running else "⏸️ Pause"):
                st.session_state.pomodoro_running = not st.session_state.pomodoro_running
                if st.session_state.pomodoro_running:
                    st.session_state.pomodoro_start_time = datetime.now()
        
        if st.session_state.pomodoro_running and st.session_state.pomodoro_start_time:
            elapsed = (datetime.now() - st.session_state.pomodoro_start_time).seconds
            remaining = max(0, session_info['duration'] * 60 - elapsed)
            
            progress = 1 - (remaining / (session_info['duration'] * 60))
            st.progress(progress)
            
            mins, secs = divmod(remaining, 60)
            st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            
            if remaining == 0:
                st.session_state.pomodoro_session += 1
                st.session_state.pomodoro_running = False
                st.session_state.pomodoro_start_time = None
                st.success("Session complete! 🎉")
                st.rerun()
        
        if st.button("🔄 Reset"):
            st.session_state.pomodoro_session = 0
            st.session_state.pomodoro_running = False
            st.session_state.pomodoro_start_time = None
            st.rerun()

class SleepCycleOptimizer:
    """Sleep Cycle Optimization with AI Integration"""
    
    def __init__(self):
        self.sleep_cycles = 90  # minutes per sleep cycle
        self.recommended_cycles = 5  # 7.5 hours
        self.ideal_sleep_hours = 7.5
    
    def calculate_optimal_bedtime(self, wake_time: str) -> List[Dict[str, Any]]:
        """Calculate optimal bedtime based on wake time"""
        try:
            wake_hour, wake_min = map(int, wake_time.split(':'))
            wake_datetime = datetime.now().replace(hour=wake_hour, minute=wake_min, second=0, microsecond=0)
            
            bedtimes = []
            for cycles in range(4, 7):  # 4-6 sleep cycles
                sleep_minutes = cycles * self.sleep_cycles
                bedtime = wake_datetime - timedelta(minutes=sleep_minutes)
                
                # Adjust for falling asleep time (15 minutes)
                bedtime -= timedelta(minutes=15)
                
                bedtimes.append({
                    'time': bedtime.strftime('%H:%M'),
                    'cycles': cycles,
                    'hours': sleep_minutes / 60,
                    'quality': 'Optimal' if cycles == 5 else 'Good' if cycles == 6 else 'Minimum'
                })
            
            return bedtimes
        except:
            return []
    
    def calculate_wake_time_from_bedtime(self, bedtime: str) -> List[Dict[str, Any]]:
        """Calculate optimal wake times based on bedtime"""
        try:
            bed_hour, bed_min = map(int, bedtime.split(':'))
            bed_datetime = datetime.now().replace(hour=bed_hour, minute=bed_min, second=0, microsecond=0)
            
            wake_times = []
            for cycles in range(4, 7):  # 4-6 sleep cycles
                sleep_minutes = cycles * self.sleep_cycles
                wake_datetime = bed_datetime + timedelta(minutes=sleep_minutes)
                
                # Adjust for falling asleep time (15 minutes)
                wake_datetime += timedelta(minutes=15)
                
                wake_times.append({
                    'time': wake_datetime.strftime('%H:%M'),
                    'cycles': cycles,
                    'hours': sleep_minutes / 60,
                    'quality': 'Optimal' if cycles == 5 else 'Good' if cycles == 6 else 'Minimum'
                })
            
            return wake_times
        except:
            return []
    
    def get_sleep_recommendations(self) -> List[str]:
        """Get sleep hygiene recommendations"""
        return [
            "Maintain a consistent sleep schedule, even on weekends",
            "Avoid screens 1 hour before bedtime",
            "Keep your bedroom cool (65-68°F / 18-20°C)",
            "Avoid caffeine after 2 PM",
            "Exercise regularly, but not too close to bedtime",
            "Create a relaxing bedtime routine",
            "Limit naps to 20-30 minutes before 3 PM",
            "Get exposure to natural light during the day",
            "Avoid heavy meals close to bedtime",
            "Use your bed only for sleep and intimacy"
        ]
    
    def get_energy_level_recommendations(self, time_of_day: str) -> Dict[str, Any]:
        """Get energy level recommendations based on time of day"""
        hour = int(time_of_day.split(':')[0])
        
        if 6 <= hour < 9:
            return {
                'level': 'moderate',
                'recommendations': [
                    'Light exercise or stretching',
                    'Healthy breakfast',
                    'Plan your day',
                    'Review priorities'
                ],
                'best_for': ['Planning', 'Light tasks', 'Exercise']
            }
        elif 9 <= hour < 12:
            return {
                'level': 'peak',
                'recommendations': [
                    'Tackle your most important tasks',
                    'Deep work sessions',
                    'Creative problem solving',
                    'Complex decision making'
                ],
                'best_for': ['High-priority tasks', 'Deep work', 'Creative work']
            }
        elif 12 <= hour < 14:
            return {
                'level': 'moderate',
                'recommendations': [
                    'Lunch break',
                    'Light administrative tasks',
                    'Team meetings',
                    'Email responses'
                ],
                'best_for': ['Meetings', 'Administrative tasks', 'Social interactions']
            }
        elif 14 <= hour < 16:
            return {
                'level': 'low',
                'recommendations': [
                    'Short power nap (20-30 min)',
                    'Light physical activity',
                    'Routine tasks',
                    'Review and organize'
                ],
                'best_for': ['Routine tasks', 'Organization', 'Light work']
            }
        elif 16 <= hour < 19:
            return {
                'level': 'peak',
                'recommendations': [
                    'Second wind of productivity',
                    'Exercise or sports',
                    'Creative projects',
                    'Learning new skills'
                ],
                'best_for': ['Exercise', 'Learning', 'Creative work']
            }
        elif 19 <= hour < 22:
            return {
                'level': 'moderate',
                'recommendations': [
                    'Wind down activities',
                    'Light reading',
                    'Family time',
                    'Prepare for tomorrow'
                ],
                'best_for': ['Relaxation', 'Social time', 'Planning']
            }
        else:
            return {
                'level': 'low',
                'recommendations': [
                    'Avoid screens',
                    'Relaxation techniques',
                    'Prepare for sleep',
                    'Light stretching'
                ],
                'best_for': ['Sleep preparation', 'Relaxation']
            }
    
    def render_sleep_widget(self):
        """Render sleep optimization widget with AI features"""
        st.markdown("### 😴 Sleep Optimizer")
        
        tab1, tab2, tab3 = st.tabs(["🌙 Bedtime Calculator", "⏰ Wake Time Calculator", "💡 Energy Tips"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                wake_time = st.text_input("Wake Up Time (HH:MM)", value="06:00", key="sleep_wake")
            
            with col2:
                if st.button("Calculate Optimal Bedtime", key="calc_bedtime"):
                    bedtimes = self.calculate_optimal_bedtime(wake_time)
                    
                    if bedtimes:
                        st.success("🌙 Optimal Bedtimes Based on Sleep Cycles:")
                        for bt in bedtimes:
                            quality_emoji = "⭐" if bt['quality'] == 'Optimal' else "✅" if bt['quality'] == 'Good' else "⚠️"
                            st.write(f"{quality_emoji} **{bt['time']}** - {bt['cycles']} cycles ({bt['hours']:.1f} hours) - {bt['quality']}")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                bedtime = st.text_input("Bedtime (HH:MM)", value="22:00", key="sleep_bed")
            
            with col2:
                if st.button("Calculate Optimal Wake Time", key="calc_wake"):
                    wake_times = self.calculate_wake_time_from_bedtime(bedtime)
                    
                    if wake_times:
                        st.success("⏰ Optimal Wake Times Based on Sleep Cycles:")
                        for wt in wake_times:
                            quality_emoji = "⭐" if wt['quality'] == 'Optimal' else "✅" if wt['quality'] == 'Good' else "⚠️"
                            st.write(f"{quality_emoji} **{wt['time']}** - {wt['cycles']} cycles ({wt['hours']:.1f} hours) - {wt['quality']}")
        
        with tab3:
            current_time = st.text_input("Current Time (HH:MM)", value=datetime.now().strftime('%H:%M'), key="energy_time")
            
            if st.button("Get Energy Recommendations", key="get_energy"):
                energy_info = self.get_energy_level_recommendations(current_time)
                
                level_emoji = "🔴" if energy_info['level'] == 'peak' else "🟡" if energy_info['level'] == 'moderate' else "🟢"
                st.success(f"{level_emoji} Energy Level: **{energy_info['level'].upper()}**")
                
                st.markdown("**Recommendations:**")
                for rec in energy_info['recommendations']:
                    st.write(f"• {rec}")
                
                st.markdown("**Best for:**")
                for task in energy_info['best_for']:
                    st.write(f"• {task}")
        
        with st.expander("Sleep Hygiene Tips"):
            tips = self.get_sleep_recommendations()
            for i, tip in enumerate(tips, 1):
                st.write(f"{i}. {tip}")

class FocusMode:
    """Focus Mode - Prevents going back from screen"""
    
    def __init__(self):
        self.is_active = False
        self.start_time = None
        self.current_task = None
    
    def activate(self, task: str):
        """Activate focus mode"""
        self.is_active = True
        self.start_time = datetime.now()
        self.current_task = task
    
    def deactivate(self):
        """Deactivate focus mode"""
        self.is_active = False
        self.start_time = None
        self.current_task = None
    
    def get_elapsed_time(self) -> Optional[str]:
        """Get elapsed time since focus mode started"""
        if self.is_active and self.start_time:
            elapsed = datetime.now() - self.start_time
            hours, remainder = divmod(elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return None
    
    def render_focus_widget(self):
        """Render focus mode widget"""
        st.markdown("### 🎯 Focus Mode")
        
        if not self.is_active:
            task = st.text_input("What are you focusing on?", key="focus_task_input")
            
            if st.button("🚀 Start Focus Mode", type="primary"):
                if task:
                    self.activate(task)
                    st.rerun()
                else:
                    st.warning("Please enter a task to focus on")
        else:
            st.success(f"**Currently focusing on:** {self.current_task}")
            
            elapsed = self.get_elapsed_time()
            if elapsed:
                st.metric("Time Elapsed", elapsed)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⏸️ Take Break"):
                    self.deactivate()
                    st.rerun()
            
            with col2:
                if st.button("✅ Complete Task"):
                    st.success("Great job! Task completed! 🎉")
                    self.deactivate()
                    st.rerun()
            
            # Warning message
            st.warning("⚠️ Focus mode is active. Stay on this screen and avoid distractions!")

class TimeBlocking:
    """Time Blocking Technique"""
    
    def __init__(self):
        self.blocks = []
    
    def create_block(self, 
                    start_time: str, 
                    end_time: str, 
                    activity: str,
                    category: str = "work",
                    importance: str = "medium") -> Dict[str, Any]:
        """Create a time block with importance"""
        block = {
            'id': len(self.blocks) + 1,
            'start_time': start_time,
            'end_time': end_time,
            'activity': activity,
            'category': category,
            'importance': importance,
            'created_at': datetime.now().isoformat()
        }
        self.blocks.append(block)
        return block
    
    def get_daily_blocks(self, date: str) -> List[Dict[str, Any]]:
        """Get blocks for a specific date"""
        return [b for b in self.blocks if b.get('date') == date]
    
    def render_time_blocking_widget(self):
        """Render time blocking widget with importance"""
        st.markdown("### 📅 Time Blocking")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            start_time = st.time_input("Start Time", value=datetime.now().time())
        
        with col2:
            end_time = st.time_input("End Time", value=(datetime.now() + timedelta(hours=1)).time())
        
        with col3:
            activity = st.text_input("Activity")
        
        with col4:
            importance = st.selectbox("Importance", ["high", "medium", "low"])
        
        category = st.selectbox("Category", ["work", "break", "meeting", "exercise", "learning", "personal"])
        
        if st.button("Add Time Block"):
            if activity:
                block = self.create_block(
                    start_time.strftime('%H:%M'),
                    end_time.strftime('%H:%M'),
                    activity,
                    category,
                    importance
                )
                st.success(f"Added: {activity} ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}) - {importance.upper()}")
        
        if self.blocks:
            st.markdown("#### Today's Blocks")
            
            # Sort by importance
            importance_order = {'high': 0, 'medium': 1, 'low': 2}
            sorted_blocks = sorted(self.blocks[-5:], key=lambda x: importance_order.get(x.get('importance', 'medium'), 1))
            
            for block in sorted_blocks:
                importance_emoji = "🔴" if block['importance'] == 'high' else "🟡" if block['importance'] == 'medium' else "🟢"
                st.write(f"{importance_emoji} **{block['start_time']} - {block['end_time']}**: {block['activity']} ({block['category']})")

class EisenhowerMatrix:
    """Eisenhower Matrix for Task Prioritization"""
    
    def __init__(self):
        self.quadrants = {
            'urgent_important': [],
            'not_urgent_important': [],
            'urgent_not_important': [],
            'not_urgent_not_important': []
        }
    
    def categorize_task(self, task: str, is_urgent: bool, is_important: bool) -> str:
        """Categorize task into quadrant"""
        if is_urgent and is_important:
            quadrant = 'urgent_important'
            action = 'Do it now'
        elif not is_urgent and is_important:
            quadrant = 'not_urgent_important'
            action = 'Schedule it'
        elif is_urgent and not is_important:
            quadrant = 'urgent_not_important'
            action = 'Delegate it'
        else:
            quadrant = 'not_urgent_not_important'
            action = 'Eliminate it'
        
        self.quadrants[quadrant].append({
            'task': task,
            'action': action,
            'added_at': datetime.now().isoformat()
        })
        
        return quadrant
    
    def render_eisenhower_widget(self):
        """Render Eisenhower Matrix widget"""
        st.markdown("### 📊 Eisenhower Matrix")
        
        task = st.text_input("Enter task")
        
        col1, col2 = st.columns(2)
        
        with col1:
            is_urgent = st.checkbox("Urgent")
        
        with col2:
            is_important = st.checkbox("Important")
        
        if st.button("Categorize Task"):
            if task:
                quadrant = self.categorize_task(task, is_urgent, is_important)
                st.success(f"Task categorized as: **{quadrant.replace('_', ' ').title()}**")
        
        # Display matrix
        st.markdown("#### Task Matrix")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Urgent & Important**")
            st.write("*Do it now*")
            for item in self.quadrants['urgent_important'][-3:]:
                st.write(f"- {item['task']}")
        
        with col2:
            st.markdown("**🟡 Not Urgent & Important**")
            st.write("*Schedule it*")
            for item in self.quadrants['not_urgent_important'][-3:]:
                st.write(f"- {item['task']}")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**🟠 Urgent & Not Important**")
            st.write("*Delegate it*")
            for item in self.quadrants['urgent_not_important'][-3:]:
                st.write(f"- {item['task']}")
        
        with col4:
            st.markdown("**🟢 Not Urgent & Not Important**")
            st.write("*Eliminate it*")
            for item in self.quadrants['not_urgent_not_important'][-3:]:
                st.write(f"- {item['task']}")

class ProductivityTechniques:
    """Main productivity techniques manager"""
    
    def __init__(self):
        self.pomodoro = PomodoroTimer()
        self.sleep_optimizer = SleepCycleOptimizer()
        self.focus_mode = FocusMode()
        self.time_blocking = TimeBlocking()
        self.eisenhower = EisenhowerMatrix()
    
    def render_all_techniques(self):
        """Render all productivity techniques"""
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🍅 Pomodoro", 
            "😴 Sleep", 
            "🎯 Focus", 
            "📅 Time Blocking",
            "📊 Eisenhower"
        ])
        
        with tab1:
            self.pomodoro.render_pomodoro_widget()
        
        with tab2:
            self.sleep_optimizer.render_sleep_widget()
        
        with tab3:
            self.focus_mode.render_focus_widget()
        
        with tab4:
            self.time_blocking.render_time_blocking_widget()
        
        with tab5:
            self.eisenhower.render_eisenhower_widget()
    
    def get_productivity_tips(self) -> List[str]:
        """Get general productivity tips"""
        return [
            "🎯 Start with your most important task (MIT)",
            "⏰ Use time blocking to schedule your day",
            "🍅 Use Pomodoro technique for focused work",
            "📵 Minimize distractions during focus time",
            "💪 Take regular breaks to maintain energy",
            "📝 Review and plan your day each morning",
            "🌙 Prioritize sleep for better performance",
            "🧘 Practice mindfulness or meditation",
            "🥗 Eat healthy and stay hydrated",
            "🏃 Exercise regularly for mental clarity",
            "📚 Learn to say no to non-essential tasks",
            "✅ Celebrate small wins to stay motivated"
        ]
