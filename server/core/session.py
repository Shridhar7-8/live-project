from dataclasses import dataclass
from typing import Dict, Any, Optional
import asyncio



@dataclass
class SessionState:
    """Tracks the session of the client session"""
    is_receiving_response: bool=False
    interrupted: bool=False
    current_tool_execution: Optional[asyncio.Task]=None
    current_audio_stream: Optional[Any]=None
    genai_session: Optional[Any]=None
    received_model_response: Optional[Any]=None


active_sessions: Dict[str, SessionState] = {}


def create_session(session_id: str)->SessionState:
    """Create a new session state"""
    session = SessionState()
    active_sessions[session_id] = session
    return session

def get_session(session_id: str)->Optional[SessionState]:
    """Get a session state"""
    return active_sessions.get(session_id)


def remove_session(session_id: str)->None:
    """Remove a session state"""
    if session_id in active_sessions:
        del active_sessions[session_id]