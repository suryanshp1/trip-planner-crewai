![CrewAI](https://miro.medium.com/v2/resize:fit:1400/0*-7HC-GJCxjn-Dm7i.png)

# 🏖️ Trip Planner: Streamlit with CrewAI

![Streamlit App](images/trip_planner.jpg)

## Introduction

Trip Planner leverages the CrewAI framework to automate and enhance the trip planning experience, integrating a CLI, FASTAPI, and a user-friendly Streamlit interface.


## CrewAI Framework

CrewAI simplifies the orchestration of role-playing AI agents. In VacAIgent, these agents collaboratively decide on cities and craft a complete itinerary for your trip based on specified preferences, all accessible via a streamlined Streamlit user interface.

### Flow Diagram

![Flow Diagram](flow_diagram.svg)

## Running the Application

To experience the VacAIgent app:

- **Configure Environment**: Set up the environment variables for [Browseless](https://www.browserless.io/), [Serper](https://serper.dev/), and [OpenAI](https://openai.com/). Use the `secrets.example` as a guide to add your keys then move that file (`secrets.toml`) to `.streamlit/secrets.toml`.

- **Install Dependencies**: Execute `pip install -r requirements.txt` in your terminal.
- **Launch the CLI Mode**: Run `python cli_app.py -o "Bangalore, India" -d "Krabi, Thailand" -s 2024-05-01 -e 2024-05-10 -i "2 adults who love swimming, dancing, hiking, shopping, food, water sports adventures, rock climbing"` to start the CLI Mode.
- **Launch the FASTAPI**: Run `uvicorn api_app:app --reload` to start the FASTAPI server.
- **Launch the Streamlit App**: Run `streamlit run streamlit_app.py` to start the Streamlit interface.

★ **Disclaimer**: The application uses GEMINI by default. Ensure you have access to GEMINI's API and be aware of the associated costs.

## Details & Explanation

- **Streamlit UI**: The Streamlit interface is implemented in `streamlit_app.py`, where users can input their trip details.
- **Components**:
  - `./trip_tasks.py`: Contains task prompts for the agents.
  - `./trip_agents.py`: Manages the creation of agents.
  - `./tools directory`: Houses tool classes used by agents.
  - `./streamlit_app.py`: The heart of the Streamlit app.

## Using LLM Models

To switch LLMs from differnet Providers

```python
class TripAgents():
    def __init__(self, llm: BaseChatModel = None):
        if llm is None:
            #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            self.llm = LLM(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm

```
[Connect to LLMs](https://docs.crewai.com/how-to/llm-connections#connect-crewai-to-llms)



### Integrating Ollama with CrewAI

Pass the Ollama model to agents in the CrewAI framework:

```python
    agent = Agent(
        role='Local AI Expert',
        goal='Process information using a local model',
        backstory="An AI assistant running on local hardware.",
        llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
    )
```


## Docker Setup

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



## License

Trip Planner is open-sourced under the MIT License.
