import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["GROQ_KEY"])

def getPPTData(prompt, slideNumber):
    system_prompt = (
        f"Generate a visually appealing {slideNumber}-slide presentation on '{prompt}'. "
        "For each slide, use a clear, catchy heading (wrap in double asterisks: **Heading**). "
        "Under each heading, provide 3-5 concise, meaningful one-liner bullet points (start each with •). "
        "Bullet points should be contextually relevant, easy to understand, and avoid generic statements. "
        "Use vocabulary that is professional yet friendly—avoid jargon, but keep it engaging and smart. "
        "Do not include slide numbers, extra explanations, or formatting outside of headings and bullet points. "
        "STRICTLY: Only return the presentation content in the specified format. "
        "Example format:\n**Heading**\n• Point one\n• Point two\n..."
        "Add one line gap between each bullet point"
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates presentation content."},
            {"role": "user", "content": system_prompt}
        ]
    )

    content = response.choices[0].message.content
    print("\n--- Groq Response ---\n", content, "\n--- End Response ---\n")
    if "**" not in content or "•" not in content:
        print("WARNING: Response format may not match expected headings/bullets.\n")
    return content
