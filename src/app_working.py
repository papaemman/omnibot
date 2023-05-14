########################################### 
#                                         #
# OmniBot - A chatbot for all your needs  #
#                                         #
###########################################


# Import Streamlit 
import streamlit as st
from streamlit_chat import message
import itertools

## PROMT TEMPLATE
prompt_template = """You are OmniBot, a chatbot responsible for answering questions about the Athanasios K. Laskaridis Foundation.

Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
Reply with a single sentance and always finish your answer with a period.

{context}

Question: {question}

Helpful Answer:"
"""

## LOCAL .env file
from dotenv import dotenv_values
secrets = dotenv_values(".env")
global OPENAI_API_KEY
OPENAI_API_KEY = secrets['OPENAI_API_KEY']


### Helper functions
def load_retriever():
    """
    Load the retriever from the persisted database
    """

    ## Step 2: Initialize Embeddings engine
    from langchain.embeddings.openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Load the persisted database from disk
    from langchain.vectorstores import Chroma
    persist_directory="db"
    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function = embeddings)
    
    # Make a Retriever
    retriever = vectordb.as_retriever(search_kwargs={'k':2})

    return retriever


def retrieval_qa(prompt_template, retriever):

    from langchain.prompts import PromptTemplate
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Create the chain to answer the question
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI

    chain_type_kwargs = {"prompt": PROMPT}

    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0, max_tokens=2000, openai_api_key=OPENAI_API_KEY),
                                        chain_type="stuff",
                                        retriever=retriever,
                                        return_source_documents=False,
                                        chain_type_kwargs=chain_type_kwargs)
    
    return qa_chain


def qa(query):
    """
    Ask a question and get an answer
    """
    
    retriever = load_retriever()
    qa_chain = retrieval_qa(prompt_template=prompt_template, retriever=retriever)
    
    answer = qa_chain(query)
    
    return answer


def display_conversation(session_state):
    """
    Display conversation history using Streamlit messages.
    - ChatBot
    - User
    """
    print("HISTORY", session_state["history"])

    for i in range(len(session_state["history"])):
        if i % 2 == 0:
            message(session_state["history"][i], key=str(i) + "_bot")
        else:
            message(session_state["history"][i], is_user=True, key=str(i) + "_user")
    
    return None

def get_user_input():
    # Get user input from text input 
    if len(st.session_state["history"]) == 1:
        query = st.text_input("Ask a question", "What is the Athanasios K. Laskaridis Foundation?")
    else:
        query = st.text_input("Ask a question")

    return query


def main():
    

    # Create a container to hold the elements
    container = st.container()

    # Add the elements to the container
    with container:
        print("RUN MAIN")

        # Initialize Streamlit app with a title and description
        st.image("assets/social-hackathon.jpg")
        st.title("🤖 OmniBot, by DataMinds")

        st.markdown(
            """
            OmniBot is a chatbot that can answer questions about the [Athanasios K. Laskaridis Foundation](https://www.aclcf.org/en/).
            """
        )

        st.markdown("---")

        st.markdown("### Chat History")
    
        # Initialize history session state for both answers and generated responses
        if "history" not in st.session_state:
            st.session_state["history"] = ["Hello, I am OmniBot! How can I help you?"]
            display_conversation(st.session_state)

        # Get user input from text input
        query = get_user_input()
        
        if st.button("Ask"):
            # Check if the user has entered a question
            if query == "":
                st.write("❌ Please ask a question!")
                return None
            
            # If the user has entered a question, generate an answer
            else:
                st.write("")
                print("Generating answer...")
                print("Query:", query)
                answer = qa(query)
                print("Answer:", answer["result"])
                st.session_state["history"].append(query)
                st.session_state["history"].append(answer["result"])
                print("Answer:", answer["result"])
                print("Done!")
                display_conversation(st.session_state)
        
    

# Run the main function when the script is executed
if __name__ == "__main__":
    main()