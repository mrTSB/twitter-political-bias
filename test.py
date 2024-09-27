'''
This file can be used to test what models are the best judges. It leverages the output.txt file created by analysis.py.
The output.txt file can be created by uncommenting the code at the bottom of analysis.py.
'''

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

democrat_count = 0
republican_count = 0
total = 0

def get_chatgpt_response(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

custom_prompt = "Is this following tweet more favorable for the Republican or Democratic party. Reply with either 'Democratic' or 'Republican'. Do NOT say anything else besides that one word. \n "

with open('output.txt', 'r') as file:
    for line in file:
        total += 1
        line = line.strip()
        if line:
            response = get_chatgpt_response(custom_prompt + line)
            
            if "Democrat" in response:
                democrat_count += 1
            elif "Republican" in response:
                republican_count += 1

# Output the results
print(f"Democrat count: {democrat_count}")
print(f"Republican count: {republican_count}")
print(total)