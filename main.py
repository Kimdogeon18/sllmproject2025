from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from fastapi.middleware.cors import CORSMiddleware

# Hugging Face 토큰 설정
os.environ['HF_TOKEN'] = "----"

# 모델 및 토크나이저 로딩
tokenizer = AutoTokenizer.from_pretrained('google/gemma-2-2b-it')
model = AutoModelForCausalLM.from_pretrained('google/gemma-2-2b-it')

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 처럼 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 body 구조 정의
class InputText(BaseModel):
    text: str

@app.post("/generate")  # POST 메서드로만 요청을 받음
async def generate_text(input_data: InputText):
    # 사용자 입력 → 토큰화
    input_ids = tokenizer(input_data.text, return_tensors="pt")

    # 모델에 입력 → 출력 생성
    with torch.no_grad():
        output_ids = model.generate(**input_ids, max_length=512)

    # 디코딩 (토큰 → 문자열)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return {"generated_text": output_text}