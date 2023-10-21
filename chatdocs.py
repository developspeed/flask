from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from utilities import DBRead
import os

def construct_index(directory_path,userSession):
    max_input_size = 16000
    num_outputs = 8000
    max_chunk_overlap = 40
    chunk_size_limit = 1000

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo-16k", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.save_to_disk(f'index_{userSession}.json')
    return index


def get_answer_for_question(question, userSession):
    index_path = f'index_{userSession}.json'
    user_folder = f"documents/{userSession}/"
    index = construct_index(user_folder, userSession)
    try:
        index = GPTSimpleVectorIndex.load_from_disk(index_path)
        response = index.query(question, response_mode="compact")
        return response.response
    except Exception as error:
        return str(error)
                
