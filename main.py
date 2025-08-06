import uvicorn
from fastapi import FastAPI, HTTPException, Body
from typing import Optional
# from model import process_ai_query

app = FastAPI()

@app.post("/ask")
async def ask_ai_model(
    model: str = "default-model",
    user_query: str = Body(..., description="사용자가 보낸 질문 텍스트"), # Body(...)'는 이 값이 본문에 포함되어야 하며, 필수 값
    previous_response_id: Optional[str] = Body(None, description="이전 대화의 ID, 연속적인 대화에 사용") # 'Body(None, ...)'는 body에 포함, 안 될 수도 있는 선택적 필드
):
    try:
        # response_data = process_ai_query(
        #     user_query=user_query,
        #     model_name=model,
        #     prev_id=previous_response_id
        # )

        response_data = {
            "response_text": f"Processed response for query: {user_query} using model: {model}",
            "new_response_id": "12345" if previous_response_id is None else previous_response_id + "_next"
        }

        return {
            "response_text": response_data["response_text"],
            "previous_response_id": response_data["new_response_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
