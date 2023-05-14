# Streamlit chatbot component

# Load libraries
import streamlit as st
from streamlit_chat import message

st.title("OmniBot")

st.text("A chatbot for all your needs")

st.write("""
I can help you with the following:
- [x] Tell you about myself
- [x] Tell you about my creator
- [x] Tell you about my purpose
- [x] Tell you about my future
""")
         
st.image("https://media.giphy.com/media/3o7aDcz3u24RLHj8rm/giphy.gif")

message_history= []

message("Hello, I am OmniBot! How can I help you?")  

message("""
Hello OmniBot! 
My name is Lazaros Paschalidis. 
What do you know about me?
""", is_user=True)  # align's the message to the righ

message("Hello, Lazaros! I know that you used to like programming. Are you still into that?")  

for message_ in message_history:
    message(message_)   # display all the previous message

placeholder = st.empty()  # placeholder for latest message
input_ = st.text_input("you:")
message_history.append(input_)

with placeholder.container():
    message(message_history[-1]) # display the latest message