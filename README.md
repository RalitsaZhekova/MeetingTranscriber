# Meeting Transcriber

Meeting Transcriber is a Django-based web application for uploading meeting recordings and generating **local, speaker-labeled transcripts**. It is built for practical workflows where users need to upload recordings, separate speakers, review transcripts in the browser, and export results for later use.

The project currently focuses on a reliable backend pipeline that includes file upload, asynchronous processing, media normalization, multilingual transcription, speaker diarization, and transcript export.

## Quick Start

```bash
git clone https://github.com/RalitsaZhekova/MeetingTranscriber.git
cd MeetingTranscriber
python -m venv venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example`:

```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1

HF_TOKEN=your_huggingface_token_here
```

Run the database setup:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Start Redis, Django, and Celery in separate terminals:

```bash
docker start meeting-transcriber-redis
python manage.py runserver
celery -A meeting_transcriber worker --loglevel=info --pool=solo
```

> `--pool=solo` is used because it is the simplest Celery option for local development on Windows.

## Features

- audio and video upload through a Django web interface
- background processing with Celery and Redis
- media normalization with FFmpeg
- local multilingual transcription with `faster-whisper`
- selectable transcription language mode:
  - Auto detect
  - English
  - Bulgarian
- speaker diarization with `pyannote.audio`
- speaker-labeled transcript generation
- transcript export in TXT and JSON
- transcript display in the web UI
- automatic cleanup of temporary processing files

## How It Works

1. A user uploads an audio or video file.
2. Django creates a `TranscriptJob`.
3. Celery processes the job in the background.
4. FFmpeg normalizes the media into a WAV file.
5. `faster-whisper` transcribes the normalized audio.
6. `pyannote.audio` performs speaker diarization.
7. The application aligns transcript segments with speaker segments.
8. The final transcript is saved to the database and exported as TXT and JSON.
9. Temporary processing files are removed after completion or failure.

## Requirements

Before running the project locally, make sure you have:

- Python 3.11 or a compatible version
- Redis
- FFmpeg installed and available in your system `PATH`
- a Hugging Face account
- a Hugging Face token with read access
- accepted access to the `pyannote/speaker-diarization-community-1` model

## Setup Notes

### Hugging Face Access

Speaker diarization requires a Hugging Face token with read access and accepted access to the `pyannote/speaker-diarization-community-1` model.

Add the token to `.env` as `HF_TOKEN`.

### FFmpeg

Verify installation with:

```bash
ffmpeg -version
```

### Redis

Redis must be running before starting the Celery worker.

If you want to run Redis with Docker:

```bash
docker run --name meeting-transcriber-redis -p 6379:6379 -d redis
```

To start it again later:

```bash
docker start meeting-transcriber-redis
```

### Environment Variables

- `HF_TOKEN` is required for diarization model access.
- Keep `.env` private and never commit it.
- Commit `.env.example` instead.

## Using the Application

1. Open the web app in the browser.
2. Upload an audio or video file.
3. Select a transcription language mode:
   - Auto detect
   - English
   - Bulgarian
4. Submit the job.
5. Wait for background processing to finish.
6. Open the job detail page to review:
   - status
   - transcript text
   - TXT output
   - JSON output

## Output Artifacts

For each processed job, the application stores:

- uploaded source media
- normalized audio file
- transcript text in the database
- transcript TXT file
- transcript JSON file

Temporary processing artifacts are removed automatically after the job completes or fails.

## Limitations

Current known limitations:

- speaker diarization is less reliable for:
  - short speaker turns
  - overlapping speech
  - rapid turn-taking
  - speakers with very little speech
- transcript-to-speaker alignment is currently segment-based and can misassign short utterances
- no user authentication yet
- no production deployment configuration yet
- development currently uses SQLite
- PostgreSQL support is planned

## Tech Stack

### Django

Django fits the core workflow well: upload a file, create a job, track status, display results, and export outputs. It also provides a solid ORM, admin interface, and a straightforward path toward production deployment.

### Django Templates

Server-rendered templates are enough for the current stage of the project. Most of the complexity is in the processing pipeline rather than a highly interactive frontend.

### Celery + Redis

Transcription and diarization are long-running operations, so they run outside the request-response cycle. Celery and Redis provide background job execution and a clean path for scaling later.

### FFmpeg

FFmpeg normalizes uploaded recordings into a consistent processing format:

- mono
- 16 kHz
- WAV

This improves transcription and diarization stability.

### faster-whisper

`faster-whisper` provides:

- local transcription
- multilingual support
- strong practical performance
- no required external API costs

### pyannote.audio

`pyannote.audio` is used for speaker diarization, making it possible to generate structured speaker-labeled transcripts instead of plain text output.

## Development Notes

### Database

The current development setup uses SQLite for simplicity.

The long-term plan is to move to PostgreSQL for production. The codebase is being kept migration-friendly by:

- following Django ORM conventions
- avoiding database-specific logic
- keeping the processing state modeled in the application layer

### Windows

Some Hugging Face and audio-related libraries may produce warnings on Windows, especially around:

- symlink-based model cache behavior
- `torchcodec` audio decoding
- FFmpeg shared library issues

The current implementation mitigates the main decoding issue by passing normalized in-memory audio to `pyannote` rather than relying on `torchcodec` file decoding.

## Roadmap

Planned improvements include:

- expected speaker count selection
- better diarization quality for short speaker turns
- improved alignment between transcript and speaker turns
- transcript job list and history page
- safer deletion flow with file cleanup
- PostgreSQL support
- improved UI styling
- user authentication
- deployment configuration
- transcript summarization
- richer transcript exports
