# Description: A playground for testing Streamlit features

import streamlit as st

def main(chat_text):
    print("RUN MAIN")

    # Create a container to hold the elements
    container = st.container()

    # Add the elements to the container
    with container:

        # Create a placeholder for the chat text
        chat_placeholder = st.empty()

        # Display the chat text
        for text in chat_text:
            chat_placeholder.text(text)

        # Input text field
        input_text = st.text_input("Input")

    # Add the button after the container
    if st.button("Button"):
        # Append the input text to the chat text
        chat_text.append(input_text)
        print(chat_text)
        input_text = ""

        # Update the chat text placeholder with the updated chat text
        chat_placeholder.text('\n'.join(chat_text))

if __name__ == '__main__':
    chat_text = []
    main(chat_text)
