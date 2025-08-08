import sys
import os

import uvicorn
from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

current_file_path = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(backend_dir)
sys.path.append(project_root)

current_file_path =os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_path)

# ai_engineer 디렉토리를 Python 경로에 추가
ai_engineer_path = os.path.join(project_root, "ai_engineer")
sys.path.append(ai_engineer_path)

from ai_engineer.main import openai_llm_response

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
        if openai_llm_response is None:
            raise HTTPException(
                status_code=500,
                detail=(
                    "ai_engineer 모듈을 불러올 수 없습니다. 레포에 `ai_engineer/main.py`와 "
                    "`openai_llm_response` 함수를 포함하거나, 해당 모듈을 의존성으로 배포하세요. "
                    f"원인: {_AI_ENGINEER_IMPORT_ERROR}"
                ),
            )
        # 요청 로깅
        print("=" * 50)
        print("클라이언트 요청 받음")
        print(f"모델: {model}")
        print(f"사용자 질문: {user_query}")
        print(f"이전 응답 ID: {previous_response_id}")
        print("=" * 50)
        
        response_text, previous_response_id = openai_llm_response(
            user_query=user_query, 
            previous_response_id=previous_response_id, 
            model=model
        )

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
