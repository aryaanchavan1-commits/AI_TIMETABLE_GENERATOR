"""
AI Timetable Generator using Groq API
Generates intelligent timetables based on user tasks, goals, and productivity techniques
"""

import streamlit as st
from groq import Groq
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class AITimetableGenerator:
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client with API key from Streamlit secrets"""
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)
            else:
                st.error("Groq API key not found in secrets. Please add GROQ_API_KEY to your .streamlit/secrets.toml file.")
        except Exception as e:
            st.error(f"Failed to initialize Groq client: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for AI timetable generation"""
        return """You are an expert productivity coach and timetable generator. Your role is to create 
        intelligent, realistic, and personalized timetables that maximize productivity while maintaining 
        work-life balance.

        Key principles to follow:
        1. Respect natural sleep cycles (7-9 hours of sleep, ideally 10 PM - 6 AM)
        2. Incorporate Pomodoro technique (25 min work, 5 min break, long break after 4 sessions)
        3. Schedule demanding tasks during peak energy hours (typically 9 AM - 12 PM and 4 PM - 6 PM)
        4. Include buffer time between tasks (10-15 minutes)
        5. Balance work, exercise, meals, and relaxation
        6. Consider the user's specific goals and deadlines
        7. Make the schedule realistic and achievable
        8. Include motivational notes and productivity tips
        9. PRIORITIZE TASKS BY IMPORTANCE: Schedule high-importance tasks during peak energy hours
        10. Group similar tasks together to minimize context switching
        11. Include sleep cycle optimization recommendations
        12. Add energy management tips throughout the day

        IMPORTANCE-BASED SCHEDULING RULES:
        - HIGH importance tasks: Schedule during peak energy hours (9 AM - 12 PM, 4 PM - 6 PM)
        - MEDIUM importance tasks: Schedule during moderate energy hours (1 PM - 3 PM)
        - LOW importance tasks: Schedule during low energy hours (after 6 PM or early morning)

        SLEEP CYCLE OPTIMIZATION:
        - Recommend optimal bedtime based on wake time (5-6 sleep cycles of 90 minutes each)
        - Include wind-down activities before sleep
        - Suggest morning routine to maximize energy
        - Include short power naps if needed (20-30 minutes before 3 PM)

        Always respond in a structured JSON format that can be easily parsed and displayed.
        """
    
    def _create_user_context(self, 
                            tasks: List[Dict[str, Any]], 
                            goals: Dict[str, Any],
                            preferences: Dict[str, Any],
                            current_time: datetime) -> str:
        """Create user context for AI with importance-based scheduling"""
        
        # Sort tasks by importance
        importance_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_tasks = sorted(tasks, key=lambda x: importance_order.get(x.get('importance', 'medium'), 1))
        
        # Calculate total time needed
        total_time = sum(task.get('duration', 60) for task in tasks)
        
        # Get peak energy hours
        peak_start = preferences.get('peak_energy_start', '09:00')
        peak_end = preferences.get('peak_energy_end', '12:00')
        
        context = f"""
        Current Date and Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
        Day of Week: {current_time.strftime('%A')}
        
        USER TASKS (Sorted by Importance):
        {json.dumps(sorted_tasks, indent=2)}
        
        TASK ANALYSIS:
        - Total tasks: {len(tasks)}
        - Total time needed: {total_time // 60} hours {total_time % 60} minutes
        - High priority tasks: {sum(1 for t in tasks if t.get('importance') == 'high')}
        - Medium priority tasks: {sum(1 for t in tasks if t.get('importance') == 'medium')}
        - Low priority tasks: {sum(1 for t in tasks if t.get('importance') == 'low')}
        
        USER GOALS:
        Short-term Goals: {goals.get('short_term', 'Not specified')}
        Long-term Goals: {goals.get('long_term', 'Not specified')}
        Daily Goals: {goals.get('daily', 'Not specified')}
        
        USER PREFERENCES:
        Wake Up Time: {preferences.get('wake_up_time', '6:00 AM')}
        Sleep Time: {preferences.get('sleep_time', '10:00 PM')}
        Work Hours: {preferences.get('work_hours', '9:00 AM - 5:00 PM')}
        Break Preferences: {preferences.get('break_preferences', 'Pomodoro (25/5)')}
        Focus Areas: {preferences.get('focus_areas', 'General productivity')}
        Peak Energy Start: {peak_start}
        Peak Energy End: {peak_end}
        
        SLEEP CYCLE OPTIMIZATION:
        - Calculate optimal bedtime based on wake time
        - Include 5-6 sleep cycles (7.5-9 hours)
        - Add wind-down activities 1 hour before sleep
        - Include morning routine to maximize energy
        
        Please generate a detailed timetable for today that includes:
        1. Time blocks for each task (ordered by importance)
        2. HIGH importance tasks during peak energy hours
        3. MEDIUM importance tasks during moderate energy hours
        4. LOW importance tasks during low energy hours
        5. Pomodoro sessions where appropriate
        6. Breaks and meal times
        7. Exercise or movement breaks
        8. Buffer time between tasks (10-15 minutes)
        9. Evening wind-down activities
        10. Sleep cycle recommendations
        11. Energy management tips
        12. Motivational notes
        
        Format the response as a JSON object with the following structure:
        {
            "date": "YYYY-MM-DD",
            "day": "Day of week",
            "schedule": [
                {
                    "time": "HH:MM - HH:MM",
                    "activity": "Activity name",
                    "description": "Detailed description",
                    "type": "work|break|meal|exercise|relaxation|sleep",
                    "pomodoro_sessions": number (if applicable),
                    "priority": "high|medium|low",
                    "importance": "high|medium|low",
                    "energy_level": "peak|moderate|low",
                    "tips": "Productivity tip for this block"
                }
            ],
            "summary": {
                "total_work_hours": number,
                "total_break_time": number,
                "focus_sessions": number,
                "sleep_hours": number,
                "key_achievements": ["list of expected achievements"],
                "energy_management": ["list of energy management tips"]
            },
            "sleep_recommendations": [
                "Optimal bedtime recommendations",
                "Sleep hygiene tips"
            ],
            "motivation": "Daily motivational message"
        }
        """
        return context
    
    def generate_timetable(self, 
                          tasks: List[Dict[str, Any]], 
                          goals: Dict[str, Any],
                          preferences: Dict[str, Any],
                          description: str = "") -> Optional[Dict[str, Any]]:
        """Generate a timetable using AI with importance-based scheduling"""
        if not self.client:
            return None
        
        try:
            current_time = datetime.now()
            user_context = self._create_user_context(tasks, goals, preferences, current_time)
            
            if description:
                user_context += f"\n\nADDITIONAL DESCRIPTION:\n{description}"
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": user_context
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                stream=False
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                # Find JSON in response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_str = response_text[json_start:json_end]
                    timetable = json.loads(json_str)
                    return timetable
                else:
                    # If no JSON found, create a structured response
                    return self._create_fallback_timetable(tasks, goals, preferences, response_text)
            
            except json.JSONDecodeError:
                return self._create_fallback_timetable(tasks, goals, preferences, response_text)
        
        except Exception as e:
            st.error(f"Error generating timetable: {str(e)}")
            return None
    
    def _create_fallback_timetable(self, 
                                   tasks: List[Dict[str, Any]], 
                                   goals: Dict[str, Any],
                                   preferences: Dict[str, Any],
                                   ai_response: str) -> Dict[str, Any]:
        """Create a fallback timetable with importance-based scheduling"""
        current_time = datetime.now()
        
        # Sort tasks by importance
        importance_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_tasks = sorted(tasks, key=lambda x: importance_order.get(x.get('importance', 'medium'), 1))
        
        schedule = []
        
        # Get wake and sleep times
        wake_time = preferences.get('wake_up_time', '06:00')
        sleep_time = preferences.get('sleep_time', '22:00')
        
        # Parse wake time
        wake_hour, wake_min = map(int, wake_time.split(':'))
        
        # Morning routine
        schedule.append({
            "time": f"{wake_hour:02d}:{wake_min:02d} - {wake_hour+1:02d}:{wake_min:02d}",
            "activity": "Morning Routine",
            "description": "Wake up, freshen up, light exercise, breakfast",
            "type": "routine",
            "priority": "high",
            "importance": "high",
            "energy_level": "moderate",
            "tips": "Start your day with intention and energy. Get natural light exposure."
        })
        
        current_hour = wake_hour + 1
        current_min = wake_min
        
        # Schedule high importance tasks during peak energy hours (9 AM - 12 PM)
        peak_start = int(preferences.get('peak_energy_start', '09:00').split(':')[0])
        peak_end = int(preferences.get('peak_energy_end', '12:00').split(':')[0])
        
        # Add tasks based on importance
        for task in sorted_tasks:
            task_name = task.get('name', 'Task')
            duration = task.get('duration', 60)
            importance = task.get('importance', 'medium')
            
            # Determine energy level based on time and importance
            if current_hour >= peak_start and current_hour < peak_end:
                energy_level = "peak"
            elif current_hour >= 13 and current_hour < 15:
                energy_level = "moderate"
            else:
                energy_level = "low"
            
            # Calculate end time
            end_hour = current_hour + (duration // 60)
            end_min = current_min + (duration % 60)
            
            if end_min >= 60:
                end_hour += 1
                end_min -= 60
            
            schedule.append({
                "time": f"{current_hour:02d}:{current_min:02d} - {end_hour:02d}:{end_min:02d}",
                "activity": task_name,
                "description": task.get('description', 'Focus on this important task'),
                "type": "work",
                "pomodoro_sessions": max(1, duration // 30),
                "priority": importance,
                "importance": importance,
                "energy_level": energy_level,
                "tips": f"{'🔴 HIGH PRIORITY - ' if importance == 'high' else ''}Use Pomodoro technique: 25 min work, 5 min break"
            })
            
            # Add buffer time
            current_hour = end_hour
            current_min = end_min + 15
            
            if current_min >= 60:
                current_hour += 1
                current_min -= 60
            
            # Add break after every 2 tasks
            if len(schedule) % 3 == 0:
                schedule.append({
                    "time": f"{current_hour:02d}:{current_min:02d} - {current_hour:02d}:{current_min+15:02d}",
                    "activity": "Short Break",
                    "description": "Stretch, hydrate, rest your eyes",
                    "type": "break",
                    "priority": "medium",
                    "importance": "medium",
                    "energy_level": "low",
                    "tips": "Movement boosts creativity and focus"
                })
                current_min += 15
                
                if current_min >= 60:
                    current_hour += 1
                    current_min -= 60
        
        # Add lunch break
        schedule.append({
            "time": "12:00 - 13:00",
            "activity": "Lunch Break",
            "description": "Healthy lunch and short walk",
            "type": "meal",
            "priority": "medium",
            "importance": "medium",
            "energy_level": "moderate",
            "tips": "Take a proper break to recharge. Avoid heavy meals."
        })
        
        # Add afternoon break
        schedule.append({
            "time": "15:00 - 15:15",
            "activity": "Afternoon Break",
            "description": "Short break, stretch, hydrate",
            "type": "break",
            "priority": "medium",
            "importance": "medium",
            "energy_level": "low",
            "tips": "Consider a power nap (20-30 min) if needed"
        })
        
        # Add exercise
        schedule.append({
            "time": "18:00 - 19:00",
            "activity": "Exercise",
            "description": "Physical activity or sports",
            "type": "exercise",
            "priority": "high",
            "importance": "high",
            "energy_level": "moderate",
            "tips": "Exercise improves mental clarity and sleep quality"
        })
        
        # Add evening wind-down
        schedule.append({
            "time": "21:00 - 22:00",
            "activity": "Evening Wind-down",
            "description": "Relaxation, reading, prepare for sleep",
            "type": "relaxation",
            "priority": "medium",
            "importance": "medium",
            "energy_level": "low",
            "tips": "Avoid screens 1 hour before bed. Quality sleep is essential for productivity"
        })
        
        # Calculate sleep hours
        sleep_hour = int(sleep_time.split(':')[0])
        wake_hour = int(wake_time.split(':')[0])
        
        if sleep_hour > wake_hour:
            sleep_hours = 24 - sleep_hour + wake_hour
        else:
            sleep_hours = wake_hour - sleep_hour
        
        return {
            "date": current_time.strftime('%Y-%m-%d'),
            "day": current_time.strftime('%A'),
            "schedule": schedule,
            "summary": {
                "total_work_hours": 8,
                "total_break_time": 2,
                "focus_sessions": 4,
                "sleep_hours": sleep_hours,
                "key_achievements": [task.get('name', 'Complete task') for task in sorted_tasks[:3]],
                "energy_management": [
                    "Schedule high-priority tasks during peak energy hours",
                    "Take regular breaks to maintain focus",
                    "Stay hydrated throughout the day",
                    "Exercise regularly for mental clarity"
                ]
            },
            "sleep_recommendations": [
                f"Optimal bedtime: {sleep_time} for {sleep_hours} hours of sleep",
                "Maintain consistent sleep schedule",
                "Avoid screens 1 hour before bedtime",
                "Keep bedroom cool and dark",
                "Create a relaxing bedtime routine"
            ],
            "motivation": "Every day is a new opportunity to achieve your goals. Stay focused and consistent!",
            "ai_notes": ai_response
        }
    
    def chat_with_ai(self, 
                     message: str, 
                     chat_history: List[Dict[str, Any]],
                     user_context: Dict[str, Any]) -> str:
        """Chat with AI about timetable and productivity"""
        if not self.client:
            return "AI service is not available. Please check your API key configuration."
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful productivity assistant. You help users with:
                    - Creating and optimizing timetables
                    - Productivity tips and techniques
                    - Time management advice
                    - Goal setting and achievement strategies
                    - Work-life balance tips
                    - Sleep cycle optimization
                    - Energy management
                    - Importance-based task scheduling
                    
                    Be friendly, encouraging, and provide actionable advice.
                    Keep responses concise but helpful."""
                }
            ]
            
            # Add chat history
            for msg in chat_history[-10:]:  # Last 10 messages for context
                messages.append({
                    "role": msg.get('role', 'user'),
                    "content": msg.get('content', '')
                })
            
            # Add current message with context
            context_message = f"""
            User Context:
            - Current tasks: {json.dumps(user_context.get('tasks', []))}
            - Goals: {json.dumps(user_context.get('goals', {}))}
            
            User Message: {message}
            """
            
            messages.append({
                "role": "user",
                "content": context_message
            })
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            return chat_completion.choices[0].message.content
        
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again."
    
    def optimize_timetable(self, 
                          current_timetable: Dict[str, Any],
                          feedback: str) -> Optional[Dict[str, Any]]:
        """Optimize existing timetable based on feedback"""
        if not self.client:
            return None
        
        try:
            prompt = f"""
            Current Timetable:
            {json.dumps(current_timetable, indent=2)}
            
            User Feedback:
            {feedback}
            
            Please optimize this timetable based on the feedback. Consider:
            1. Adjusting time blocks
            2. Adding or removing activities
            3. Improving work-life balance
            4. Incorporating more productivity techniques
            5. Optimizing task scheduling based on importance
            6. Improving sleep cycle integration
            7. Enhancing energy management
            
            Return the optimized timetable in the same JSON format.
            """
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                stream=False
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Extract JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            
            return None
        
        except Exception as e:
            st.error(f"Error optimizing timetable: {str(e)}")
            return None
