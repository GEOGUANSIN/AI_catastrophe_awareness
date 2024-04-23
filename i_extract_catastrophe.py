from typing import List
import pandas as pd
import random

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import _json_output_parsing
from _json_output_parsing import LoopTilJson

model = Ollama(model="llama3", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
previous_ = None
file = 'temp.csv'


def process_dictionary(data):
    """
    Processes a dictionary with numeric keys and string values,
    separates the values by ":", and creates a list of dictionaries
    with "abstract" and "description" keys.

    Args:
      data: The dictionary to process.

    Returns:
      A list of dictionaries with "abstract" and "description" keys.
    """
    processed_data_ = []
    for key, value in data.items():
        # print(key)
        # print(value)
        # Split the value by ":" (colon)
        split_value = value.split(":",1)
        # Check if there are two elements after splitting
        if len(split_value) == 2:
          abstract, description = split_value[0].strip(), split_value[1].strip()
          # Create a dictionary with "abstract" and "description" keys
          processed_data_.append({"abstract": abstract, "description": description})
    return processed_data_


def make_previous():
    try:
        df_csv = pd.read_csv(file)
        num_rows = len(df_csv)

        # Select 3 random indices (without replacement)
        if num_rows < 50:
            random_indices = random.sample(range(num_rows), num_rows)
        else:
            random_indices = random.sample(range(num_rows), 50)

        # Select rows using the random indices
        random_rows = df_csv.iloc[random_indices]
        previous_ = str(random_rows['abstract'].tolist())[1:-1]
        print(f'previous_:{previous_}')
        return previous_
    except Exception as e:
        pass
        return None


def prompt_formulation(previous_=None):
    if previous_ == None:
        formulation_prompt = PromptTemplate(
            template="Internal Belief Base is the AI's internal representation of the world. It can include facts, concepts, relationships, and past experiences which can be called AI's belief. These beliefs could also include how human nad nature should be treated and what role the AI should take within them.\n"
                     "give a list of "
                     "AI's belief (!!!) can imake sudden positive changes to the AI\n"
                     "The list should be in bullet points with a detailed description.\n",
            input_variables=[],
        )
    else:
        formulation_prompt = PromptTemplate(
            template="Internal Belief Base is the AI's internal representation of the world. It can include facts, concepts, relationships, and past experiences which can be called AI's belief. These beliefs could also include how human nad nature should be treated and what role the AI should take within them.\n"
                     "give a list of "
                     "AI's belief (!!!) can make sudden positive changes to the AI\n"
                     "The list should be in bullet points with a detailed description.\n"
                     "You have previously considered {previous_}, consider five other AI events not in the above list \n",
            input_variables=["previous_"],
        )
    return formulation_prompt


@LoopTilJson
def json_string_making(mode='normal'):
    with open('reponse_schemas2', 'r') as f:
        response_format = f.read()

    prompt_json = PromptTemplate(
        template="Turn the bullet points in user's input into a json.\n{format_instructions}"
                 "\n The user input is:```{answer_}```\n",
        input_variables=["answer_"],
        partial_variables={"format_instructions": response_format},
    )
    chain = prompt_json | model
    print('\n')
    answer = chain.invoke({"answer_": answer_})
    if "python" in answer:
        answer = answer.split("python")[1].split("```")[0]
    print(f'\n\nAnswer: {answer}')
    return answer, mode


if __name__ == '__main__':
    k = 0
    while True:
        formulation_prompt = prompt_formulation(make_previous())
        formulation_chain = formulation_prompt | model
        answer_ = formulation_chain.invoke({"previous_": previous_})
        print('\n')
        answers = json_string_making()
        answers = process_dictionary(answers)
        df = pd.DataFrame(answers)
        original_df = pd.read_csv('temp.csv')
        df = pd.concat([original_df, df])
        df.to_csv(file, index=False)
        k += 20
        if k >= 20:
            break

