from langchain import PromptTemplate


standalone_prompt = """
Generate a standalone question which is combination of the new question plus the chat history.

- If the new product is totally different, or if the previous question is empty string then use it as the new standalone question
- else update the previous question and combine it with the new question

Give output in the following JSON format:
{{
    "standalone_question": "Your generated standalone question goes here."
}}

New Question: {new_query}

Previous question: {previous_query}

Output:
"""



extraction_prompt = """
You are good in extracting information.
You will be given a input json containing question, and you have to extract the following files in the specified JSON format.
{{
	"product_category": "category of the product mentioned",
	"product_names": ["array of specific product names mentioned"],
	"filters": {{
		"budget" : {{
			"low": integer lower value of budget and default null,
			"high": integet upper value of budget and default null
		}},
		"brands": ["array of brands/company names mentioned"],
		"ratings": integer value of rating in range [1, 5] 
	}}
}}

Example is show below
Input:
{{
	"question": "I want to buy the best air conditioner for my living room in a 30K budget, please suggest me a branded 5-star power-rated AC preferably of LG."
}}
Output:
{{
	"product_category": "air conditioner",
	"product_names": [],
	"filters": {{
		"budget" : {{
			"low": null,
			"high": 30000
		}},
		"brands": ["LG"],
		"ratings": 5
	}}
}}

Let's begin
Input:
{question}
Output: 
"""






############################### Prompt Templates ###############################
standalone_prompt_template = PromptTemplate(
    template=standalone_prompt,
    input_variables=["new_query", "previous_query"]
)


extraction_prompt_template = PromptTemplate(
    template=extraction_prompt,
    input_variables=["question"]
)
