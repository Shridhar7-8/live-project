import os
import logging
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from google.cloud import secretmanager
from google import genai

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Exception raised for configuration errors"""
    pass


def get_secret(secret_id: str) -> str:
    """Get secret from secret manager"""
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("PROJECT_ID")

    if not project_id:
        raise ConfigurationError("PROJECT_ID environment variable is not set")

    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version({"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise


class APIConfig:
    def __init__(self):
        # Determine if using Vertex AI
        self.use_vertex = os.getenv("VERTEX_API", "false").lower() == "true"
        self.api_key: Optional[str] = None

        logger.info(f"Initialized APIConfig with use_vertex={self.use_vertex}")

    async def initialize(self):
        if not self.use_vertex:
            try:
                self.api_key = get_secret("GOOGLE_API_KEY")
            except Exception as e:
                logger.info("Failed to get GOOGLE_API_KEY from secret manager")
                self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ConfigurationError("GOOGLE_API_KEY is not set")


api_config = APIConfig()


if api_config.use_vertex:
    MODEL = os.getenv('MODEL_VERTEX_API', 'gemini-2.0-flash-exp')
    VOICE = os.getenv('VOICE_VERTEX_API', 'Aoede')
else:
    MODEL = os.getenv('GOOGLE_API_KEY', 'models/gemini-2.0-flash-live-001')
    VOICE = os.getenv('VOICE_GOOGLE_API', 'Aoede')


# Add your deployed cloud function URL here
CLOUD_FUNCTIONS = {
    "get_customer_data": os.getenv('SHEET_FUNCTION_URL')
}

# Validate the cloud function URL
for name, url in CLOUD_FUNCTIONS.items():
    if not url:
        logger.warning(f"Missing {name} function URL")
    elif not url.startswith("https://"):
        logger.warning(f"Invalid {name} function URL: {url}")


# Load system instructions
try:
    with open("config/system-instruction.txt", "r") as f:
        SYSTEM_INSTRUCTIONS = f.read()
except FileNotFoundError:
    logger.warning("system-instruction.txt not found, using default")
    SYSTEM_INSTRUCTIONS = ""

logger.info(f"System instructions: {SYSTEM_INSTRUCTIONS}")


CONFIG = {
    "generation_config": {
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}
        },
    },
    "system_instruction": SYSTEM_INSTRUCTIONS,
    "tools": [{
        "function_declarations": [
            {
                "name": "get_customer_data",
                "description": "Retrieves customer data from a specified Google Sheet using the customer's account ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {
                            "type": "string",
                            "description": "The customer's account ID (required) to search for in the Google Sheet."
                        },
                        "sheet_name": {
                            "type": "string",
                            "description": "Optional name of the Google Sheet to search. Defaults to 'Synthetic_Bank_Customer_Records_new' if not provided."
                        }
                    },
                    "required": ["customer_id"]
                }
            }
        ],
    },
    {"code_execution": {}},
    {"google_search": {}}
    ]
}
