# llm-recommendation-app


# THEME: Shopping Experience Enhancement with Generative AI + AWS

## Team Name: 729950-U92A3D3B

### Team Members:
- Anuj Jadhav
- Bittu Kumar
- Pulkit Kumar Agarwal
- Animesh Maru
---

## Problem Statement

In the contemporary e-commerce landscape, consumers demand personalized and easy-to-use shopping experiences. Traditional online shopping platforms often fail to provide tailored product recommendations, leading to inefficient decision-making. The goal is to employ Generative AI and AWS technologies to enhance the Amazon shopping experience, considering factors like user preferences, previous orders, location, and chat interactions.

---

## <u>Solution:</u>

We have created a telegram bot where we curate contextual shopping experiences based on individual user's chat session and preferences. 
You can send your query to the chatbot and it will show you the best products based on the context given by you in the query.


### PPT Link: [link](https://docs.google.com/presentation/d/1qAZEzYsSzj9SHvJ3ff1mM5j19BHARMyd/edit?usp=sharing&ouid=115057851485032498036&rtpof=true&sd=true)


### Flow Chart:
![flow chart](https://github.com/Hackon-with-amazon-2023/llm-recommendation-app/assets/77394228/a2a6b629-56fe-4218-9303-a2ad968a45fb)


### You can try out the bot here: [telegram bot](https://t.me/AmazonProductSearchBot)

---
## Screenshots:

### Starting the bot:
![Screenshot (48)](https://github.com/Hackon-with-amazon-2023/llm-recommendation-app/assets/77394228/cc0726af-3fe0-4449-b07a-831d59d8d153)

### Getting details for phones:
![Screenshot (50)](https://github.com/Hackon-with-amazon-2023/llm-recommendation-app/assets/77394228/bbdf8395-3d1b-416e-8c2c-a72b16b60795)


### Getting details for shoes:
![Screenshot (47)](https://github.com/Hackon-with-amazon-2023/llm-recommendation-app/assets/77394228/31fdc2f8-3305-4e8c-bba9-17c37a277177)

---

## To run the bot on local:
1. Clone the repo and install all libraries
    - git clone https://github.com/Hackon-with-amazon-2023/llm-recommendation-app.git
    - pip install -r requirements.txt

2. Create a telegram bot using @botfather on telegram and get the token for bot

3. Create a .env file with variables:
    - TELEGRAM_TOKEN
    - OPENAI_API_KEY

4. Run main.py file
