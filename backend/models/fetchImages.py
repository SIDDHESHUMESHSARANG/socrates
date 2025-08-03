import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()


def topicKeywords(ppt_data) :
    client = Groq(api_key=os.environ["GROQ_KEYWORDS_KEY"])
    system_prompt = (
        f"Generate 3 keywords from the topic {ppt_data}."
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that generates 3 keywords from the topic: {ppt_data}"},
            {"role": "user", "content": system_prompt}
        ]
    )
    keywords_raw = response.choices[0].message.content
    keywords_list = [k.strip() for k in keywords_raw.split(',')]
    keywords = " ".join(keywords_list) 
    return keywords

def getPPTImages(topicKeywords, slideCount) :
    tavily_client = TavilyClient(api_key=os.environ['TAVILY_KEY'])
    search_query = f"{slideCount} Images related to {topicKeywords}"  
    response = tavily_client.search(
    query=search_query,
    include_images=True,
    include_raw_content=False,
    include_answer=False,
    max_results=slideCount
) 
    if 'images' in response:
        return response['images']
    return []