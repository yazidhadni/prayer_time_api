# Prayer Time API

A simple API that fetches and returns prayer times from a third-party service.
This project demonstrates how to interact with external APIs, implement caching, and manage environment variables in a backend application.

## Features

- Fetch prayer times from a third-party API
- Cache responses to reduce unnecessary requests [**TODO**]
- Configure API keys and settings using environment variables [**TODO**]

### Prerequisites
- python >= 3.13
- uv

#### Backend

```bash
cd backend
uv sync
```

### Running the app locally
uvicorn src.prayer_times.main:app --reload
**note:** --reload: automatically reloads the server when you change code, which is perfect for development.