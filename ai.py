import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
client = AsyncGroq(api_key=os.getenv('GROQ_API_KEY'))

async def ask_amadeus(persona, history, user_message):
    SECRETrules = ( # to prevent discord and api limits
        "you must AVOID long answers. "
        "summarize all your answers concisely, briefly, and clearly. "
        "maximum of 2 short paragraphs, if explaining a concept, provide only the key points."
    )

    system_content = f"{persona}\n\n{SECRETrules}"

    messages = [{"role": "system", "content": system_content}] 
    messages.extend(history[-8:])
    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        messages=messages, 
        model="llama-3.1-8b-instant", # ikr this shit is so ass but i think its enough just for daily usage
        temperature=0.7,
        max_tokens=600
    )
    
    return response.choices[0].message.content