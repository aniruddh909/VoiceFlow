# 🎤 VoiceFlow AI

A modern fullstack audio-to-text application that transforms voice recordings into clear, structured text using AI. Built as a clone of AudioPen.ai with unique design and enhanced features.

## ✨ Features

- **🎙️ Audio Recording & Upload**: Record directly in browser or upload MP3, WAV, M4A files
- **🤖 AI Transcription**: Powered by OpenAI Whisper for accurate speech-to-text
- **✨ Smart Text Refinement**: Use GPT-4 to improve grammar, structure, and clarity
- **🎨 Tone Customization**: Choose between casual, formal, or "like me" styles
- **📝 Custom Prompts**: Create personalized refinement instructions
- **💾 Note Management**: Save, view, edit, and export your transcriptions
- **📱 Responsive Design**: Clean, modern interface that works on all devices

## 🏗️ Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework for building APIs
- **OpenAI Whisper** - State-of-the-art speech recognition
- **OpenAI GPT-4** - Advanced text refinement and style adjustment
- **SQLite** - Lightweight database for development
- **AsyncIO** - Asynchronous processing for better performance

### Frontend

- **HTML5 + Tailwind CSS** - Modern, responsive design system
- **Vanilla JavaScript** - Clean, dependency-free frontend
- **Web Audio API** - Browser-based audio recording
- **Lucide Icons** - Beautiful, consistent iconography

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone and navigate to the project**:

   ```bash
   cd VoiceFlow
   ```

2. **Set up the backend**:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Initialize the database**:

   ```bash
   python init_db.py
   ```

5. **Start the backend server**:

   ```bash
   python main.py
   ```

6. **Open the frontend**:
   Navigate to `http://localhost:8000/static/index.html` in your browser

## 📖 Usage

### Recording Audio

1. Click "Start Recording" to begin voice recording
2. Speak clearly and click "Stop Recording" when finished
3. The audio will be automatically transcribed

### Uploading Files

1. Click "Upload File" or drag and drop audio files
2. Supported formats: MP3, WAV, M4A, MP4
3. Files are processed immediately after upload

### Refining Text

1. After transcription, choose your preferred tone:
   - **Casual**: Conversational and relaxed
   - **Formal**: Professional and structured
   - **Like Me**: Preserves your personal style
2. Click "Refine Text" to improve the transcription
3. Copy, export, or save the refined text

### Managing Notes

- View all your previous transcriptions in the history section
- Click "View" to reload a note for further editing
- Export notes as TXT files
- Delete notes you no longer need

## 🛠️ API Endpoints

### Transcription

- `POST /api/transcribe/upload` - Upload and transcribe audio
- `GET /api/transcribe/status/{note_id}` - Get transcription status

### Text Refinement

- `POST /api/refine/improve` - Refine transcribed text
- `POST /api/refine/custom-prompt` - Save custom prompts
- `GET /api/refine/tones` - Get available tone options

### Notes Management

- `GET /api/notes/` - Get all notes with pagination
- `GET /api/notes/{note_id}` - Get specific note
- `DELETE /api/notes/{note_id}` - Delete note
- `GET /api/notes/{note_id}/export` - Export note

## 🔧 Configuration

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
DATABASE_URL=sqlite:///voiceflow.db
HOST=0.0.0.0
PORT=8000
DEBUG=True
MAX_FILE_SIZE_MB=25
```

### Customization

- **Audio Limits**: Adjust `MAX_FILE_SIZE_MB` in environment variables
- **Tone Prompts**: Modify prompts in `services/gpt_service.py`
- **UI Styling**: Customize colors and styling in `frontend/index.html`
- **Database**: Switch to PostgreSQL by updating `services/db.py`

## 🚀 Deployment

### Development

```bash
python main.py
```

### Production (Docker)

```bash
# Build and run with Docker
docker build -t voiceflow-ai .
docker run -p 8000:8000 voiceflow-ai
```

### Cloud Deployment

The app is ready for deployment on:

- **Render**: Use the provided `render.yaml`
- **Railway**: Connect your GitHub repo
- **Fly.io**: Use the provided `fly.toml`
- **Heroku**: Add Procfile for deployment

## 📝 Development Notes

### Adding New Features

1. **Backend**: Add routes in `routes/` and services in `services/`
2. **Frontend**: Extend the `VoiceFlowApp` class in `js/app.js`
3. **Database**: Update schema in `services/db.py`

### Code Structure

```
backend/
├── main.py              # FastAPI application entry point
├── routes/              # API route handlers
├── services/            # Business logic and external APIs
├── init_db.py           # Database initialization
└── requirements.txt     # Python dependencies

frontend/
├── index.html           # Main UI interface
├── js/app.js           # Frontend application logic
└── styles/             # Additional CSS (if needed)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT-4 APIs
- FastAPI team for the excellent framework
- Tailwind CSS for the design system
- AudioPen.ai for inspiration

## 📞 Support

For questions or issues:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

**Built with ❤️ using GitHub Copilot and VS Code**
