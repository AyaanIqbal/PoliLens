import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('openAI_API_KEY')

def analyze_news_with_gpt(article_content):
    prompt = (
        "Analyze the following news article and extract key information:\n"
        f"Article: {article_content}\n"
        "What is the main impact of this news on the stock market? "
        "Mention the affected sectors or companies, and any potential implications."
    )

    # Create the chat messages format expected by the ChatCompletion API
    messages = [
        {"role": "system", "content": "You are a financial expert."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.5
        )
        analysis = response['choices'][0]['message']['content']
        return analysis
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
article_content = "The Federal Reserve has announced an unexpected interest rate increase, citing inflation concerns..."
result = analyze_news_with_gpt(article_content)
print(result)
