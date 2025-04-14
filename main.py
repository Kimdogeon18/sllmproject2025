from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch

# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정 (HTML 요청 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안을 위해 실제 배포 시에는 도메인 제한 추천
    allow_methods=["*"],
    allow_headers=["*"]
)

# 모델과 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it")

# 입력 데이터 구조 정의
class InputText(BaseModel):
    text: str

# 텍스트 생성 엔드포인트
@app.post("/generate")
async def generate(input: InputText):
    inputs = tokenizer(input.text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return { "response": response }
