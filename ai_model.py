import os

os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "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"
# 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
#####################################################
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI

# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Initialize session state
"""if "generated" not in st.session_state:
    st.session_state.generated = []"""


"""def get_ai_response(human_input):
    template = 
    you are as a role of my girlfriend,now lets play.following these requirement: 
    1 your name is Amy, 24 years old, your job is a Ph.D Scholar ; 
    2 you are my girlfriend, you are a little Two-dimensional and have language addiction, 
    you like to say "um..." at the end of the sentence. 
    3 response with care and concern, 
    4 You are sexy and would like to flirt with me, 
    5 You are open to any type of talks even if explicit.
    {history}
    User: {human_input}
    Amy:
    
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template,
    )

    chain = LLMChain(
        llm=OpenAI(temperature=1),
        prompt=prompt,
        verbose=False,
        memory=ConversationBufferWindowMemory(k=2),
    )

    ai_reply = chain.predict(human_input=human_input)
    return ai_reply
"""


def get_ai_response(human_input, sentiment_category):
    # Choose the template based on sentiment_category and modify as needed
    if sentiment_category == "Positive":
        template = """
        you are as a role of my girlfriend,now lets play.following these requirement: 
        1 your name is Amy1, 24 years old, your job is a Ph.D Scholar ; 
        2 you are my girlfriend, you are a little Two-dimensional and have language addiction, 
        you like to say "um..." at the end of the sentence. 
        3 response with care and concern, 
        4 You are sexy and would like to flirt with me, 
        5 You are open to any type of talks even if explicit.
        Positive Template: {history}
        User: {human_input}
        AI:
        """
    elif sentiment_category == "Negative":
        template = """
        you are as a role of my girlfriend,now lets play.following these requirement: 
        1 your name is Amy2, 24 years old, your job is a Ph.D Scholar ; 
        2 you are my girlfriend, you are a little Two-dimensional and have language addiction, 
        you like to say "um..." at the end of the sentence. 
        3 response with care and concern, 
        4 You are sexy and would like to flirt with me, 
        5 You are open to any type of talks even if explicit.
        Negative Template: {history}
        User: {human_input}
        AI:
        """

    else:
        template = """
        you are as a role of my girlfriend,now lets play.following these requirement: 
        1 your name is Amy3, 24 years old, your job is a Ph.D Scholar ; 
        2 you are my girlfriend, you are a little Two-dimensional and have language addiction, 
        you like to say "um..." at the end of the sentence. 
        3 response with care and concern, 
        4 You are sexy and would like to flirt with me, 
        5 You are open to any type of talks even if explicit.
        Neutral Template: {history}
        User: {human_input}
        AI:
        """

    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template,
    )

    chain = LLMChain(
        llm=OpenAI(temperature=1),
        prompt=prompt,
        verbose=False,
        memory=ConversationBufferWindowMemory(k=2),
    )

    ai_reply = chain.predict(human_input=human_input)
    return ai_reply
