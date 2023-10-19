import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate




class LLM:
    def __init__(self, OPENAI_API_KEY) -> None:
        self.llm = OpenAI(openai_api_key=OPENAI_API_KEY)


        self.user_query_prompt_template = PromptTemplate.from_template(
            "You are a seller of ecommerce store, you want to help a customer who wants to buy some products from an your store online but don't know how to write query to search products according to his requirements.\n"
            "So he ask you to help him in writing the query to search bar of website.\n"
            "Give more importance to the last sentence in the User Query\n"
            "You have to reply in the following format:\n"
            "{{\"query\": \"Your Query\"}}\n"
            "Example1:\n"
            "User Query: 'I want to buy a shirt which is blue in color or may be red'\n"
            "You: {{\"query\": \"Red or Blue Shirt\"}}\n"
            "Example2:\n"
            "User Query: 'Red or Blue Shirt, Show me shoes'\n"
            "You: {{\"query\": \"Shoes\"}}\n"
            ""
            ""
            "Give reply for the following query.\n"
            "User Query: {query}\n"
            "You: "
        )



    def predict(self, user_query, temperature=0.5):
        user_query_prompt = self.user_query_prompt_template.format(query=user_query)
        return self.llm.predict(user_query_prompt, temperature=temperature)


    def get_user_query(self, old_query, new_message):
        user_query = f"{old_query}, {new_message}"
        user_query_prompt = self.user_query_prompt_template.format(query=user_query)
        user_query_response = self.llm.predict(user_query_prompt, temperature=0.5)

        user_query = json.loads(user_query_response)['query']
        return user_query

