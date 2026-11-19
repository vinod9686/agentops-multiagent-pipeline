# config.py -- every setting for every service, read from the environment
import os
from dotenv import load_dotenv

# Reads .env when running locally; inside Docker the same variables
# arrive through env_file / environment in docker-compose.yml.
load_dotenv()

# ---- settings for the agent services (researcher, writer, reviewer)
ROLE = os.getenv("ROLE", "researcher")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
# Fault injection, so we can practise failure handling on purpose
FAIL_RATE = float(os.getenv("FAIL_RATE", "0"))  # 0.3 = fail 30% of calls
DELAY_MS = int(os.getenv("DELAY_MS", "0"))      # extra waiting time per call

# ---- settings for the orchestrator
RESEARCHER_URL = os.getenv("RESEARCHER_URL", "http://localhost:8001")
WRITER_URL = os.getenv("WRITER_URL", "http://localhost:8002")
REVIEWER_URL = os.getenv("REVIEWER_URL", "http://localhost:8003")
TIMEOUT_S = float(os.getenv("TIMEOUT_S", "10"))       # give up on a call
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))      # extra tries per call
BACKOFF_S = float(os.getenv("BACKOFF_S", "0.5"))      # first wait; doubles
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "1"))  # rewrite rounds
LOG_FILE = os.getenv("LOG_FILE", "logs/events.jsonl")
STUDENT_SRN = os.getenv("STUDENT_SRN", "UNKNOWN")
