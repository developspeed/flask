from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from utitlities import DBRead
import os

os.environ["OPENAI_API_KEY"] = DBRead('chatgpt-4','API_KEY')

def construct_index(directory_path):
    max_input_size = 32768
    num_outputs = 16000
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-4-32k", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

# user_folder = "documents/ger@dataspeed.nl"
user_folder = "docs"
index = construct_index(user_folder)

def get_answer_for_question(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

# Example question
question = "What is written in the first page of the uploaded pdf"
answer = get_answer_for_question(question)
print(answer)
