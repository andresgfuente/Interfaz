#Hello! It seems like you want to import the Streamlit library in Python. Streamlit is a powerful open-source framework used for building web applications with interactive data visualizations and machine learning models. To import Streamlit, you'll need to ensure that you have it installed in your Python environment.
#Once you have Streamlit installed, you can import it into your Python script using the import statement,
import streamlit as st

#As Langchain team has been working aggresively on improving the tool, we can see a lot of changes happening every weeek,
#As a part of it, the below import has been depreciated
#from langchain.llms import OpenAI

#New import from langchain, which replaces the above
from langchain_openai import OpenAI
import boto3
import json
import botocore.config
#When deployed on huggingface spaces, this values has to be passed using Variables & Secrets setting, as shown in the video :)
#import os
#os.environ["OPENAI_API_KEY"] = ""

#Function to return the response



def load_answer(question):
    prompt_text = f"""Human: Responde la siguiente pregunta: {question}.
    Assistant:
    """
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k":250,
        "top_p": 0.2,
        "stop_sequences":["\n\nHuman:"]
    }
    body_titan= {
            "inputText": prompt_text,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        }

    # "text-davinci-003" model is depreciated, so using the latest one https://platform.openai.com/docs/deprecations
    bedrock=boto3.client("bedrock-runtime",region_name='us-east-1')
    response = bedrock.invoke_model(body=json.dumps(body_titan),modelId="amazon.titan-text-express-v1")
    response_content = response.get('body').read().decode('utf-8')
    response_data = json.loads(response_content)
    response_data=response_data['results'][0]['outputText']
    #respuesta= response_data["completion"].strip()
    #llm = OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0)

    #Last week langchain has recommended to use invoke function for the below please :)
    return response_data


#App UI starts here
st.set_page_config(page_title="Prueba", page_icon=":robot:")
st.header("Interfaz Demo")

#Gets the user input
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input=get_text()
response = load_answer(user_input)

submit = st.button('Generate')  

#If generate button is clicked
if submit:

    st.subheader("Respuesta:")

    st.write(response)

