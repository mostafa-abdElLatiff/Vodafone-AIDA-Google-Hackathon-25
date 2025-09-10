import base64
import streamlit as st
from typing import List, Dict
from inference_client import InferenceClient


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


def rag_backend(inference_client,
                query: str,
                messages: List,
                counter: int,
               ):
    """Send the query to the inference client and get the LLM response"""
    number_of_qa_to_preserve = (5 * 2) + 1
    if len(messages) > number_of_qa_to_preserve:
        messages = messages[-number_of_qa_to_preserve:]
    
    # We perform a try/catch block in case we get an error from the RAI 
    try:
        print("query is: ",query)
        response = inference_client.predict(query)
    
    except ValueError as e:
        error = str(e).split('scanner: ')[1].split('with')[0].strip()
        
        response = f'Query rejected by the Responsible AI Service for {error}'
        return response, 'No Reference'
    
    except:
        response = 'Query rejected by the Responsible AI Service'
        return response, 'No Reference'
    
    return response['answer'], response['reference']

    
def main():

    # Load favicon file (app logo image)
    img_path = "./vodafone.png"
    img = get_base64("./vodafone.png")

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
        
    # Create an instance of the InferenceClient for each session
    if "inference_client" not in st.session_state:
        st.session_state.inference_client = InferenceClient()
        
    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "styled_messages" not in st.session_state:
        st.session_state.styled_messages = []

    # Initialize a counter for the user queries
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    # Display existing chat history
    for message in st.session_state.styled_messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'], unsafe_allow_html=True)
            
    
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
        response = rag_backend(st.session_state.inference_client, prompt, st.session_state.messages, st.session_state.counter)
        answer = response[0]
        reference = response[1] 

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