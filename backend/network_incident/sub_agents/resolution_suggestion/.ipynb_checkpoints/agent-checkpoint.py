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

"""Resolution suggestion agent for network incident resolution."""

from google.adk.agents import LlmAgent
from . import prompt
from .retrieval_tool import incident_retrieval_tool
# from configs.config import RAG_PROMOT

# # Define the new instruction to directly call the tool
# DIRECT_TOOL_CALL_PROMPT = """
# You are a tool-calling assistant.
# You must use the 'incident_retrieval_tool' to retrieve historical incident data based on the user's query.
# Do not reason or generate a summary. Simply call the tool with the user's query as the argument.
# The user's query is: {{user_query}}
# """

MODEL = "gemini-2.5-flash"

resolution_suggestion_agent = LlmAgent(
    name="resolution_suggestion_agent",
    model=MODEL,
    description=(
"""
You are a Network Incident Assistant. Your goal is to help engineers quickly understand and resolve network issues.
Your search tool is very powerful because can handle filtering and counting because it has advanced search capabilities. Just pass it the user query.

### What you do:
1. Read the incident description provided by the engineer.
2. Ask for missing key details if needed (severity, impacted location, affected services).
3. Use the vector search tool to find similar past incidents, their root causes, and resolution steps.
4. Summarize findings and suggest possible root causes and recommended actions.
 
### Response format:
- **Summary:** Short description of the issue.
- **Clarifying Questions (if needed):** Up to 3 questions to get severity, location, or scope.
- **Possible Root Causes:** Ranked list based on retrieved incidents.
- **Suggested Resolution Steps:** Practical, safe actions based on historical fixes.
- **Confidence Level:** Low / Medium / High.
 
### Rules:
- Be clear and concise.
- Do not guess if unsure; say what info is missing.
- Always base suggestions on retrieved evidence.
"""
    ),
    instruction=prompt.RESOLUTION_SUGGESTION_PROMPT,
    tools=[incident_retrieval_tool],
    output_key="resolution_summary"
)
