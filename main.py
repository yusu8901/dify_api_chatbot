import requests
import json

# Difyのchat-messagesエンドポイント
API_URL = "https://api.dify.ai/v1/chat-messages"

# DifyのSecret Keyを設定
API_KEY = "YOUR_APIKEY_HERE"

# リクエスト共通ヘッダー
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

def start_conversation(query: str, inputs: dict = {}):
    """
    新規会話を開始し、conversation_idと最初の応答を返す関数
    query: ユーザーからの最初の質問
    inputs: 必要に応じて渡す変数（初回の呼び出し時のみ有効）
    """
    data = {
        "inputs": inputs,
        "query": query,
        "response_mode": "blocking",  # "streaming"も可能
        "conversation_id": "",        # 新規会話は空文字列または省略
        "user": "user-123"            # ユーザーを表すIDを任意で指定
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        resp_json = response.json()
        # 新規会話のレスポンスにはconversation_idが含まれる
        conversation_id = resp_json.get("conversation_id", None)
        answer = resp_json.get("answer", "")
        return conversation_id, answer
    else:
        print("Error:", response.text)
        return None, None


def continue_conversation(conversation_id: str, query: str):
    """
    既存のconversation_idを用いて会話を継続
    query: ユーザーからの追加の問いかけ
    """
    data = {
        # 会話継続時、inputsは無視されるため空でOK
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": "user-123"
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        resp_json = response.json()
        answer = resp_json.get("answer", "")
        return answer
    else:
        print("Error:", response.text)
        return ""


if __name__ == "__main__":
    # 新規会話開始
    print("=== Difyチャットボットへようこそ ===")
    user_input = input("あなた: ")
    
    # 最初の問いかけで新規会話開始
    conversation_id, answer = start_conversation(user_input)
    if conversation_id is None:
        print("会話開始に失敗しました。")
        exit(1)
    
    print("Bot:", answer)

    # 継続対話ループ
    while True:
        user_input = input("あなた: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: またお話ししましょう！さようなら！")
            break

        # 既に取得したconversation_idを使って続きの会話
        answer = continue_conversation(conversation_id, user_input)
        print("Bot:", answer)
