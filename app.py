## loading all the environment variables
from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
from PIL import Image
import PIL.Image
import google.generativeai as genai
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# ------------------------Gemini Api------------------------------------

## function to load Gemini Pro model and get repsonses
def get_gemini_response(question):
    model=genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response=chat.send_message(question)
    # Uncomment the below line if you want to stream the conversation 
    # response=chat.send_message(question,stream=True)
    return response

##Function to load Gemini Pro vision Model 
def get_gemini_vision_response(uploaded_image,txt_input):
    
    model=genai.GenerativeModel("gemini-pro-vision")
    chat = model.start_chat(history=[])
    img = PIL.Image.open(uploaded_image)
    response = model.generate_content([txt_input,img])
    # Uncomment the below line if you want to stream the conversation 
    # response = model.generate_content([txt_input,img],stream=True)
    return response
# -----------------------------------Gemini----------------------------------


##initialize our streamlit app

# ----------------------------Header--------------------------------
st.set_page_config(page_title="Synclo AI Diagnose")
c30, c31, c32 = st.columns([0.2, 0.1, 1.5])
with c30:
    st.caption("")
    st.image("synclo-logo.png",width = 95)
with c32:
    st.title(" Talk🗣️ with your Medical Images and Reports ")
# ----------------------------------------------------------------------

# ---------------------------------Welcome Balooons----------------
# st.balloons()
# -----------------------------------------------------------------




# ------------------Tabs------------------------------------
tab1, tab2 = st.tabs(([":blue[**Chat**]", ":blue[**Chat with image**]"]))
with tab1:
    st.header("")
with tab2:
    # st.header("image")
    uploaded_image = st.file_uploader("Upload your Image", type=["jpg", "jpeg", "png"])

# -----------------------------------------------------

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


# -----------------------Input Text session------------------------------
if 'something' not in st.session_state:
    st.session_state.something = ''

def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''

st.text_input('Something', key='widget', on_change=submit)
txt_input = st.session_state.something
submit = st.button("Ask..")
# ---------------------------------------------------------------------------

if txt_input or submit  :

    users = st.chat_message("user")
    users.markdown( txt_input)
    response  = ""
    if uploaded_image:
        if txt_input == "":
            txt_input = "Read the given Image and tell me a short blog about it."
        response = get_gemini_vision_response(uploaded_image,txt_input)
    else:
        if txt_input:
            response=get_gemini_response(txt_input)
        else:
            st.warning("Please Enter some prompt...")

    if uploaded_image:
        st.image(uploaded_image, width = 200)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You ", txt_input))
    message = st.chat_message("assistant")
    for chunk in response:
        message.write(chunk.text)
        st.session_state['chat_history'].append(("Bot ", chunk.text))
    


# ---------------------------History Section--------------------------------
with st.expander("History"):
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
# -------------------------------------------------------------------------- 
