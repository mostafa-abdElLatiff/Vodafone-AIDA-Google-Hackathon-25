run:
	poetry run env \
		GOOGLE_GENAI_USE_VERTEXAI=1 \
		GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205 \
		GOOGLE_CLOUD_LOCATION=europe-west1 \
		streamlit run frontend/app.py


run-test:
	poetry run env \
		GOOGLE_GENAI_USE_VERTEXAI=1 \
		GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205 \
		GOOGLE_CLOUD_LOCATION=europe-west1 \
		adk run backend/network_incident/

run-web:
	poetry run env \
		GOOGLE_GENAI_USE_VERTEXAI=1 \
		GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205 \
		GOOGLE_CLOUD_LOCATION=europe-west1 \
		adk web


