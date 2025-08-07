# backend

1. 이 리포지토리를 클론합니다.

   ```bash
   git clone https://github.com/Smash-RFP/backend.git

   ```

2. 패키지를 설치합니다.

   ```bash
    conda install -c conda-forge fastapi uvicorn
    or
    pip install fastapi uvicorn

   ```

3. 프로젝트를 실행 합니다.
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
