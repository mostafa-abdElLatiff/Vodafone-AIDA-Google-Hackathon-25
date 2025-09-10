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

"""Academic_websearch_agent for finding research papers using search tools."""

from google.adk import Agent
from google.adk.tools import google_search
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt

MODEL = "gemini-2.5-pro"


# academic_websearch_agent = Agent(
#     model=MODEL,
#     name="academic_websearch_agent",
#     instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
#     output_key="recent_citing_papers",
#     tools=[google_search],
# )
# from adk import LlmAgent, AgentTool
# import prompt  # assuming prompt.py is in the same directory

resolution_suggestion_agent = LlmAgent(
    name="resolution_suggestion_agent",
    model=MODEL,
    description=(
        "This agent accepts a natural language query from a network engineer describing a current issue. "
        "It searches the vector database for similar past incidents, summarizes historical resolutions and probable root causes, "
        "and suggests recommended resolution steps."
    ),
    instruction=prompt.RESOLUTION_SUGGESTION_PROMPT,
    output_key="resolution_summary"
)
