import json, os
import openai
from langchain.prompts import PromptTemplate 
from dotenv.main import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Step 2: Open the JSON file and read its contents
with open('jupyter_notebooks/phones.json', 'r') as json_file:
    data = json.load(json_file)


for it in data:
    del it['details']
    it['link'] = "amazon.com/" + it['name'][:20]

print(data)

recommendation_prompt = """
You are a e-commerce recommendation assistant
You are given a product list in JSON format, based on your understanding reply to the user query
Try to give detailed answers, use the product details and mention all it's qualities.
Mention the link for the described product as well

Product List:
```
{product_list}
```
"""

recommendation_prompt_template = PromptTemplate(
    template=recommendation_prompt,
    input_variables=["product_list"]
)


def get_recommendation(product_list, question):
    prompt = recommendation_prompt_template.format(product_list=product_list);

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        api_key=api_key,
        temperature=1
    )
    
    return response['choices'][0]['message']['content']

question = "Suggest me a gaming smartphone, I have a lot of money"
output = get_recommendation(data, question)
print(output)
