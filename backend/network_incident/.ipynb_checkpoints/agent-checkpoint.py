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
from .sub_agents.incident_ingestion import incident_ingestion_agent
from .sub_agents.resolution_suggestion import resolution_suggestion_agent

MODEL = "gemini-2.5-pro"


network_incident = LlmAgent(
    name="network_incident",
    model=MODEL,
    description=(
            "This Router Agent acts as a controller that dynamically selects the appropriate downstream agent based on input context. If the input is a structured dataset (e.g., Excel file), it invokes the Incident Ingestion Agent to process and index incidents. If the input is a natural language query from an engineer, it invokes the Resolution Suggestion Agent to retrieve similar incidents and generate resolution insights."
    ),
    instruction=prompt.ROUTER_AGENT_PROMPT,
    tools=[
    AgentTool(agent=incident_ingestion_agent),
    AgentTool(agent=resolution_suggestion_agent),
]

)

root_agent = network_incident
