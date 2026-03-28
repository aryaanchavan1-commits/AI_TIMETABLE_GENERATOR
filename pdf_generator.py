"""
PDF Generator for AI Timetable Generator
Creates attractive, downloadable PDF timetables with importance indicators and sleep cycle info
"""

from fpdf import FPDF
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

class TimetablePDF(FPDF):
    """Custom PDF class for timetable generation"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(102, 126, 234)  # Purple color
        self.cell(0, 10, 'AI Generated Timetable', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
    
    def add_title_section(self, title: str, subtitle: str = ""):
        """Add title section"""
        self.set_font('Arial', 'B', 24)
        self.set_text_color(51, 51, 51)
        self.cell(0, 15, title, 0, 1, 'C')
        
        if subtitle:
            self.set_font('Arial', '', 12)
            self.set_text_color(102, 102, 102)
            self.cell(0, 8, subtitle, 0, 1, 'C')
        
        self.ln(10)
    
    def add_info_box(self, label: str, value: str):
        """Add information box"""
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(51, 51, 51)
        
        # Label
        self.cell(40, 8, label, 0, 0, 'L')
        
        # Value
        self.set_font('Arial', '', 10)
        self.cell(0, 8, value, 0, 1, 'L')
    
    def add_schedule_header(self):
        """Add schedule table header with importance column"""
        self.set_fill_color(102, 126, 234)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 9)
        
        col_widths = [25, 45, 55, 25, 25, 25]
        headers = ['Time', 'Activity', 'Description', 'Type', 'Priority', 'Energy']
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        
        self.ln()
    
    def add_schedule_row(self, item: Dict[str, Any], is_alt: bool = False):
        """Add schedule row with importance indicators"""
        if is_alt:
            self.set_fill_color(248, 249, 250)
        else:
            self.set_fill_color(255, 255, 255)
        
        self.set_text_color(51, 51, 51)
        self.set_font('Arial', '', 8)
        
        col_widths = [25, 45, 55, 25, 25, 25]
        
        # Time
        time_str = item.get('time', '')
        self.cell(col_widths[0], 8, time_str, 1, 0, 'C', True)
        
        # Activity
        activity = item.get('activity', '')
        self.cell(col_widths[1], 8, activity[:18], 1, 0, 'L', True)
        
        # Description
        description = item.get('description', '')
        self.cell(col_widths[2], 8, description[:25], 1, 0, 'L', True)
        
        # Type
        activity_type = item.get('type', '')
        type_color = self._get_type_color(activity_type)
        self.set_text_color(*type_color)
        self.cell(col_widths[3], 8, activity_type.capitalize(), 1, 0, 'C', True)
        
        # Priority with color coding
        priority = item.get('priority', item.get('importance', 'medium'))
        priority_color = self._get_priority_color(priority)
        self.set_text_color(*priority_color)
        self.cell(col_widths[4], 8, priority.upper(), 1, 0, 'C', True)
        
        # Energy level
        energy_level = item.get('energy_level', 'moderate')
        energy_color = self._get_energy_color(energy_level)
        self.set_text_color(*energy_color)
        self.cell(col_widths[5], 8, energy_level.capitalize(), 1, 1, 'C', True)
        
        self.set_text_color(51, 51, 51)
    
    def _get_type_color(self, activity_type: str) -> tuple:
        """Get color for activity type"""
        colors = {
            'work': (220, 53, 69),      # Red
            'break': (40, 167, 69),     # Green
            'meal': (255, 193, 7),      # Yellow
            'exercise': (0, 123, 255),  # Blue
            'relaxation': (111, 66, 193), # Purple
            'routine': (108, 117, 125), # Gray
            'sleep': (111, 66, 193)     # Purple
        }
        return colors.get(activity_type, (51, 51, 51))
    
    def _get_priority_color(self, priority: str) -> tuple:
        """Get color for priority level"""
        colors = {
            'high': (220, 53, 69),      # Red
            'medium': (255, 193, 7),    # Yellow
            'low': (40, 167, 69)        # Green
        }
        return colors.get(priority, (51, 51, 51))
    
    def _get_energy_color(self, energy_level: str) -> tuple:
        """Get color for energy level"""
        colors = {
            'peak': (220, 53, 69),      # Red
            'moderate': (255, 193, 7),  # Yellow
            'low': (40, 167, 69)        # Green
        }
        return colors.get(energy_level, (51, 51, 51))
    
    def add_summary_section(self, summary: Dict[str, Any]):
        """Add summary section with sleep and energy info"""
        self.ln(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'Daily Summary', 0, 1, 'L')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        
        self.add_info_box('Total Work Hours:', f"{summary.get('total_work_hours', 0)} hours")
        self.add_info_box('Total Break Time:', f"{summary.get('total_break_time', 0)} hours")
        self.add_info_box('Focus Sessions:', str(summary.get('focus_sessions', 0)))
        self.add_info_box('Sleep Hours:', f"{summary.get('sleep_hours', 7.5)} hours")
        
        if 'key_achievements' in summary:
            self.ln(5)
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Key Achievements:', 0, 1, 'L')
            
            self.set_font('Arial', '', 10)
            for achievement in summary['key_achievements']:
                self.cell(10, 6, '', 0, 0)
                self.cell(0, 6, f"• {achievement}", 0, 1, 'L')
        
        if 'energy_management' in summary:
            self.ln(5)
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, 'Energy Management Tips:', 0, 1, 'L')
            
            self.set_font('Arial', '', 10)
            for tip in summary['energy_management']:
                self.cell(10, 6, '', 0, 0)
                self.cell(0, 6, f"• {tip}", 0, 1, 'L')
    
    def add_sleep_recommendations_section(self, recommendations: List[str]):
        """Add sleep recommendations section"""
        self.ln(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'Sleep Cycle Recommendations', 0, 1, 'L')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        
        for i, rec in enumerate(recommendations, 1):
            self.cell(10, 6, '', 0, 0)
            self.cell(0, 6, f"{i}. {rec}", 0, 1, 'L')
    
    def add_motivation_section(self, motivation: str):
        """Add motivation section"""
        self.ln(10)
        self.set_fill_color(102, 126, 234)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'I', 11)
        
        self.multi_cell(0, 8, f'"{motivation}"', 0, 'C', True)
    
    def add_tips_section(self, tips: List[str]):
        """Add productivity tips section"""
        self.ln(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'Productivity Tips', 0, 1, 'L')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        
        for i, tip in enumerate(tips, 1):
            self.cell(10, 6, '', 0, 0)
            self.cell(0, 6, f"{i}. {tip}", 0, 1, 'L')
    
    def add_importance_legend(self):
        """Add importance legend"""
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'Priority & Energy Legend', 0, 1, 'L')
        
        self.set_font('Arial', '', 9)
        self.set_text_color(51, 51, 51)
        
        # Priority legend
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(220, 53, 69)
        self.cell(20, 6, 'HIGH', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- Schedule during peak energy hours', 0, 1, 'L')
        
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(255, 193, 7)
        self.cell(20, 6, 'MEDIUM', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- Schedule during moderate energy hours', 0, 1, 'L')
        
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(40, 167, 69)
        self.cell(20, 6, 'LOW', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- Schedule during low energy hours', 0, 1, 'L')
        
        # Energy legend
        self.ln(5)
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(220, 53, 69)
        self.cell(20, 6, 'PEAK', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- 9 AM - 12 PM, 4 PM - 6 PM', 0, 1, 'L')
        
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(255, 193, 7)
        self.cell(20, 6, 'MODERATE', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- 1 PM - 3 PM', 0, 1, 'L')
        
        self.cell(10, 6, '', 0, 0)
        self.set_text_color(40, 167, 69)
        self.cell(20, 6, 'LOW', 0, 0, 'C')
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, '- Early morning, evening', 0, 1, 'L')

class PDFGenerator:
    """Main PDF generator class"""
    
    def __init__(self):
        self.output_dir = "generated_pdfs"
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_timetable_pdf(self, 
                              timetable: Dict[str, Any],
                              username: str = "User",
                              description: str = "") -> Optional[str]:
        """Generate PDF for timetable with importance indicators and sleep info"""
        try:
            pdf = TimetablePDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            
            # Title section
            date_str = timetable.get('date', datetime.now().strftime('%Y-%m-%d'))
            day_str = timetable.get('day', datetime.now().strftime('%A'))
            
            pdf.add_title_section(
                f"Your Personalized Timetable",
                f"{day_str}, {date_str}"
            )
            
            # User info
            pdf.add_info_box('Created for:', username)
            if description:
                pdf.add_info_box('Description:', description[:50])
            pdf.add_info_box('Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M'))
            
            pdf.ln(10)
            
            # Schedule
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(102, 126, 234)
            pdf.cell(0, 10, 'Daily Schedule (Prioritized by Importance)', 0, 1, 'L')
            
            pdf.add_schedule_header()
            
            schedule = timetable.get('schedule', [])
            for i, item in enumerate(schedule):
                pdf.add_schedule_row(item, is_alt=(i % 2 == 0))
            
            # Importance legend
            pdf.add_importance_legend()
            
            # Summary
            if 'summary' in timetable:
                pdf.add_summary_section(timetable['summary'])
            
            # Sleep recommendations
            if 'sleep_recommendations' in timetable:
                pdf.add_sleep_recommendations_section(timetable['sleep_recommendations'])
            
            # Motivation
            if 'motivation' in timetable:
                pdf.add_motivation_section(timetable['motivation'])
            
            # Tips
            tips = [
                "Start with your most important task first (HIGH priority)",
                "Schedule demanding tasks during peak energy hours",
                "Take regular breaks to maintain focus",
                "Stay hydrated throughout the day",
                "Review your progress at the end of the day",
                "Prepare for tomorrow before going to bed",
                "Maintain consistent sleep schedule",
                "Exercise regularly for mental clarity"
            ]
            pdf.add_tips_section(tips)
            
            # Save PDF
            filename = f"timetable_{username}_{date_str}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            pdf.output(filepath)
            
            return filepath
        
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None
    
    def generate_weekly_timetable_pdf(self,
                                     timetables: List[Dict[str, Any]],
                                     username: str = "User") -> Optional[str]:
        """Generate PDF for weekly timetable"""
        try:
            pdf = TimetablePDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            
            # Title
            pdf.add_title_section(
                "Weekly Timetable",
                f"Created for {username}"
            )
            
            pdf.add_info_box('Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M'))
            pdf.ln(10)
            
            # Add each day
            for timetable in timetables:
                date_str = timetable.get('date', '')
                day_str = timetable.get('day', '')
                
                pdf.set_font('Arial', 'B', 12)
                pdf.set_text_color(102, 126, 234)
                pdf.cell(0, 10, f"{day_str} - {date_str}", 0, 1, 'L')
                
                pdf.add_schedule_header()
                
                schedule = timetable.get('schedule', [])
                for i, item in enumerate(schedule):
                    pdf.add_schedule_row(item, is_alt=(i % 2 == 0))
                
                pdf.ln(10)
                
                # Add new page if not last day
                if timetable != timetables[-1]:
                    pdf.add_page()
            
            # Save PDF
            filename = f"weekly_timetable_{username}_{datetime.now().strftime('%Y%m%d')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            pdf.output(filepath)
            
            return filepath
        
        except Exception as e:
            print(f"Error generating weekly PDF: {str(e)}")
            return None
    
    def generate_summary_pdf(self,
                            stats: Dict[str, Any],
                            username: str = "User") -> Optional[str]:
        """Generate summary PDF with statistics"""
        try:
            pdf = TimetablePDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            
            # Title
            pdf.add_title_section(
                "Productivity Summary",
                f"Report for {username}"
            )
            
            pdf.add_info_box('Report Date:', datetime.now().strftime('%Y-%m-%d'))
            pdf.ln(10)
            
            # Statistics
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(102, 126, 234)
            pdf.cell(0, 10, 'Your Statistics', 0, 1, 'L')
            
            pdf.add_info_box('Total Timetables:', str(stats.get('total_timetables', 0)))
            pdf.add_info_box('Total Tasks:', str(stats.get('total_tasks', 0)))
            pdf.add_info_box('Chat Messages:', str(stats.get('total_chat_messages', 0)))
            
            if stats.get('last_activity'):
                pdf.add_info_box('Last Activity:', stats['last_activity'][:10])
            
            # Save PDF
            filename = f"summary_{username}_{datetime.now().strftime('%Y%m%d')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            pdf.output(filepath)
            
            return filepath
        
        except Exception as e:
            print(f"Error generating summary PDF: {str(e)}")
            return None
