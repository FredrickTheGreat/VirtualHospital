import json
import requests


def get_assist(query):
    url = 'https://u384232-8174-307abb43.westc.gpuhub.com:8443/chat/knowledge_base_chat'
    history = '''[
        {
            "content": "我们来玩成语接龙，我先来，生龙活虎",
            "createAt": 1713163951123,
            "id": "pPwYTkEp",
            "meta": "iavatar",
            "parentId": "undefined",
            "role": "user",
            "title": "undefined",
            "updateAt": 1713163951123
        },
        {
            "content": "虎头虎脑",
            "createAt": 1713163951123,
            "id": "pPwYTkEp",
            "meta": "iavatar",
            "parentId": "undefined",
            "role": "assistant",
            "title": "undefined",
            "updateAt": 1713163951123
        }
    ]'''
    origin = json.loads(history)
    transhistory = [
        {"role": item["role"], "content": item["content"]} for item in origin if item["role"] != "assistant"
    ]
    print(json.dumps(transhistory, ensure_ascii=False, indent=4))
    data = {
        "query": query,
        "knowledge_base_name": "samples",
        "top_k": 5,
        "score_threshold": 1,
        "history": transhistory,
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
