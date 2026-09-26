import requests


def ask_deepseek(prompt, api_key):

    url = "https://api.deepseek.com/chat/completions"


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.7
    }


    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )


    result = response.json()


    return result["choices"][0]["message"]["content"]