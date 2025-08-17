<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# VoiceFlow AI - Copilot Instructions

## Project Overview

This is a fullstack audio-to-text application that replicates AudioPen.ai functionality with modern design and AI-powered text refinement. The app transforms voice recordings into clear, structured text using OpenAI Whisper and GPT-4.

## Code Style & Standards

### Backend (Python/FastAPI)

- Use async/await for all database and API operations
- Follow FastAPI best practices with proper dependency injection
- Implement comprehensive error handling with HTTPException
- Use Pydantic models for request/response validation
- Maintain type hints throughout the codebase
- Follow PEP 8 style guidelines

### Frontend (JavaScript)

- Use ES6+ class-based architecture
- Implement async/await for API calls
- Follow modern JavaScript best practices
- Use consistent naming conventions (camelCase)
- Add comprehensive error handling for user interactions

### Database

- Use async SQLite operations with aiosqlite
- Implement proper database connection management
- Use UUID for primary keys
- Add appropriate indexes for performance
- Handle database migrations properly

## Architecture Patterns

### API Design

- RESTful endpoints with clear naming
- Consistent response formats with success/error indicators
- Proper HTTP status codes
- Request validation and sanitization

### Service Layer

- Separate business logic from route handlers
- Use dependency injection for services
- Implement proper error propagation
- Add logging for debugging and monitoring

### Frontend Architecture

- Single-page application with vanilla JavaScript
- Event-driven architecture for user interactions
- State management for current note and UI state
- Modular component-like structure

## AI Integration Guidelines

### OpenAI Services

- Use proper API key management through environment variables
- Implement rate limiting and retry logic
- Handle API errors gracefully with user feedback
- Use appropriate model parameters for different use cases

### Audio Processing

- Support multiple audio formats (MP3, WAV, M4A)
- Validate file types and sizes before processing
- Handle temporary file cleanup properly
- Provide progress indicators for long operations

## Security Considerations

- Validate all user inputs
- Sanitize file uploads
- Use environment variables for sensitive data
- Implement proper CORS configuration
- Add request size limits

## Performance Guidelines

- Use async operations for I/O bound tasks
- Implement proper caching where appropriate
- Optimize database queries with indexes
- Handle large file uploads efficiently
- Use connection pooling for external APIs

## Error Handling

- Provide meaningful error messages to users
- Log errors for debugging purposes
- Implement graceful degradation for API failures
- Use try-catch blocks appropriately
- Return proper HTTP status codes

## Testing Approach

- Write unit tests for service layer functions
- Test API endpoints with different scenarios
- Validate error handling paths
- Test file upload and processing workflows
- Ensure frontend JavaScript handles API errors

## Development Workflow

- Use feature branches for new functionality
- Write descriptive commit messages
- Update documentation when adding features
- Test locally before committing changes
- Follow the project's file structure conventions

## Deployment Considerations

- Use environment-specific configurations
- Implement proper logging for production
- Handle database migrations safely
- Configure CORS for production domains
- Set up monitoring and health checks

When generating code for this project, please follow these guidelines and maintain consistency with the existing codebase structure and patterns.
