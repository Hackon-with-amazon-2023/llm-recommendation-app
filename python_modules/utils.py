###### User Input ######
###### Create standalone question ######
######### Extract features from user input #########
######### Scrape products if product_category changes #########
######## Recommend products based on extracted information ########


# external knowledge base for storing user prefrences
contexts = [
    (
        "User buy branded items only." +
        " User spends money wisely."
    ),
    (
        "User buy items on holdiays." +
        " User buy items on festivals."
    )
]
context_str = '\n\n##\n\n'.join(contexts)





# Function to call GPT-3.5 with the template
def generate_recommendation(user_requirements, product_list, context_str):
    

    prompt = recommandation_prompt_template.format(
        user_requirements= user_requirements,
        product_list=product_list,
        context_str=context_str
    )

    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-3.5
        prompt=prompt,
        max_tokens=50,  # Adjust this as needed
        api_key=api_key
    )
    
    return response.choices[0].text

