import logging
import asyncio
import os
import websockets
from core.websocket_handler import handle_client


logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper()),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


for logger_name in [
    'google',
    'google.auth',
    'google.auth.transport',
    'google.auth.transport.requests',
    'urllib3.connectionpool',
    'google.genai',
    'websockets.client',
    'websockets.protocol',
    'httpx',
    'httpcore',
]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main function to run the server"""
    port = 8081

    async with websockets.serve(handle_client,
                                "0.0.0.0", 
                                port,
                                ping_interval=30,
                                ping_timeout=10):

        logger.info(f"Server started on port {port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())