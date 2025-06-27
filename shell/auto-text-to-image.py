import json
import os
import httpx
import requests
from openai import OpenAI

# 配置参数
DESCRIPTION_FOLDER = "E:\T2I lab\shell_generated" # 存放描述文本的文件夹
OUTPUT_FOLDER = "E:\\T2I lab\\shell_generated_image" # 存放生成图片的文件夹

# 确保输出文件夹存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
API_KEY = "k"


def generate_image(prompt, seed=35):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "doubao-seedream-3-0-t2i-250415",  # 替换为你用的模型ID
        "prompt": prompt,
        "response_format": "url",
        "size": "1024x1024",
        "seed": seed,
        "guidance_scale": 2.5,
        "watermark": True
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()["data"][0]["url"]
    else:
        print("❌ 请求失败:", response.status_code, response.text)
        return None
    

def generate_image_from_text(doubao, prompt):
    response = doubao.images.generate(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="ep-20250522111820-f6984",
        prompt=prompt,
        size="1024x1024",
        response_format="url",
        seed=42
        # watermark=False
    )

    return response.data[0].url if response.data else None


def process_all_files():
    # # 初始化Ark客户端，从环境变量中读取您的API Key
    # doubao_client = OpenAI(
    #     # 此为默认路径，您可根据业务所在地域进行配置
    #     base_url="https://ark.cn-beijing.volces.com/api/v3",
    #     # 填入api key
    #     api_key="k",
    #     timeout=httpx.Timeout(30.0, connect=10.0)
    # )
    
    for filename in os.listdir(DESCRIPTION_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(DESCRIPTION_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    prompt = f.read().strip()
                except UnicodeDecodeError:
                    with open(file_path, "r", encoding="gbk") as f:
                        prompt = f.read().strip()
                        
                print(f"\n处理文件: {filename}，内容：{prompt}")
                # image_url = generate_image_from_text(doubao_client, prompt)
                image_url = generate_image(prompt, 250)
                if image_url:
                    save_path = os.path.join(
                        OUTPUT_FOLDER, filename.replace(".txt", ".png")
                    )
                    save_b64_image(image_url, save_path)
                if not image_url:
                    print(f"⚠️ 图像生成失败：{filename}")
                    continue


def save_b64_image(url, save_path="./", filename=None):
    """ """
    try:
        ans = requests.get(url, stream=True)
        ans.raise_for_status()

        # 拼接完整保存路径
        full_path = save_path.replace(".png", f"_{filename}.png")
        # 保存为 PNG 文件
        with open(full_path, "wb") as f:
            for chunk in ans.iter_content(1024):
                f.write(chunk)

        print(f"image save: {full_path}")
        print()
        return full_path

    except Exception as e:
        print(f"convert error: {str(e)}")
        return None


if __name__ == "__main__":
    process_all_files()
