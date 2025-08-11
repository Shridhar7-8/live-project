import logging 
import os
from google import genai
from config.config import CONFIG, api_config, ConfigurationError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


MODEL = "models/gemini-2.0-flash-live-001"



async def create_gemini_session():
    """Create a Gemini session"""
    try:
        await api_config.initialize()

        if api_config.use_vertex:
            
            location = os.getenv("VERTEX_LOCATION", "us-central1")
            project_id = os.getenv("PROJECT_ID")
            
            if not project_id:
                raise ConfigurationError("PROJECT_ID environment variable is not set")

            logger.info(f"initializing vertex AI for location {location} and project_id {project_id}")

            client  = genai.Client(
                vertexai=True,
                project_id=project_id,
                location=location
            )

            logger.info(f"Vertex AI initialized with client {client}")

        else:
            logger.info("initializing developement client")

            client = genai.Client(
                vertexai=False,
                http_options={"api_version": "v1alpha"},
                api_key=api_config.api_key
            )

        session = client.aio.live.connect(
            model = MODEL,
            config=CONFIG
        )

        return session

    except ConfigurationError as e:
        logger.error(f"Failed to create Gemini session: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create Gemini session: {e}")
        raise
    