import openai

openai.api_key = 'your_openai_api_key'

def analyze_news_with_gpt(article_content):
    prompt = (
        "Analyze the following news article and extract key information:\n"
        f"Article: {article_content}\n"
        "What is the main impact of this news on the stock market? "
        "Mention the affected sectors or companies, and any potential implications."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.5
    )

    analysis = response['choices'][0]['message']['content']
    return analysis
