import langchain
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import AIMessage, HumanMessage
from streamlit_chat import message as st_message

from utils import (gather_info_message, intent_action_map,
                   parse_user_intent_and_entities)

langchain.verbose = False

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(temperature=0, openai_api_key="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")


def bot_greeting():
    return (
        "Hi there, I'm a virtual assistant that help you retrieve and analyze data from blockchain. \n"
        "How can I help you today?"
    )


def extract_known_and_missing_entities(entities):
    missing_entities = []
    known_entities = []
    for k in entities:
        if entities[k] == "":
            missing_entities.append(k)
        else:
            known_entities.append(k)

    return known_entities, missing_entities


def generate_answer():
    user_message = st.session_state.input_text
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history_openai.append(HumanMessage(content=user_message))
    llm = st.session_state["llm"]
    parsed_intent = parse_user_intent_and_entities(
        llm, conversation=st.session_state.history_openai
    )
    intent_name = parsed_intent["intent"]
    entities = parsed_intent["entities"]
    print("detected intent: ", intent_name)
    print("entities: ", entities)
    known_entities, missing_entities = extract_known_and_missing_entities(entities)
    if len(missing_entities) > 0:
        # ask follow-up question to gather information
        bot_message = gather_info_message(
            llm,
            known_entities,
            missing_entities,
            conversation=st.session_state.history_openai,
        )
    else:
        # trigger function once gather all entities
        intent = intent_action_map[intent_name]
        bot_message = intent.fulfill(**entities)
    st.session_state.history.append({"message": bot_message, "is_user": False})
    st.session_state.history_openai.append(AIMessage(content=bot_message))
    clear_text()


def clear_text():
    st.session_state["input_text"] = ""


if "history" not in st.session_state:
    bot_message = bot_greeting()
    st.session_state.history = [{"message": bot_message, "is_user": False}]
    st.session_state.history_openai = [AIMessage(content=bot_message)]

st.title("SOC_Bot - Jarvis for blockchain data")
st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

for i, chat in enumerate(st.session_state.history):
    st_message(**chat, key=str(i))  # unpacking
