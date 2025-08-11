# import logging
# import sys
# import os
# from typing import Dict, Any


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from config.tools import get_customer_data

# logger = logging.getLogger(__name__)

# Tool_Functions = {
#     "get_customer_data": get_customer_data
# }

# async def execute_tool(tool_name: str, params: Dict[str, Any])-> Dict[str, Any]:
#     """ Execute a tool function """
#     try:
#         if tool_name not in Tool_Functions:
#             logger.error(f"Tool {tool_name} not found")
#             raise ValueError(f"Tool {tool_name} not found")
        
#         tool_function = Tool_Functions[tool_name]  # Access dictionary with square brackets

#         logger.debug(f"Executing tool {tool_name} with params {params}")

#         if callable(tool_function):
#             # Check if the function is a coroutine function (async)
#             import inspect
#             if inspect.iscoroutinefunction(tool_function):
#                 # For async functions, let exceptions propagate
#                 return await tool_function(**params)
#             else:
#                 # For regular functions, let exceptions propagate
#                 return tool_function(**params)
#         else:
#             logger.error(f"Tool {tool_name} is not callable")
#             raise ValueError(f"Tool {tool_name} is not callable")
#     except Exception as e:
#         logger.error(f"Failed to execute tool {tool_name}: {e}")
#         raise


import logging
import aiohttp
from typing import Dict, Any
from config.config import CLOUD_FUNCTIONS
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

async def execute_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool based on name and parameters by calling the corresponding cloud function"""
    try:
        if tool_name not in CLOUD_FUNCTIONS:
            logger.error(f"Tool not found: {tool_name}")
            return {"error": f"Unknown tool: {tool_name}"}

        base_url = CLOUD_FUNCTIONS[tool_name]
        query_string = urlencode(params)
        function_url = f"{base_url}?{query_string}" if params else base_url
        
        logger.debug(f"Calling cloud function for {tool_name}")
        logger.debug(f"URL with params: {function_url}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(function_url) as response:
                response_text = await response.text()
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                logger.debug(f"Response body: {response_text}")
                
                if response.status != 200:
                    logger.error(f"Cloud function error: {response_text}")
                    return {"error": f"Cloud function returned status {response.status}"}
                
                try:
                    return await response.json()
                except Exception as e:
                    logger.error(f"Failed to parse JSON response: {response_text}")
                    return {"error": f"Invalid JSON response from cloud function: {str(e)}"}

    except aiohttp.ClientError as e:
        logger.error(f"Network error calling cloud function for {tool_name}: {str(e)}")
        return {"error": f"Failed to call cloud function: {str(e)}"}
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        return {"error": f"Tool execution failed: {str(e)}"} 
    