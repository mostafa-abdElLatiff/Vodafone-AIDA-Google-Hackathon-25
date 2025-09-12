# agent_client.py

import os
import sys
import logging
from typing import Dict, Any, Optional
from google.cloud import aiplatform
import pandas as pd
import requests

# Add the backend path to sys.path if not already there
# This is crucial for the import to work correctly
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from network_incident.agent import root_agent

# Import necessary ADK components for the Runner
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

logger = logging.getLogger(__name__)

# [AgentClient class remains the same]
# ...


class LocalAgentClient:
    def __init__(self):
        """Initialize the local agent client"""
        self.agent = None
        self.runner = None
        self.session_service = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the ADK agent and its runner"""
        try:
            # The root_agent is the entry point
            self.agent = root_agent
            
            # Use InMemorySessionService for local development
            self.session_service = InMemorySessionService()
            
            # The Runner is what executes the agent
            self.runner = Runner(
                agent=self.agent,
                app_name="network-incident-app",  # A unique name for your app
                session_service=self.session_service
            )
            
            logger.info("Agent and Runner initialized successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import agent: {e}")
            self.agent = None
            self.runner = None
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            self.agent = None
            self.runner = None

    def predict(self, query: str, file_content: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Process query using local agent via the Runner.
        """
        try:
            if self.runner is None:
                return {
                    "answer": "Agent not properly initialized. Please check your setup.",
                    "reference": "Initialization Error"
                }

            user_id = "test_user"
            session_id = "test_session"

            # Create the initial message for the runner
            message_parts = []
            
            if file_content and filename:
                logger.info(f"Processing query with uploaded file: {filename}")
                # Create a ToolCallPart to explicitly invoke the ingestion tool
                tool_call = types.ToolCall(
                    name="ingest_data",  # This must match the tool name in your agent
                    args={"file_content": file_content, "filename": filename}
                )
                message_parts.append(types.Part(tool_call=tool_call))
            
            # Add the user's text query, if it exists
            if query:
                message_parts.append(types.Part(text=query))

            new_message = types.Content(
                role="user",
                parts=message_parts
            )

            logger.info(f"Runner input parts: {new_message.parts}")

            # Call the runner's run method to execute the agent
            events = self.runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message
            )

            # Process the event stream to get the final response
            final_response = None
            for event in events:
                if event.is_final_response():
                    final_response = event.message.parts[0].text
                    
            if final_response:
                return {
                    "answer": final_response,
                    "reference": "Agent Response"
                }
            else:
                return {
                    "answer": "No final response from agent.",
                    "reference": "Processing Error"
                }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "reference": "Processing Error"
            }

    
    def predict(self, query: str, user_id: str, session_id: str, file_content: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Process query using local agent via the Runner.
        """
        try:
            if self.runner is None:
                return {
                    "answer": "Agent not properly initialized. Please check your setup.",
                    "reference": "Initialization Error"
                }

            # Create the initial message for the runner
            message_parts = []
            
            if file_content and filename:
                logger.info(f"Processing query with uploaded file: {filename}")
                # Create a ToolCallPart to explicitly invoke the ingestion tool
                tool_call = types.ToolCall(
                    name="ingest_data",  # This must match the tool name in your agent
                    args={"file_content": file_content, "filename": filename}
                )
                message_parts.append(types.Part(tool_call=tool_call))
            
            # Add the user's text query, if it exists
            if query:
                message_parts.append(types.Part(text=query))

            new_message = types.Content(
                role="user",
                parts=message_parts
            )

            logger.info(f"Runner input parts: {new_message.parts}")

            # Call the runner's run method with the required IDs
            events = self.runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message
            )

            # Process the event stream to get the final response
            final_response = None
            for event in events:
                if event.is_final_response():
                    final_response = event.message.parts[0].text
                    
            if final_response:
                return {
                    "answer": final_response,
                    "reference": "Agent Response"
                }
            else:
                return {
                    "answer": "No final response from agent.",
                    "reference": "Processing Error"
                }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "reference": "Processing Error"
            }