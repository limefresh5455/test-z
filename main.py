
from fastapi import FastAPI
import pandas as pd
import difflib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

app = FastAPI(title="FastAPI APP Endpoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items")
async def read_item():
    return {"item_id": "WORKING"}



def generate(content):
    topics_df = pd.read_csv("topics.csv")

    # Create a list of all possible topic-subtopic combinations
    topic_subtopic_pairs = [f"Topic: {topic}, SubTopic: {subtopic}" for topic, subtopic in zip(topics_df['Topic'], topics_df['Subtopic'])]
    topic_subtopic_pairs_str = "\n".join(topic_subtopic_pairs)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                                            You are working as a classifier to categorize content using the provided list of topics and subtopics.

                                            Possible topics and subtopics:

                                            {topic_subtopic_pairs_str}

                                            **Important**: If the content cannot be classified into the provided list, provide the closest topic and subtopic from the list above. 

                                            - If there are multiple close matches, provide the closest topic and subtopic combination.
                                            - Your response should be formatted exactly as: "Topic: topic, SubTopic: subtopic"
                                            - Use only the topics and subtopics given in the provided list above. Do not introduce any new topics or subtopics.
                                            """
            },
            {"role": "user", "content": content}
        ],
        max_tokens=50,
        temperature=0.05
    )
    categories = str(response.choices[0].message.content)
    if categories not in topic_subtopic_pairs_str:
        closest_match = difflib.get_close_matches(categories, topic_subtopic_pairs, n=2, cutoff=0.6)#difflib.get_close_matches function uses a sequence similarity algorithm to find the closest matches
        if closest_match:
            return closest_match[0]
        else:
            return closest_match[1]
    else:
        return categories