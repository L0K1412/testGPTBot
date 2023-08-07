import json

from langchain.prompts import PromptTemplate

from intents import GetTokenPrice, GetTokenPriceChanges, GetTokenWebsite

available_intents = [
    GetTokenPrice(),
    GetTokenWebsite(),
    GetTokenPriceChanges(),
]


intent_action_map = {intent.name: intent for intent in available_intents}


def construct_promt_intents(intents):
    return "\n".join([intent.promt() for intent in intents])


def parse_user_intent_and_entities(llm, conversation, intents=available_intents):
    # based on the customers answer, return the intent
    prompt = PromptTemplate(
        input_variables=["conversation", "promt_intents"],
        template=(
            "You are a friendly assistant that help user retrieve and analyze data on blockchain. \n"
            "You are helping a customer who just got into contact with you.\n"
            "The conversation so far:\n"
            "{conversation}\n\n"
            "based on user answer and the following list of intents, please extract the intent and entities \
            that best matches the user's answer.\n"
            "{promt_intents}\n"
            'Please answer with a JSON object containing the intent and entities in the format \
            {{"intent": "intent_name", "entities": PLACE_HOLDER}}\n'
            "Where PLACE_HOLDER is the dictionary of required entities defined for each intent above, \n"
            "leave it as empty string if not found. \n"
        ),
    )

    promt_intents = construct_promt_intents(intents)

    intent_json = llm.predict(
        prompt.format(conversation=conversation, promt_intents=promt_intents)
    )

    return json.loads(intent_json)  # return dict


def gather_info_message(llm, known_information, missing_information, conversation):
    template = PromptTemplate(
        input_variables=[
            "known_information",
            "missing_information",
            "conversation",
        ],
        template=(
            "You are a friendly assistant that help user retrieve and analyze data on blockchain. \n"
            "The conversation so far:\n"
            "{conversation}\n\n"
            "The user has provided the following information:\n"
            "{known_information}\n"
            "The user has not provided the following information:\n"
            "{missing_information}\n"
            "Please ask the customer in a friendly way for the missing information. "
        ),
    )
    prompt = template.format(
        known_information=known_information,
        missing_information=missing_information,
        conversation=conversation,
    )
    response = llm.predict(prompt)

    return response
