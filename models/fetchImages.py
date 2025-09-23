import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()


def topicKeywords(ppt_data) :
    client = Groq(api_key=os.environ["GROQ_KEYWORDS_KEY"])
    system_prompt = (
        f"Generate 3 keywords from the topic: {ppt_data}. Return only the keywords separated by commas."
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates 3 keywords from the topic."},
            {"role": "user", "content": system_prompt}
        ]
    )
    keywords_raw = response.choices[0].message.content
    # Remove any extra text and split by comma
    keywords_list = [k.strip() for k in keywords_raw.split(',') if k.strip()]
    return keywords_list

def getPPTImages(topicKeywords, slideCount) :
    tavily_client = TavilyClient(api_key=os.environ['TAVILY_KEY'])
    # Join keywords for search
    search_query = f"{slideCount} Images related to {' '.join(topicKeywords)}"  
    response = tavily_client.search(
        query=search_query,
        include_images=True,
        include_raw_content=False,
        include_answer=False,
        max_results=slideCount
    )
    if 'images' in response and isinstance(response['images'], list):
        # Only return valid image URLs
        return [img for img in response['images'] if isinstance(img, str) and img.startswith('http')]
    return []