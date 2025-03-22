# 导入Streamlit库，用于创建Web应用
import os

import streamlit as st
# 导入OpenAI库，用于与OpenAI的API进行交互
from openai import OpenAI
# 导入PIL库，用于图像处理
from PIL import Image
# 导入base64库，用于编码和解码base64字符串
import base64
# 导入io库，用于处理字节流
import io
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)


# 定义函数来处理文本输出
def generate_text_response(prompt):
    # 调用OpenAI的API生成文本响应
    response = client.chat.completions.create(
        model="gpt-4o",  # 使用的模型名称
        messages=[
            {"role": "system", "content": "assistant"},  # 系统消息
            {"role": "user", "content": prompt}  # 用户输入的提示
        ],
        max_tokens=150  # 最大生成的标记数
    )
    # 返回生成的响应文本
    return response.choices[0].message.content.strip()


# 定义函数来将图像编码为base64字符串
def encode_image(image_path):
    # 打开图像文件并读取其内容
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 定义函数来处理图像输入
def generate_image_response(image):
    # 将PIL 图像转为字节数组
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    # 将字节数组转换为base64 编码字符串
    base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
    # 调用OpenAI的Api生成图像响应
    response = client.chat.completions.create(
        model="gpt-4o",  # 使用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "这张照片里有什么？"},  # 用户输入的文本
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"  # base64编码的图像URL
                        },
                    },
                ],
            }
        ],
        max_tokens=300,  # 最大生成的token数
    )
    # 返回生成的响应文本
    return f"{response.choices[0].message.content.strip()}"

# 设置应用标题
st.title("多模态 简单Chatbot 应用")

st.header("文本输入")

text_input = st.text_input("输入你的问题：")
if st.button("发送文本"):
    if text_input:
        text_response = generate_text_response(text_input)
        st.write(f"回答： {text_response}")

    else:
        st.write("请输入文本内容")

st.header("图像输入")

uploaded_file = st.file_uploader(
    "上传一张图片",
    type=[
        'png',
        'jpg',
        'jpeg'
    ]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的图片", use_column_width=True)

    if st.button("发送图片"):
        image_response = generate_image_response(image)
        st.write(f"回答：{image_response}")
