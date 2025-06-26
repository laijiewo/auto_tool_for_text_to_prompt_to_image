from openai import OpenAI
import json
import os

# ========== 配置 ==========

# 你的 OpenAI API Key（可替换为环境变量或从文件读取）
client = OpenAI(api_key="key")

MEMORY_FILE = "memory.json"

# ========== 工具函数 ==========


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def build_memory_prompt(memory):
    return f"""
你正在和用户对话，请记住以下信息：
- 用户姓名：{memory.get('name', '未知')}
- 用户偏好：{memory.get('preferences', '未知')}
- 备注：{memory.get('notes', '')}
"""


def update_memory(memory, new_note):
    if new_note:
        memory["notes"] += f" {new_note}"
        save_memory(memory)


# ========== 聊天主函数 ==========


def chat():
    memory = load_memory()
    memory_intro = build_memory_prompt(memory)

    print("💬 请输入用户提问，输入 'exit' 退出：")
    messages = [{"role": "system", "content": memory_intro}]

    while True:
        user_input = input("👤 你：")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        # 与 GPT 交互
        response = client.chat.completions.create(model="gpt-4", messages=messages)

        reply = response.choices[0].message.content
        print(f"🤖 GPT：{reply}")

        messages.append({"role": "assistant", "content": reply})

        # 简单示例：若用户输入“记住我喜欢狗”，就追加偏好
        if "记住" in user_input and "喜欢" in user_input:
            update_memory(memory, user_input.replace("记住", "").strip())


# ========== 启动 ==========

if __name__ == "__main__":
    chat()
