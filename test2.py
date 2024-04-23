import json

# 已有的 history JSON 数据
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

# 创建一个新的 JSON 字符串，包含 history 和一个额外的查询
full_json = f'{{"history": {history}, "query": "职能学习干啥的"}}'

# 打印这个新的 JSON 字符串
print(full_json)

# 如果需要将这个 JSON 字符串转换为 Python 字典
full_dict = json.loads(full_json)
print(full_dict)