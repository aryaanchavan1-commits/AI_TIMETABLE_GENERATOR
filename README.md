# 📅 AI Timetable Generator

An intelligent productivity app powered by AI that creates personalized timetables based on your tasks, goals, and productivity techniques.

## ✨ Features

### 🤖 AI-Powered Timetable Generation
- Uses Groq API for intelligent schedule creation
- Considers your tasks, goals, and preferences
- Real-life based schedules with sleep cycles and Pomodoro technique
- Motivational messages and productivity tips

### 🔐 User Authentication
- Secure login and registration system
- Password hashing with bcrypt
- Session management
- User preferences storage

### 📊 History & Analytics
- Save all timetables and tasks
- Chat history with AI assistant
- Export/import data functionality
- User statistics and insights

### 🛠️ Productivity Techniques
- **Pomodoro Timer**: 25/5 work/break cycles
- **Sleep Optimizer**: Calculate optimal bedtime
- **Focus Mode**: Distraction-free work sessions
- **Time Blocking**: Schedule your day in blocks
- **Eisenhower Matrix**: Prioritize tasks effectively

### 📥 PDF Generation
- Beautiful, downloadable PDF timetables
- Weekly timetable summaries
- Productivity reports
- Custom styling and formatting

### 💬 AI Chat Assistant
- Ask questions about productivity
- Get personalized advice
- Context-aware responses
- Chat history saved

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (get it from https://console.groq.com/)

### Step 1: Clone the Repository
```bash
git clone https://github.com/aryaanchavan1-commits/AI_TIMETABLE_GENERATOR.git
cd AI_TIMETABLE_GENERATOR
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```


### Step 3: Run the Application
```bash
streamlit run app.py
```



## 📁 Project Structure

```
timetable_generator_ai/
├── app.py                 # Main Streamlit application
├── auth.py                # Authentication system
├── database.py            # Database operations
├── ai_generator.py        # AI timetable generation
├── pdf_generator.py       # PDF generation
├── productivity.py        # Productivity techniques
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    ├── config.toml       # Streamlit configuration
    └── secrets.toml      # API keys and secrets
```

## 🎯 How to Use

### 1. Register/Login
- Create a new account or login with existing credentials
- Your data is securely stored locally

### 2. Create Timetable
- Add your tasks with duration and priority
- Set short-term and long-term goals
- Configure your preferences (wake time, sleep time, etc.)
- Click "Generate Timetable" to create your personalized schedule

### 3. Use Productivity Tools
- **Pomodoro Timer**: Start focused work sessions
- **Sleep Optimizer**: Calculate your optimal bedtime
- **Focus Mode**: Work without distractions
- **Time Blocking**: Plan your day in blocks
- **Eisenhower Matrix**: Prioritize tasks

### 4. Chat with AI
- Ask questions about productivity
- Get personalized advice
- Discuss your goals and challenges

### 5. View History
- Access all your past timetables
- Review completed tasks
- Export your data anytime

## 🔧 Configuration

### Streamlit Configuration
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

### User Preferences
Set your default preferences in Settings:
- Wake up time
- Sleep time
- Work hours
- Break preferences
- Focus areas

## 📊 Data Storage

All data is stored locally in JSON files:
- `users.json`: User accounts and authentication
- `database.json`: Timetables, tasks, and chat history
- `generated_pdfs/`: Generated PDF files

## 🛡️ Security

- Passwords are hashed using bcrypt
- User sessions are managed securely
- API keys are stored in Streamlit secrets
- All data is stored locally

## 🎨 Customization

### Adding New Productivity Techniques
Edit `productivity.py` to add new techniques:
```python
class NewTechnique:
    def __init__(self):
        # Initialize your technique
        pass
    
    def render_widget(self):
        # Render your widget
        pass
```

### Modifying AI Prompts
Edit `ai_generator.py` to customize AI behavior:
- Modify `_get_system_prompt()` for different AI personality
- Adjust `_create_user_context()` for different input formats
- Customize `_create_fallback_timetable()` for default schedules

### Changing PDF Style
Edit `pdf_generator.py` to customize PDF appearance:
- Modify colors in `_get_type_color()`
- Adjust layout in `add_schedule_row()`
- Add new sections as needed

## 🐛 Troubleshooting

### API Key Error
If you see "Groq API key not found":
1. Check that `.streamlit/secrets.toml` exists
2. Verify your API key is correct
3. Restart the Streamlit app

### Import Errors
If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Groq for the powerful AI API
- FPDF2 for PDF generation
- All productivity technique creators (Pomodoro, Eisenhower, etc.)

---

**Made with ❤️ for productivity enthusiasts by aryan chavan **
