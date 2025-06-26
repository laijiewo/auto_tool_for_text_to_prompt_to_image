import os
import requests
from openai import OpenAI

# 配置参数
DESCRIPTION_FOLDER = "road" # 存放描述文本的文件夹
OUTPUT_FOLDER = "road" # 存放生成图片的文件夹

# 确保输出文件夹存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_image_from_text(doubao, prompt):
    response = doubao.images.generate(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="ep-20250522111820-f6984",
        prompt=prompt,
        size="1024x1024",
        response_format="url",
        # watermark=False
    )

    return response.data[0].url if response.data else None


def process_all_files():
    # 初始化Ark客户端，从环境变量中读取您的API Key
    doubao_client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        # 填入api key
        api_key="key",
    )
    
    for filename in os.listdir(DESCRIPTION_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(DESCRIPTION_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    prompt = f.read().strip()
                except UnicodeDecodeError:
                    with open(file_path, "r", encoding="gbk") as f:
                        prompt = f.read().strip()
                        
                print(f"\n处理文件：{filename}，内容：{prompt}")
                image_url = generate_image_from_text(doubao_client, prompt)
                if image_url:
                    save_path = os.path.join(
                        OUTPUT_FOLDER, filename.replace(".txt", ".png")
                    )
                    save_b64_image(image_url, save_path)


def save_b64_image(url, save_path="./", filename=None):
    """ """
    try:
        ans = requests.get(url, stream=True)
        ans.raise_for_status()

        # # 拼接完整保存路径
        full_path = save_path.replace(".png", f"_{filename}.png")
        # 保存为 PNG 文件
        with open(full_path, "wb") as f:
            for chunk in ans.iter_content(1024):
                f.write(chunk)

        print(f"image save: {full_path}")
        return full_path

    except Exception as e:
        print(f"convert error: {str(e)}")
        return None


if __name__ == "__main__":
    process_all_files()
