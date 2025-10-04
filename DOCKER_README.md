# Trip Planner - Docker Setup

This document explains how to run the Trip Planner application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t trip-planner .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 --env-file .env trip-planner
   ```

## Environment Variables

Make sure to create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
# Add other required environment variables
```

## Accessing the Application

Once the container is running, you can access the application at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://0.0.0.0:8501

## Health Check

The application includes a health check that monitors the Streamlit server. You can check the health status with:

```bash
docker-compose ps
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port mapping in `docker-compose.yaml` from `8501:8501` to `8502:8501`
   - Access the app at http://localhost:8502

2. **Environment variables not loaded:**
   - Ensure your `.env` file is in the project root
   - Check that the `.env` file has the correct format

3. **Build failures:**
   - Check that all dependencies in `requirements.txt` are compatible with Python 3.13
   - Try rebuilding with `docker-compose up --build --no-cache`

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs trip-planner
```

## Development

For development, you might want to mount the source code as a volume:

```yaml
# Add to docker-compose.yaml under volumes
- .:/app
```

This allows you to see changes without rebuilding the image.
