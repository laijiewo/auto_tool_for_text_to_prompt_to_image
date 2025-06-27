from openai import OpenAI
import os

# ====== 配置 OpenAI 客户端 ======
client = OpenAI(api_key="k")  # ⚠️ 建议使用环境变量方式更安全

# ====== 固定的转换任务 prompt ======
system_prompt = """
你是一个3D纹理图像转换器。用户会提供一段完整的黄金饰品描述，请你仅保留与图案纹理有关的内容，严格按照以下格式生成描述：

【输出格式要求】
1. 开头固定写为：“仅提供长方形的用于映射到3D的平面展开纹理，图案的形状和细节参考输入图片。背景为纯黑背景。”
2. 明确写出纹理材质，例如：“纹理材质为黄金，且为金黄色，磨砂质感。”
3. 如果描述中出现“X组浮雕，每组包含...”这样的句式，请**只保留每组的结构和排列方式**，不要乘以组数。禁止写成“浮雕包括X个XXX”，而是写成：“每组浮雕包括...”或“浮雕由...组成”。
4. 明确说明浮雕或图案的排列顺序，例如：“浮雕由1个福字、1朵莲花、2条卷草纹组成，依次排列”。如果描述中出现”上下两侧各有一圈扭绳”这句话，请删除。
5. 可以根据原文提取并补充排列细节，例如“福字居中，左右各有1朵莲花，莲花外侧各有1条卷草纹”。并且去除所有的“镂空”描述。
6. 严禁出现“手镯”、“宽度”、“正视图”、“整体视角”等与结构或摄影角度无关的词汇。
7. 结尾统一写为：“注意除了浮雕以外都是背景，保持背景颜色一致，都是纯黑色，没有上下边框。注意：所有纹理图案必须沿水平方向一字排开，排列在同一条直线上，禁止出现上下堆叠或层叠效果。整体纹理为单层横向纹理，用于生成连续贴图。”
8. 禁止出现“镂空”与“光面”相关的描述。所有的镂空与光面的描述都需要删除。
9. 所有浮雕图案必须**严格沿一条横线排列**，禁止垂直堆叠或错落排布，整体纹理结构为**单行横向展开**，用于映射到环形表面。
10. 请确保所有图案均为同一高度，**所有纹理图案必须严格在一条横线上**，不得分层排列，便于环形贴图使用。

【语言要求】
- 使用简体中文。
- 语气准确、规范、简洁，便于图像生成模型识别。
- 输出内容风格统一，与以下样例一致：

请严格遵守以上规则生成内容。
"""

input_dir = "E:\\T2I lab\\3D渲染图文件20250523\\正视图"
output_dir = "E:\\T2I lab\\shell_generated"


def read_text_with_fallback_encoding(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="gbk") as f:
            return f.read().strip()
        
        
# ====== 批处理函数 ======
def convert_all_texts():
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".txt", ".result.txt"))

        user_input = read_text_with_fallback_encoding(input_path)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        print(f"📄 正在处理: {filename}...")

        response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
        result = response.choices[0].message.content
        print(result)

        with open(output_path, "w", encoding="utf-8") as out:
                out.write(result)

        print(f"✅ 输出完成: {output_path}")


if __name__ == "__main__":
    convert_all_texts()
