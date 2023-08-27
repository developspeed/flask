from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from utitlities import DBRead
import os

os.environ["OPENAI_API_KEY"] = DBRead('chatgpt-4','API_KEY')

def construct_index(directory_path,userSession):
    max_input_size = 32768
    num_outputs = 16000
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-4-32k", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.save_to_disk(f'index_{userSession}.json')
    return index



def get_answer_for_question(question,userSession):
    user_folder = f"documents/{userSession}/"
    index = construct_index(user_folder,userSession)
    try:
        index = GPTSimpleVectorIndex.load_from_disk(f'index_{userSession}.json')
        response = index.query(question, response_mode="compact")
        return response.response
    except Exception as error:
        return error
    
    