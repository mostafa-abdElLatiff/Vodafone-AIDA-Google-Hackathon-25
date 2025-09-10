# inference_client.py
import time

class InferenceClient:
    """
    This is a DUMMY InferenceClient for frontend development.
    It simulates the real backend's response structure.
    """
    def __init__(self):
        print("Initializing DUMMY Inference Client for frontend testing...")

    def predict(self, query: str):
        """
        Simulates a call to the RAG agent and returns a hardcoded,
        structured response in markdown format.
        """
        # Simulate network latency
        time.sleep(1.5)

        # The backend team should produce a response that looks like this
        dummy_markdown_response = """
**Probable Root Cause:** High packet loss is likely due to network congestion on the primary backbone router in the Manchester region, which is consistent with previous incidents.

**Recommended Resolution Steps:**
1. Verify router CPU and memory utilization on `MCR-Primary-Router-01`.
2. Check for active BGP session flaps or routing table anomalies.
3. Consider rerouting traffic through the secondary path via `MCR-Secondary-Router-02`.
4. Escalate to the core networking team if the issue persists after 15 minutes.

**Similar Past Incidents:** `INC00451`, `INC00782`, `INC00901`
"""
        return {
            "answer": dummy_markdown_response,
            "reference": "Analysis based on 3 similar incidents."
        }