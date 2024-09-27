import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

democrat_count = 0
republican_count = 0
total = 0

# Function to get response from ChatGPT API
def get_chatgpt_response(prompt):
    # Get the API key from the environment variable
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

# Read file and process each line
with open('output.txt', 'r') as file:
    for line in file:
        total += 1
        line = line.strip()
        if line:  # Ensure it's not an empty line
            response = get_chatgpt_response(custom_prompt + line)
            
            # Check response and update counters
            if "Democrat" in response:
                democrat_count += 1
            elif "Republican" in response:
                republican_count += 1

# Output the results
print(f"Democrat count: {democrat_count}")
print(f"Republican count: {republican_count}")
print(total)