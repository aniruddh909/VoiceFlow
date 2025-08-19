# VoiceFlow AI

A fullstack audio-to-text application that transforms voice recordings into clear, structured text using AI-powered transcription and text refinement. This project replicates AudioPen.ai functionality with modern design and cost-effective local AI processing.

![VoiceFlow Frontend](docs/images/frontend-screenshot.png)

## Features

- **Voice Recording**: Real-time audio recording with microphone integration
- **File Upload**: Support for multiple audio formats (MP3, WAV, M4A)
- **AI Transcription**: Powered by HuggingFace Whisper models for accurate speech-to-text conversion
- **Text Refinement**: AI-powered text improvement with customizable tones and styles
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Cost Effective**: Uses free HuggingFace models instead of expensive OpenAI APIs
- **Local Processing**: All AI processing happens locally for privacy and cost savings

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **HuggingFace Transformers**: AI models for transcription and text processing
- **SQLite**: Lightweight database for storing notes and transcriptions
- **Python 3.9+**: Core backend language with async/await support
- **Uvicorn**: ASGI server for running the FastAPI application

### Frontend
- **React**: Modern JavaScript library for building user interfaces
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/ui**: Modern component library

### AI Models
- **openai/whisper-base**: Speech recognition and transcription
- **microsoft/DialoGPT-medium**: Text refinement and style enhancement

## Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/aniruddh909/VoiceFlow.git
cd VoiceFlow
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration if needed
```

5. Initialize the database:
```bash
python -c "from backend.database.init_db import init_database; init_database()"
```

6. Start the backend server:
```bash
python start_server.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

Note: The frontend code is managed separately and not included in this repository. To set up the frontend:

1. Create a new React project with Vite and TypeScript
2. Install required dependencies (React, Tailwind CSS, Shadcn/ui)
3. Configure Vite proxy to connect to the backend API
4. Implement the UI components for audio recording and transcription

## API Endpoints

### Transcription
- `POST /api/transcribe/upload` - Upload and transcribe audio files
- `POST /api/transcribe/record` - Transcribe recorded audio data

### Text Refinement
- `POST /api/refine/improve` - Improve transcribed text with AI
- `GET /api/refine/tones` - Get available refinement tones

### Notes Management
- `GET /api/notes/` - Retrieve all saved notes
- `POST /api/notes/` - Save a new note
- `PUT /api/notes/{note_id}` - Update an existing note
- `DELETE /api/notes/{note_id}` - Delete a note

## Project Structure

```
VoiceFlow/
├── backend/
│   ├── routes/          # API route handlers
│   ├── services/        # Business logic and AI services
│   ├── database/        # Database models and operations
│   ├── models/          # Pydantic models for request/response
│   └── main.py          # FastAPI application entry point
├── docs/                # Documentation and images
├── .venv/               # Python virtual environment (not tracked)
├── .env                 # Environment variables (not tracked)
├── requirements.txt     # Python dependencies
├── start_server.py      # Server startup script
└── README.md           # This file
```

## Development

### Running in Development Mode

1. Start the backend server:
```bash
source .venv/bin/activate
python start_server.py
```

2. The API will be available at `http://localhost:8000`
3. API documentation available at `http://localhost:8000/docs`

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

Test individual services:
```bash
python test_services.py
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./voiceflow.db

# AI Models
WHISPER_MODEL=openai/whisper-base
DIALOG_MODEL=microsoft/DialoGPT-medium

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Model Configuration

The application uses HuggingFace models that are downloaded automatically on first use:
- Models are cached locally for faster subsequent usage
- GPU acceleration is used if available
- Fallback to CPU processing if GPU is not available

## Deployment

### Production Setup

1. Set environment variables for production:
```bash
export DEBUG=False
export HOST=0.0.0.0
export PORT=8000
```

2. Install production dependencies:
```bash
pip install gunicorn
```

3. Run with Gunicorn:
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port 8000
```

### Docker Deployment

Build and run with Docker:
```bash
docker build -t voiceflow-ai .
docker run -p 8000:8000 voiceflow-ai
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature-name`
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper speech recognition model
- Microsoft for the DialoGPT conversation model
- HuggingFace for providing free access to AI models
- AudioPen.ai for the inspiration and design concepts
