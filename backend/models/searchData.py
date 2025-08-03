import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["GROQ_KEY"])

def getPPTData(prompt, slideNumber):
    system_prompt = (
        f"Generate a {slideNumber}-slide presentation on '{prompt}'. "
        "Each slide should have a clear heading and a min 3-5 line content."
        "Don't show the slide numbers in the output, just heading"
        "Use sections and give the same of sections by you according to the context. "
        "Make a pptx file and paste the content inside it according to respective slides."
        "STRICTLY: Only return the ppt content and not any extra explanation."
        "STRICTLY: Write the content in bullet points only."
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates presentation content."},
            {"role": "user", "content": system_prompt}
        ]
    )

    content = response.choices[0].message.content
    return content
