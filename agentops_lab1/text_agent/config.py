# config.py -- the ONLY place that reads settings from the environment
import os
from dotenv import load_dotenv

# Reads the .env file if one exists next to this code (local runs).
# Inside Docker there is no .env file; the same variables arrive
# through --env-file instead.
# load_dotenv() never overwrites a variable that is already set,
# so the values supplied by Docker win.
load_dotenv()

STUDENT_SRN = os.getenv("STUDENT_SRN", "UNKNOWN") # NEW in this experiment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3.8-27b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "2000"))
