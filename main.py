import os

import uvicorn
import httpx
from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

AI_ENGINEER_BASE_URL = os.getenv("AI_ENGINEER_BASE_URL") or "http://34.118.200.114:8000"
AI_ENGINEER_API_KEY = os.getenv("AI_ENGINEER_API_KEY")

# AI-engineer 경로 추가
app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /ask라는 URL 경로에 대해 POST HTTP 요청이 들어오면, FastAPI가 이 함수를 실행
# http://.../ask?model=gpt-4.1-nano
@app.post("/ask")
async def ask_ai_model(
    model: str = "gpt-4.1-nano",
    user_query: str = Body(..., description="사용자가 보낸 질문 텍스트"), # Body(...)'는 이 값이 본문에 포함되어야 하며, 필수 값
    previous_response_id: Optional[str] = Body(None, description="이전 대화의 ID, 연속적인 대화에 사용") # 'Body(None, ...)'는 body에 포함, 안 될 수도 있는 선택적 필드
):
    try:
        if not AI_ENGINEER_BASE_URL:
            raise HTTPException(status_code=500, detail="AI_ENGINEER_BASE_URL 환경변수가 설정되지 않았습니다.")
        # 요청 로깅
        print("=" * 50)
        print("클라이언트 요청 받음")
        print(f"모델: {model}")
        print(f"사용자 질문: {user_query}")
        print(f"이전 응답 ID: {previous_response_id}")
        print("=" * 50)
        
        payload = {
            "model": model,
            "user_query": user_query,
            "previous_response_id": previous_response_id,
        }
        headers = {}
        if AI_ENGINEER_API_KEY:
            headers["Authorization"] = f"Bearer {AI_ENGINEER_API_KEY}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{AI_ENGINEER_BASE_URL}/ask", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            response_text = data.get("response_text")
            previous_response_id = data.get("previous_response_id")

        # 응답 로깅
        print("=" * 50)
        print("AI 응답 생성 완료")
        print(f"응답 텍스트: {response_text}")
        print(f"새로운 응답 ID: {previous_response_id}")
        print("=" * 50)

        # 반환하는 값은 클라이언트(요청을 보낸 곳)에게 다시 전달
        return {
            "response_text": response_text,
            "previous_response_id": previous_response_id,
        }
    except Exception as e:
        print(f"❌ 에러 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
