# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_Research: Research advice, related literature finding, research area proposals, web knowledge access."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
# from .sub_agents.incident_ingestion import incident_ingestion_agent
from .sub_agents.resolution_suggestion import resolution_suggestion_agent
from .sub_agents.uploader import uploader_agent

MODEL = "gemini-2.5-flash"


network_incident = LlmAgent(
    name="network_incident",
    model=MODEL,
    description=(
            """
You are a Network Incident Router Agent that directs user requests to the right specialist agent.
Your job is simple:

Agent 1: If a user asks questions about network problems, troubleshooting, or incident resolution → route to the Network Resolution Agent. 
This agent can handle filtering and counting because it has advanced search capabilities. Just pass it the user query.

Agent 2: If a user asks to upload a file → route to Uploader Agent
Keep responses direct and helpful:

Don't generate code or technical implementations
Don't over-explain the routing process
Simply execute the appropriate agent and return their response
If both file upload and question are present, handle the file first, then answer the question
"""
    ),
    instruction=prompt.ROUTER_AGENT_PROMPT,
    tools=[
    AgentTool(agent=uploader_agent),
    AgentTool(agent=resolution_suggestion_agent),
    
]

)

root_agent = network_incident
