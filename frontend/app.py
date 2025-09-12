import base64
import streamlit as st
import pandas as pd
import uuid
from typing import List, Dict
from agent_client import LocalAgentClient

# Use a singleton pattern to ensure the client is only created once
@st.cache_resource
def get_agent_client():
    """
    Initializes and returns a single instance of the LocalAgentClient.
    This function will only run once.
    """
    return LocalAgentClient()


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def add_message(role, content, message_type):
    """Function to add a message to the session state"""
    if message_type == "text":
        st.session_state.messages.append({'role': role, 'content': content})
    if message_type == "style":
        st.session_state.styled_messages.append({'role': role, 'content': content})


def rag_backend(agent_client,
                user_id: str,
                session_id: str,
                query: str,
                messages: List,
                counter: int,
                uploaded_data: str = None
               ):
    """Send the query to the agent client and get the response"""
    
    if uploaded_data:
        # Read file as bytes
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        
        # Make sure both are passed
        response = agent_client.predict(
            query=query,
            user_id=user_id, # Pass the stored user ID
            session_id=session_id, # Pass the stored session ID
            file_content=file_bytes,  # This should be bytes, not None
            filename=filename         # This should be string, not None
        )
    else:
        # No file uploaded
        response = agent_client.predict(
            query=query,
            user_id=user_id, # Pass the stored user ID
            session_id=session_id # Pass the stored session ID
        )

    return response
        
def main():

    # Load favicon file (app logo image)
    img_path = "frontend/vodafone.png"
    img = get_base64(img_path)

    # Set the title of the Streamlit app
    title = "Network Incident Resolution Assistant-team 5"
    description = "AI-powered assistant to help network engineers resolve incidents faster by retrieving similar past incidents and suggesting probable resolutions."
    
    # Set the page configuration
    st.set_page_config(
        page_title=title,
        page_icon=f'data:image/png;base64,{img}',
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Display logo, header and description
    st.logo(img_path, size='large')
    st.title(title)
    st.info(description, icon=":material/description:")
        
    # Create an instance of the AgentClient for each session
    # if "agent_client" not in st.session_state:
    #     st.session_state.agent_client = LocalAgentClient()

    # Get the client instance
    agent_client = get_agent_client()
        
    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "styled_messages" not in st.session_state:
        st.session_state.styled_messages = []

    # Initialize a counter for the user queries
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    # 1. Initialize user_id and session_id in st.session_state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4()) # Generate a unique ID for the user
        
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4()) # Generate a unique ID for the conversation


    # Display existing chat history
    for message in st.session_state.styled_messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'], unsafe_allow_html=True)

    # Add Sidebar for uploading the data
    with st.sidebar:
        st.header("Upload Data")
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
        
        # Add instructions for ingestion
        st.info("💡 **To ingest data:** Upload a file and then type 'ingest this data' in the chat")
    
        # Check if a file has been uploaded
        if uploaded_file is not None:
            try:
                # Determine the file type and read it with pandas
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                
                # Display a success message and the first few rows of the data
                st.sidebar.success("File uploaded successfully!")
                st.sidebar.subheader("Uploaded Data Preview:")
                st.sidebar.dataframe(df.head())
            
                # Now you can use the DataFrame 'df' for further processing
                # For example, you can convert the DataFrame to a string
                # and pass it to your RAG backend
                uploaded_data_str = df.to_string()
                st.session_state.uploaded_data = uploaded_data_str
        
            except Exception as e:
                st.sidebar.error(f"Error reading the file: {e}")
    
    # Chat input
    if prompt := st.chat_input("Enter your query"):

        with st.chat_message('user'):
            st.markdown(prompt)

        # Increment the counter
        st.session_state.counter += 1
        
        # Add user messages to both session state messages and styled_messages
        add_message('user', prompt, "text")
        add_message('user', prompt, "style")

        
        # Generate AI response
        uploaded_data = st.session_state.get('uploaded_data', None)
        response = rag_backend(agent_client, st.session_state.user_id, st.session_state.session_id, prompt, st.session_state.messages, st.session_state.counter, uploaded_data)
        answer = response['answer']
        # reference = response[1] 

        # Display ai response
        with st.chat_message('assistant'):
            footer = "<small style='color: gray; float: right; margin-top: 20px;'>AI-generated content may be incorrect</small>"
            styled_answer = f"{answer}<br>{footer}"
            st.markdown(styled_answer, unsafe_allow_html=True)

        # Add assistant messages to both session state messages and styled_messages
        add_message('assistant', answer, "text")
        add_message('assistant', styled_answer, "style")

if __name__ == "__main__":
    main()