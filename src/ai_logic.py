import openai
import os

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_city_info(city_name, model="gpt-3.5-turbo", temperature=0):
    """
    Fetches information about the given city using OpenAI's GPT model in a chat format.
    """
    prompt = f"Tell me about the city {city_name}, its environment, climate and flood risk, and also its population. Summarize and avoid redundancy."
    messages = [{"role": "assistant", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"Failed to fetch city information: {e}")
        return None
