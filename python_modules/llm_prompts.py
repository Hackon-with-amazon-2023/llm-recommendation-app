import json
from langchain.llms import OpenAI
from .utils.prompt_templates import standalone_prompt_template, extraction_prompt_template
from .utils.constants import MODEL_NAME, MAX_TOKENS, TEMPERATURE




class LLM:
    def __init__(self, OPENAI_API_KEY) -> None:
        self.llm = OpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL_NAME)


    def generate_standalone_question(self, previous_query, new_query):
        # Standalone question
        standalone_prompt = standalone_prompt_template.format(new_query=new_query, previous_query=previous_query)
        standalone_question_response = self.llm.predict(standalone_prompt, temperature=TEMPERATURE)
        standalone_question = json.loads(standalone_question_response)['standalone_question']
        return standalone_question
    

    def extract_information(self, standalone_question):
        # Extract products information from standalone question
        extraction_prompt = extraction_prompt_template.format(question=standalone_question)
        response = self.llm.predict(extraction_prompt, temperature=TEMPERATURE)
        extracted_info = json.loads(response)
        return extracted_info


    def generate_search_query(self, standalone_question):
        extected_info = self.extract_information(standalone_question)
        query = extected_info['product_category']
        if extected_info['product_category'] == "":
            return ""
        if extected_info['product_names'] != []:
            query += " " + " ".join(extected_info['product_names'])
        if extected_info['filters']['budget']['low'] != None and extected_info['filters']['budget']['high'] != None:
            query += " in range " + str(extected_info['filters']['budget']['low']) + " to " + str(extected_info['filters']['budget']['high'])
        elif extected_info['filters']['budget']['low'] != None:
            query += " above " + str(extected_info['filters']['budget']['low'])
        elif extected_info['filters']['budget']['high'] != None:
            query += " below " + str(extected_info['filters']['budget']['high'])
        if extected_info['filters']['brands'] != []:
            query += " " + " ".join(extected_info['filters']['brands'])
        if extected_info['filters']['ratings'] != None:
            query += " with rating " + str(extected_info['filters']['ratings'])
        return query

