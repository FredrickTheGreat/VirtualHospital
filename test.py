import json
import requests


def get_assist(query):
    url = 'https://u384232-8174-307abb43.westc.gpuhub.com:8443/chat/knowledge_base_chat'
    data = {
        "query": "介绍下虚拟宠物医院学习系统",
        "knowledge_base_name": "samples",
        "top_k": 5,
        "score_threshold": 1,
        "history": [
            {
                "role": "user",
                "content": "我们来玩成语接龙，我先来，生龙活虎"
            },
            {
                "role": "assistant",
                "content": "虎头虎脑"
            }
        ],
        "stream": False,
        "local_doc_url": False
    }
    # Convert data to JSON string
    response = requests.post(url, data=json.dumps(data))
    response = response.json()
    value1 = response['answer']
    print(value1)
    return response


get_assist("query")
