FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Run FastAPI on 8000 (internal/background) and Streamlit on 7860 (main)
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=7860 --server.address=0.0.0.0
